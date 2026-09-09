import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from check_asset_alpha_probes import check


class AlphaProbes(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.image = Image.new('RGBA', (8, 6), (0, 0, 0, 0))
        self.image.putpixel((3, 3), (80, 70, 60, 255))
        self.image.save(self.root / 'asset.png')
        self.data = dict(export_path='asset.png', export_sha256=self.digest(),
                         coordinate_space='original native canvas pixels', native_canvas_px=[8, 6],
                         probes=[dict(name='handle', at=[1, 1], expected='transparent', alpha=0),
                                 dict(name='body', at=[3, 3], expected='opaque', alpha=255)])

    def digest(self):
        return hashlib.sha256((self.root / 'asset.png').read_bytes()).hexdigest()

    def run_check(self):
        (self.root / 'probes.json').write_text(json.dumps(self.data))
        return check(self.root, 'probes.json')

    def test_valid_and_read_only(self):
        before = (self.root / 'asset.png').read_bytes()
        result = self.run_check()
        self.assertEqual(result['checked'], 2)
        self.assertIn('Selected pixels only', result['scope'])
        self.assertEqual(before, (self.root / 'asset.png').read_bytes())

    def test_changed_image_fails_hash_before_pixels(self):
        self.image.putpixel((7, 5), (1, 2, 3, 255))
        self.image.save(self.root / 'asset.png')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            self.run_check()

    def test_filled_handle_fails_even_with_current_hash(self):
        self.image.putpixel((1, 1), (20, 20, 20, 255))
        self.image.save(self.root / 'asset.png')
        self.data['export_sha256'] = self.digest()
        with self.assertRaisesRegex(ValueError, 'expected alpha 0'):
            self.run_check()

    def test_hollow_body_fails(self):
        self.data['probes'][1]['at'] = [4, 4]
        with self.assertRaisesRegex(ValueError, 'expected alpha 255'):
            self.run_check()

    def test_rgb_not_assumed_opaque(self):
        self.image.convert('RGB').save(self.root / 'asset.png')
        self.data['export_sha256'] = self.digest()
        with self.assertRaisesRegex(ValueError, 'explicit alpha'):
            self.run_check()

    def test_invalid_coordinates(self):
        for at in ([8, 0], [-1, 0], [1.0, 1], [True, 1], [1]):
            with self.subTest(at=at):
                self.data['probes'][0]['at'] = at
                with self.assertRaisesRegex(ValueError, 'coordinate'):
                    self.run_check()

    def test_empty_and_duplicate_probes(self):
        self.data['probes'] = []
        with self.assertRaisesRegex(ValueError, 'At least one'):
            self.run_check()
        self.data['probes'] = [dict(name='a', at=[0, 0], expected='transparent', alpha=0),
                               dict(name='b', at=[0, 0], expected='transparent', alpha=0)]
        with self.assertRaisesRegex(ValueError, 'duplicate probe coordinate'):
            self.run_check()

    def test_wrong_record_and_canvas(self):
        self.data['probes'][0]['alpha'] = 255
        with self.assertRaisesRegex(ValueError, 'recorded alpha'):
            self.run_check()
        self.data['native_canvas_px'] = [6, 8]
        with self.assertRaisesRegex(ValueError, 'canvas mismatch'):
            self.run_check()

    def test_outside_export_rejected(self):
        self.data['export_path'] = '../outside.png'
        with self.assertRaisesRegex(ValueError, 'inside the project'):
            self.run_check()


if __name__ == '__main__':
    unittest.main()
