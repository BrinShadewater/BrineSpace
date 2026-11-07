import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('runner',Path(__file__).resolve().parents[1]/'tools/run_wall_asset_review.py')
runner=importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class LogAcceptance(unittest.TestCase):
    def test_pass_does_not_mask_script_error(self):
        self.assertTrue(runner.review_errors(0,'SCRIPT ERROR: Parse Error\nWALL ASSET PASS: exported'))

    def test_pass_does_not_mask_load_error(self):
        self.assertTrue(runner.review_errors(0,'ERROR: Failed to load\nWALL ASSET PASS: exported'))

    def test_incomplete_and_crash_are_failures(self):
        self.assertTrue(runner.review_errors(0,'Godot starting'))
        self.assertTrue(runner.review_errors(1,'WALL ASSET PASS: exported'))

    def test_clean_pass_allows_nonfatal_warning(self):
        self.assertFalse(runner.review_errors(0,'WARNING: import note\nWALL ASSET PASS: exported'))


if __name__=='__main__':
    unittest.main()
