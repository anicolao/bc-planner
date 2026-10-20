"""Actual fixed fixture-only adapter. No model/provider or host-selected tools.

This validates parts of an OS boundary; it deliberately does not implement
artifact publication, aggregate resource limits, or an accepted real launcher.
"""
import base64
import json
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import sys
import time

REPO = '/workspace/shared/bcenv-lecture'
sys.path.insert(0, REPO)
from services.controller import ExecReply, ExecRequest, ReadRequest, WriteRequest

BASE = Path('/workspace/shared/bc23-sandbox-probe')
PYTHON = '/nix/store/h3l4z7p6wny3phbckwwhy1i2g52pdnj4-python3-3.13.15/bin/python3'
HOST_PYTHON = '/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3'
SAFE = re.compile(r'[A-Za-z0-9_][A-Za-z0-9_.-]*\Z')


def path(value, write=False, directory=False):
    if type(value) is not str or not value.isascii() or len(value) > 240:
        raise ValueError('invalid_path')
    if directory and value == '.':
        return value
    parts = value.split('/')
    roots = ('src', 'scratch') if write else ('src', 'scratch', 'docs', 'artifacts', 'self_play')
    if (parts[0] not in roots or len(parts) > 16 or (not directory and len(parts) < 2)
            or any(p in ('.', '..') or not SAFE.fullmatch(p) for p in parts)):
        raise ValueError('invalid_path')
    return value


class ProbeSandboxAdapter:
    def __init__(self):
        self.last_execution = None

    def _run(self, argv, cwd='.', memory=268435456, wall=2, cap=16384, input_bytes=b''):
        if (type(argv) is not tuple or not 1 <= len(argv) <= 64 or
                any(type(s) is not str or '\x00' in s or len(s.encode()) > 4096 for s in argv)
                or not argv[0] or sum(len(s.encode()) for s in argv) > 16384):
            raise ValueError('invalid_argv')
        path(cwd, directory=True)
        if not (type(memory) is int and 16777216 <= memory <= 268435456 and
                type(wall) is int and 1 <= wall <= 10 and type(cap) is int and 128 <= cap <= 32768):
            raise ValueError('invalid_limits')
        command = ['/usr/bin/unshare', '--user', '--map-root-user', '--mount', '--pid',
                   '--fork', '--kill-child=SIGKILL', '--net', '--ipc', '--uts', '--',
                   HOST_PYTHON, '-I', '-B', str(BASE / 'namespace_launcher.py'),
                   '--cwd', cwd, '--memory', str(memory), '--'] + list(argv)
        command = [HOST_PYTHON, '-I', '-B', str(BASE / 'parent_death_guard.py'),
                   str(os.getpid())] + command
        start = time.monotonic()
        selector = None
        input_offset, total, reason = 0, 0, None
        buffers = {'stdout': bytearray(), 'stderr': bytearray()}

        def stop(why):
            nonlocal reason
            if reason is None:
                reason = why
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, close_fds=True, start_new_session=True,
                                   env={'PATH': '/usr/sbin:/usr/bin:/bin', 'LANG': 'C'})
        try:
            # Every post-spawn setup step is covered by mandatory cleanup.
            selector = selectors.DefaultSelector()
            for stream, name in ((process.stdout, 'stdout'), (process.stderr, 'stderr')):
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, name)
            # Input is controller-bounded source bytes only; avoid a blocking write.
            os.set_blocking(process.stdin.fileno(), False)
            if input_bytes:
                selector.register(process.stdin, selectors.EVENT_WRITE, 'stdin')
            else:
                process.stdin.close()
            # Closing stdout/stderr is not permission to outlive the deadline.
            while selector.get_map() or process.poll() is None:
                if time.monotonic() - start >= wall:
                    stop('timeout')
                for key, mask in selector.select(0.05):
                    if key.data == 'stdin':
                        try:
                            written = os.write(key.fd, input_bytes[input_offset:input_offset + 8192])
                            input_offset += written
                        except BrokenPipeError:
                            input_offset = len(input_bytes)
                        if input_offset >= len(input_bytes):
                            selector.unregister(key.fileobj)
                            key.fileobj.close()
                    else:
                        chunk = os.read(key.fd, 8192)
                        if not chunk:
                            selector.unregister(key.fileobj)
                            key.fileobj.close()
                            continue
                        keep = max(0, cap - total)
                        buffers[key.data].extend(chunk[:keep])
                        total += len(chunk)
                        if total > cap:
                            stop('output_limit')
                if reason is not None and time.monotonic() - start > wall + 2:
                    raise RuntimeError('descendant_teardown_unverified')
            code = process.wait(timeout=2)
        finally:
            try:
                if process.poll() is None:
                    stop('supervisor_cleanup')
                    process.wait(timeout=2)
            finally:
                # Selector.close does not close its registered pipe handles.
                try:
                    if selector is not None:
                        selector.close()
                finally:
                    for stream in (process.stdin, process.stdout, process.stderr):
                        stream.close()
        self.last_execution = {'exit_code': code, 'stop_reason': reason,
                               'elapsed_seconds': round(time.monotonic() - start, 4),
                               'output_bytes_retained': sum(len(v) for v in buffers.values())}
        status = 'timeout' if reason == 'timeout' else 'succeeded' if code == 0 and reason is None else 'failed'
        return ExecReply(status, bytes(buffers['stdout']), bytes(buffers['stderr']))

    def read(self, request):
        if type(request) is not ReadRequest or type(request.offset) is not int or type(request.limit) is not int:
            raise ValueError('invalid_read')
        path(request.path)
        if not 0 <= request.offset <= 1048576 or not 1 <= request.limit <= 8192:
            raise ValueError('invalid_read')
        reply = self._run((PYTHON, '-I', '-B', '/opt/io_worker.py'), input_bytes=json.dumps({
            'operation': 'read', 'path': request.path, 'offset': request.offset, 'limit': request.limit}).encode())
        if reply.status != 'succeeded':
            raise RuntimeError('workspace_read_failed')
        return base64.b64decode(json.loads(reply.stdout)['bytes'], validate=True)

    def write(self, request):
        if type(request) is not WriteRequest or type(request.content) is not bytes or len(request.content) > 524288:
            raise ValueError('invalid_write')
        path(request.path, write=True)
        reply = self._run((PYTHON, '-I', '-B', '/opt/io_worker.py'), input_bytes=json.dumps({
            'operation': 'write', 'path': request.path,
            'content': base64.b64encode(request.content).decode()}).encode())
        if reply.status != 'succeeded' or json.loads(reply.stdout) != {'status': 'ok'}:
            raise RuntimeError('workspace_write_failed')

    def exec(self, request):
        if type(request) is not ExecRequest:
            raise ValueError('invalid_exec')
        return self._run(request.argv, request.cwd, request.memory_bytes,
                         request.wall_seconds, request.output_bytes)
