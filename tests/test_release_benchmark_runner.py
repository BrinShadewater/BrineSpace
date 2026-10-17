import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import json

spec = importlib.util.spec_from_file_location('runner', Path(__file__).resolve().parents[1] / 'tools/run_release_benchmark.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class ReleaseCopySafety(unittest.TestCase):
    def test_interrupted_benchmark_releases_runtime_and_checks_owner(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            executable = root / 'Game.exe'
            executable.write_bytes(b'EXE')
            executable.with_suffix('.pck').write_bytes(b'PCK')
            save = root / 'input.save'
            save.write_bytes(b'SAVE')
            profile = root / 'profile'
            profile.mkdir()
            out = root / 'evidence'
            argv = ['benchmark', '--release-exe', str(executable), '--save', str(save),
                    '--output', str(out), '--scenarios', 'fresh', '--runs', '1',
                    '--resolutions', '1920x1080']
            with mock.patch.object(runner.sys, 'argv', argv), \
                 mock.patch.object(runner.sys, 'platform', 'win32'), \
                 mock.patch.object(runner, 'owner_folder', return_value=root / 'owner'), \
                 mock.patch.object(runner, 'isolated_environment', return_value=({}, profile)), \
                 mock.patch.object(runner.subprocess, 'run', side_effect=TimeoutError('stopped')):
                with self.assertRaises(TimeoutError):
                    runner.main()
            self.assertFalse((out / 'release-runtime/Game.pck').exists())
            self.assertFalse((out / 'release-runtime/Game.exe').exists())
            self.assertEqual(json.loads((out / 'owner-check.json').read_text())['changes'], [])

    def test_space_guard_reserves_headroom_before_creating_a_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            executable = root / 'Game.exe'
            executable.write_bytes(b'EXE')
            executable.with_suffix('.pck').write_bytes(b'PCK')
            usage = mock.Mock(free=runner.MIN_FREE_BYTES + 5)
            with mock.patch.object(runner.shutil, 'disk_usage', return_value=usage):
                with self.assertRaises(OSError):
                    runner.prepare_release_copy(executable, root / 'qa')
            self.assertFalse((root / 'qa').exists())

    def test_finished_copy_cleanup_keeps_identity_and_delivery(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            executable = root / 'Game.exe'
            executable.write_bytes(b'EXE')
            executable.with_suffix('.pck').write_bytes(b'PCK')
            copied = runner.prepare_release_copy(executable, root / 'qa')
            runner.release_copy_storage(copied)
            self.assertFalse(copied.exists())
            self.assertFalse(copied.with_suffix('.pck').exists())
            self.assertTrue((copied.parent / 'identity.json').exists())
            self.assertEqual(executable.with_suffix('.pck').read_bytes(), b'PCK')

    def test_cleanup_preserves_modified_runtime_for_investigation(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            executable = root / 'Game.exe'
            executable.write_bytes(b'EXE')
            executable.with_suffix('.pck').write_bytes(b'PCK')
            copied = runner.prepare_release_copy(executable, root / 'qa')
            copied.with_suffix('.pck').write_bytes(b'changed')
            with self.assertRaises(ValueError):
                runner.release_copy_storage(copied)
            self.assertTrue(copied.exists())
            self.assertTrue(copied.with_suffix('.pck').exists())

    def test_long_windows_profile_is_relocated_and_recorded(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            evidence = root / ('evidence-' + 'x' * 90)
            short = root / 'short'
            with mock.patch.object(runner.sys, 'platform', 'win32'), mock.patch.object(runner.tempfile, 'mkdtemp', return_value=str(short)):
                env, profile = runner.isolated_environment(evidence)
            self.assertEqual(profile, short / 'Godot/app_userdata/BrineSpace')
            self.assertEqual(env['APPDATA'], str(short))
            self.assertTrue(profile.is_dir())
            recorded = json.loads((evidence / 'profile-location.json').read_text())
            self.assertEqual(recorded['profile'], str(profile))
            self.assertFalse((evidence / 'Godot').exists())

    def test_copy_keeps_delivery_and_its_overrides_untouched(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            delivery = root / 'delivery'
            delivery.mkdir()
            executable = delivery / 'Game.exe'
            executable.write_bytes(b'EXE')
            executable.with_suffix('.pck').write_bytes(b'PCK')
            (delivery / 'override.cfg').write_text('owner override')
            copied = runner.prepare_release_copy(executable, root / 'qa')
            self.assertEqual(copied.read_bytes(), b'EXE')
            self.assertEqual(copied.with_suffix('.pck').read_bytes(), b'PCK')
            self.assertEqual((delivery / 'override.cfg').read_text(), 'owner override')
            self.assertFalse(copied.samefile(executable))
            copied.write_bytes(b'changed QA copy')
            self.assertEqual(executable.read_bytes(), b'EXE')
            with self.assertRaises(FileExistsError):
                runner.prepare_release_copy(executable, root / 'qa')

    def test_missing_pack_does_not_create_a_partial_qa_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            executable = root / 'Game.exe'
            executable.write_bytes(b'EXE')
            with self.assertRaises(ValueError):
                runner.prepare_release_copy(executable, root / 'qa')
            self.assertFalse((root / 'qa').exists())


if __name__ == '__main__':
    unittest.main()
