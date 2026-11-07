"""Installed west work preserves connected body pixels and transition endpoints."""
from pathlib import Path
import json
import hashlib
import unittest
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'character/major-bill-v3'


def frame(variant, action, index):
    return np.array(Image.open(ART / f'frames/{variant}/{action}-west/{index:03}.png').convert('RGBA'))


class BillWestActionContinuity(unittest.TestCase):
    def test_selected_frames_match_reviewed_candidate(self):
        hashes=json.loads((ART/'sources/west-work-identity-2026-09-21/reviewed-candidate-hashes.json').read_text())
        self.assertEqual(len(hashes),36)
        for path,digest in hashes.items():
            with self.subTest(path=path):
                image=Image.open(ART/'frames'/path).convert('RGBA')
                self.assertEqual(hashlib.sha256(image.tobytes()).hexdigest(),digest)

    def test_work_changes_only_arm_region_and_keeps_endpoints(self):
        record = json.loads((ART / 'sources/west-work-identity-2026-09-21/work-registration.json').read_text())
        mask = Image.new('L', (256, 256))
        ImageDraw.Draw(mask).polygon([tuple(p) for p in record['replacement_polygon']], fill=255)
        stationary = np.array(mask) == 0
        for variant in ('bare', 'helmet'):
            base = frame(variant, 'kneel', 5)
            for index in range(6):
                work = frame(variant, 'repair', index)
                self.assertTrue(np.array_equal(work[stationary], base[stationary]))
                self.assertTrue(np.array_equal(frame(variant, 'stand', index), frame(variant, 'kneel', 5-index)))
            self.assertTrue(np.array_equal(base, frame(variant, 'repair', 0)))
            self.assertTrue(np.array_equal(base, frame(variant, 'repair', 5)))
            self.assertFalse(np.array_equal(base, frame(variant, 'repair', 2)), 'Tool loop is frozen')

    def test_lowering_keeps_front_contact_band_registered(self):
        for index in range(6):
            pixels = frame('bare', 'kneel', index)
            y, x = np.where(pixels[218:224, :, 3] > 0)
            self.assertEqual(int(x.min()), 108)
            self.assertEqual(int(np.where(pixels[:, :, 3] > 0)[0].max()) + 1, 223)


if __name__ == '__main__':
    unittest.main()
