import contextlib
import importlib.util
import io
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('runner', Path(__file__).resolve().parents[1] / 'tools/run_tests.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ExplicitSelection(unittest.TestCase):
    def run_list(self, names):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = m.run(['--only', names, '--list'])
        return code, output.getvalue()

    def test_python_test_cannot_silently_pass_as_zero_godot_tests(self):
        code, output = self.run_list('test_release_manifest')
        self.assertEqual(code, 2)
        self.assertIn('Python checks', output)

    def test_partially_valid_selection_rejects_typo(self):
        code, output = self.run_list('test_runtime_room_art,not_a_real_test')
        self.assertEqual(code, 2)
        self.assertIn('not_a_real_test', output)

    def test_existing_godot_check_still_lists(self):
        code, output = self.run_list('test_runtime_room_art')
        self.assertEqual(code, 0)
        self.assertIn('test_runtime_room_art', output)


if __name__ == '__main__':
    unittest.main()
