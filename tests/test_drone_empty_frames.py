"""Fail if marked invisible drone cells ever acquire visible artwork."""
import json
from pathlib import Path
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


class DroneEmptyFrames(unittest.TestCase):
    def test_marked_cells_match_source_alpha(self):
        data = json.loads((ROOT / 'assets/drone-runtime-2026-09-26/mining.json').read_text())
        tested = 0
        for name, clip in data['states'].items():
            record = clip.get('effectAtlas', {})
            if 'emptyFrameRanges' not in record:
                continue
            ranges = record['emptyFrameRanges']
            self.assertTrue(ranges, name)
            marked = set()
            for start, end in ranges:
                self.assertGreaterEqual(start, 0)
                self.assertLess(end, clip['frameCount'])
                self.assertLessEqual(start, end)
                indices = set(range(start, end + 1))
                self.assertFalse(marked & indices, name)
                marked.update(indices)
            with Image.open(ROOT / record['path'].removeprefix('res://')) as image:
                alpha = image.convert('RGBA').getchannel('A')
            w, h = data['frameWidth'], data['frameHeight']
            for index in range(clip['frameCount']):
                x, y = index % record['columns'] * w, index // record['columns'] * h
                with self.subTest(clip=name, frame=index):
                    self.assertEqual(alpha.crop((x, y, x+w, y+h)).getbbox() is None, index in marked)
            tested += 1
        self.assertEqual(tested, 4, 'All four mining directions must be covered')


if __name__ == '__main__':
    unittest.main()
