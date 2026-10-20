"""Bounded independent checks; only fresh synthetic fixture contents are touched."""
import os
import sys
import time
from pathlib import Path
from unittest.mock import patch
import unittest

import test_source_export as original
from export_backend import EXPORT_ARGV
from probe_adapter import BASE

class IndependentSourceExportTests(original.SourceExportTests):
    def test_exact_file_byte_cap_is_accepted(self):
        result = self.execute('open("/workspace/' + original.PATH + '","wb").write(b"x"*524288)')
        self.assertEqual(result.status, 'succeeded')
        unused, snapshot = self.capture()
        accepted = original.accept_source_zip(snapshot.archive, snapshot.package)
        self.assertEqual(len(accepted.files[0].data), 524288)

    def test_exact_128_files_is_accepted(self):
        result = self.execute("for n in range(127):open('/workspace/src/fixturebot/C'+str(n)+'.java','wb').write(b'x')")
        self.assertEqual(result.status, 'succeeded')
        unused, snapshot = self.capture()
        self.assertEqual(len(original.accept_source_zip(snapshot.archive, snapshot.package).files), 128)

    def test_exact_path_cap_then_excess_is_rejected(self):
        for size in (224, 225):
            result = self.execute("open('/workspace/src/fixturebot/'+'A'*" + str(size) + "+'.java','wb').write(b'x')")
            self.assertEqual(result.status, 'succeeded')
            if size == 224:
                self.capture()
            else:
                self.reject()

    def test_visited_entry_cap_is_rejected(self):
        result = self.execute("import os\nfor n in range(256):os.mkdir('/workspace/src/fixturebot/D'+str(n))")
        self.assertEqual(result.status, 'succeeded')
        start = time.monotonic()
        self.reject()
        self.assertLess(time.monotonic() - start, 2)

    def test_case_collision_is_rejected(self):
        self.adapter.write(original.WriteRequest('src/fixturebot/robotplayer.java', b'x'))
        self.reject()

    def test_failed_export_after_success_never_reuses_old_handle(self):
        old_result, old = self.capture()
        self.adapter.write(original.WriteRequest(original.PATH, b'\x00'))
        self.reject()
        self.assertEqual(len(self.store._artifacts), 1)
        self.assertIs(self.store.resolve('synthetic-owner', 'synthetic-run', old_result.artifact_id), old)

    def test_valid_zip_on_normal_stdout_never_mints_handle(self):
        unused, snapshot = self.capture()
        count = len(self.store._artifacts)
        result = self.execute('import sys;sys.stdout.buffer.write(' + repr(snapshot.archive) + ')')
        self.assertEqual(result.status, 'succeeded')
        self.assertEqual(result.stdout, snapshot.archive)
        self.assertIsNone(result.artifact_id)
        self.assertEqual(len(self.store._artifacts), count)

    def test_collector_argument_alias_cannot_export(self):
        for argv in (('bcenv.fixture.export-source.v1 ',), ('./bcenv.fixture.export-source.v1',)):
            result = self.adapter.exec(original.request(argv))
            self.assertEqual(result.status, 'failed')
            self.assertIsNone(result.artifact_id)
        self.assertEqual(len(self.store._artifacts), 0)

    def test_selector_poll_exception_cleanup_blocks_future_export(self):
        import probe_adapter
        real_selector = probe_adapter.selectors.DefaultSelector
        real_popen = probe_adapter.subprocess.Popen
        captured = []
        def popen(*args, **kwargs):
            process = real_popen(*args, **kwargs)
            captured.append(process)
            return process
        def selector():
            instance = real_selector()
            def fail_select(timeout=None):
                raise RuntimeError('synthetic_poll_error')
            instance.select = fail_select
            return instance
        with patch('probe_adapter.selectors.DefaultSelector', selector), patch('probe_adapter.subprocess.Popen', popen):
            with self.assertRaisesRegex(RuntimeError, '^synthetic_poll_error$'):
                self.execute('import time;time.sleep(2)')
        self.assertEqual(len(captured), 1)
        self.assertIsNotNone(captured[0].poll())
        self.assertTrue(all(stream.closed for stream in (captured[0].stdin, captured[0].stdout, captured[0].stderr)))
        self.assertEqual(self.reject().stderr, b'workspace_cleanup_unverified\n')

    def test_fresh_copy_writes_do_not_reach_author_fixture(self):
        author_root = Path('/workspace/shared/bc23-source-export-probe')
        name = 'ReviewIsolation' + str(time.time_ns()) + '.java'
        original_path = author_root / 'writable' / 'src' / 'fixturebot' / name
        self.assertFalse(original_path.exists())
        result = self.execute("open('/workspace/src/fixturebot/" + name + "','wb').write(b'x')")
        self.assertEqual(result.status, 'succeeded')
        self.assertTrue((BASE / 'writable' / 'src' / 'fixturebot' / name).exists())
        self.assertFalse(original_path.exists())
        unused, snapshot = self.capture()
        self.assertIn('fixturebot/' + name,
                      [item.path for item in original.accept_source_zip(snapshot.archive, snapshot.package).files])
        self.assertNotEqual((BASE / 'fixture-root' / 'opt' / 'source_collector.py').stat().st_ino,
                            (author_root / 'fixture-root' / 'opt' / 'source_collector.py').stat().st_ino)

if __name__ == '__main__':
    unittest.main(verbosity=2)
