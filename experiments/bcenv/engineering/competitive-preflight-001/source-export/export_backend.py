"""Fixture-only trusted export operation over the reviewed namespace prototype.

No artifact ID is accepted or issued here. CapturingSandboxAdapter owns that
step. The lock serializes only calls through this instance in this process;
other trusted host processes are outside this fixture's exclusion guarantee.
"""
import threading

from probe_adapter import PYTHON, ProbeSandboxAdapter
from services.controller import ExecRequest
from services.controller_ledger import ExportedExecReply, SourceExport
from services.scrimmage import IntakeLimits, SubmissionRejected, accept_source_zip

EXPORT_ARGV = ('bcenv.fixture.export-source.v1',)
FIXTURE_PACKAGE = 'fixturebot'
COLLECTOR_ARGV = (PYTHON, '-I', '-B', '/opt/source_collector.py')


class ExportingFixtureBackend:
    def __init__(self):
        self._runner = ProbeSandboxAdapter()
        self._lock = threading.Lock()
        self._cleanup_uncertain = False
        self.last_export = None

    def read(self, request):
        with self._lock:
            if self._cleanup_uncertain:
                raise RuntimeError('workspace_cleanup_unverified')
            try:
                return self._runner.read(request)
            except BaseException:
                self._cleanup_uncertain = True
                raise

    def write(self, request):
        with self._lock:
            if self._cleanup_uncertain:
                raise RuntimeError('workspace_cleanup_unverified')
            try:
                return self._runner.write(request)
            except BaseException:
                self._cleanup_uncertain = True
                raise

    def exec(self, request):
        if type(request) is not ExecRequest:
            raise ValueError('invalid_exec')
        with self._lock:
            if self._cleanup_uncertain:
                return ExportedExecReply('failed', stderr=b'workspace_cleanup_unverified\n')
            if request.argv != EXPORT_ARGV:
                try:
                    reply = self._runner.exec(request)
                except BaseException:
                    # No future export after a supervisor exception that could
                    # leave process teardown uncertain. Start a fresh fixture.
                    self._cleanup_uncertain = True
                    raise
                return ExportedExecReply(reply.status, reply.stdout, reply.stderr)
            if (request.cwd != '.' or type(request.wall_seconds) is not int or
                    not 1 <= request.wall_seconds <= 10 or type(request.memory_bytes) is not int or
                    not 16777216 <= request.memory_bytes <= 268435456 or
                    type(request.output_bytes) is not int or not 128 <= request.output_bytes <= 32768):
                return ExportedExecReply('failed', stderr=b'invalid_source_export_request\n')
            self.last_export = None
            try:
                reply = self._runner._run(COLLECTOR_ARGV, cwd='.', memory=request.memory_bytes,
                    wall=min(2, request.wall_seconds), cap=IntakeLimits().max_archive_bytes,
                    _collector=True)
            except BaseException:
                self._cleanup_uncertain = True
                raise
            self.last_export = dict(self._runner.last_execution)
            if reply.status != 'succeeded':
                return ExportedExecReply(reply.status, stderr=b'source_export_failed\n')
            try:
                accept_source_zip(reply.stdout, FIXTURE_PACKAGE)
            except SubmissionRejected:
                return ExportedExecReply('failed', stderr=b'source_export_rejected\n')
            # ZIP bytes are a private trusted side channel, never model stdout.
            return ExportedExecReply('succeeded', stdout=b'source export validated\n',
                source=SourceExport(FIXTURE_PACKAGE, bytes(reply.stdout)))
