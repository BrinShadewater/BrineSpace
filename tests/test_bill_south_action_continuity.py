"""South work joins the canonical standing body and keeps stationary work anatomy."""
from pathlib import Path
import json
import unittest
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'character/major-bill-v3'


def frame(variant, action, index):
    return np.array(Image.open(ART / f'frames/{variant}/{action}-south/{index:03}.png').convert('RGBA'))


class BillSouthActionContinuity(unittest.TestCase):
    def test_standing_endpoints_match_live_idle_at_shared_pivot(self):
        for variant in ('bare', 'helmet'):
            expected = Image.new('RGBA', (256, 256))
            expected.alpha_composite(Image.fromarray(frame(variant, 'idle', 0)), (36, 52))
            self.assertTrue(np.array_equal(frame(variant, 'kneel', 0), np.array(expected)))
            self.assertTrue(np.array_equal(frame(variant, 'stand', 5), np.array(expected)))

    def test_tool_loop_preserves_body_and_connected_endpoints(self):
        record = json.loads((ART / 'sources/south-actions-style-2026-09-21/candidate-registration.json').read_text())
        mask = Image.new('L', (256, 256))
        ImageDraw.Draw(mask).polygon([tuple(p) for p in record['work']['replacement_polygon']], fill=255)
        stationary = np.array(mask) == 0
        for variant in ('bare', 'helmet'):
            base = frame(variant, 'kneel', 5)
            for index in range(6):
                self.assertTrue(np.array_equal(frame(variant, 'repair', index)[stationary], base[stationary]))
                self.assertTrue(np.array_equal(frame(variant, 'stand', index), frame(variant, 'kneel', 5-index)))
            for index in (0, 5):
                self.assertTrue(np.array_equal(frame(variant, 'repair', index), base))
            self.assertFalse(np.array_equal(frame(variant, 'repair', 2), base))


if __name__ == '__main__':
    unittest.main()
