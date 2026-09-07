"""Review-sheet contract tests; these do not certify artwork quality."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


class PropEdgeReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='edge-review-test-', dir=ROOT / 'output')
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.record = {'world_scale': 4, 'state': 'offline', 'renders': []}
        for bg, color in [('dark', (17, 29, 41)), ('light', (211, 223, 235))]:
            path = self.directory / f'{bg}.png'
            Image.new('RGB', (12, 12), color).save(path)
            self.record['renders'].append({'prop': 'host', 'background': bg,
                'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'crop': [2, 3, 6, 5]})

    def run_review(self, record=None):
        (self.directory / 'edge-review.json').write_text(json.dumps(record or self.record))
        return subprocess.run([sys.executable, str(ROOT / 'tools/review_registered_prop_edges.py'),
            str(self.directory), '--output', str(self.directory / 'sheet.png')],
            capture_output=True, text=True)

    def reject(self, record, message):
        result = self.run_review(record)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)
        self.assertFalse((self.directory / 'sheet.png').exists())

    def test_native_pixels_preserved(self):
        result = self.run_review()
        self.assertEqual(result.returncode, 0, result.stderr)
        with Image.open(self.directory / 'sheet.png') as sheet:
            self.assertEqual(sheet.size, (22, 78))
            self.assertEqual(sheet.crop((8, 26, 14, 31)).tobytes(), Image.new('RGB', (6, 5), (17, 29, 41)).tobytes())
            self.assertEqual(sheet.crop((8, 65, 14, 70)).tobytes(), Image.new('RGB', (6, 5), (211, 223, 235)).tobytes())

    def test_tampered_capture(self):
        self.record['renders'][0]['sha256'] = '0' * 64
        self.reject(self.record, 'Capture hash mismatch')

    def test_missing_background(self):
        self.record['renders'].pop()
        self.reject(self.record, 'Expected two backgrounds')

    def test_duplicate_background(self):
        self.record['renders'][1] = copy.deepcopy(self.record['renders'][0])
        self.reject(self.record, 'Duplicate prop/background')

    def test_mismatched_crops(self):
        self.record['renders'][1]['crop'][0] = 1
        self.reject(self.record, 'identical crop bounds')

    def test_invalid_crop(self):
        self.record['renders'][0]['crop'][2] = 20
        self.reject(self.record, 'Invalid diagnostic crop')

    def test_path_escape(self):
        self.record['renders'][0]['file'] = '../outside.png'
        self.reject(self.record, 'within source directory')

    def test_invalid_scale(self):
        self.record['world_scale'] = True
        self.reject(self.record, 'Invalid capture world scale')

    def test_wrong_state(self):
        self.record['state'] = 'working'
        self.reject(self.record, 'Expected offline')


if __name__ == '__main__':
    unittest.main()
