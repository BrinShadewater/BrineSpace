import json
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
from init_material_scale_review import initialize, digest


class ReviewInitialization(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        template = self.root/'skills/brinespace-room-pipeline/templates/material-scale-review.json'
        template.parent.mkdir(parents=True)
        source_template = Path(__file__).resolve().parents[1]/'skills/brinespace-room-pipeline/templates/material-scale-review.json'
        template.write_bytes(source_template.read_bytes())
        image = Image.new('RGBA', (20, 40), (0, 0, 0, 0))
        image.paste((80, 90, 100, 255), (2, 4, 18, 36))
        image.save(self.root/'source.png')
        image.save(self.root/'export.png')
        (self.root/'prompt.txt').write_text('exact prompt')
        self.reg = {'source': 'res://source.png', 'sha256': digest(self.root/'source.png'), 'region': [2, 4, 16, 32]}
        self.write_reg()

    def write_reg(self):
        (self.root/'registration.json').write_text(json.dumps(self.reg))

    def build(self, **kwargs):
        return initialize(self.root, 'registration.json', 'export.png', 'prompt.txt', 'fixture', **kwargs)

    def test_height_scale_and_no_visual_acceptance(self):
        result = self.build(height=328)
        self.assertEqual(result['proposed_display_width_world'], 164)
        self.assertEqual(result['prompt_sha256'], digest(self.root/'prompt.txt'))
        self.assertIsNone(result['owner_acceptance'])
        for gate in ('materials', 'native_scale', 'alpha'):
            self.assertIsNone(result['review'][gate]['verdict'])

    def test_changed_source_rejected(self):
        self.reg['sha256'] = 'outdated'
        self.write_reg()
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            self.build(width=38)

    def test_opaque_export_rejected(self):
        Image.new('RGBA', (20, 40), (0, 0, 0, 255)).save(self.root/'export.png')
        with self.assertRaisesRegex(ValueError, 'transparent and visible'):
            self.build(width=38)

    def test_outside_region_rejected(self):
        self.reg['region'][2] = 100
        self.write_reg()
        with self.assertRaisesRegex(ValueError, 'outside'):
            self.build(width=38)

    def test_invalid_scale_rejected(self):
        for size in (0, -1, float('nan'), float('inf')):
            with self.subTest(size=size), self.assertRaises(ValueError):
                self.build(width=size)


if __name__ == '__main__':
    unittest.main()
