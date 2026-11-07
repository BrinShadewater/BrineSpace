"""Repaired work states retain the physical helmet shell used by standing Bill."""
import json
import sys
import unittest
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from rebuild_bill_art import HelmetRebaker, WATER


class BillWorkHelmetScale(unittest.TestCase):
    def test_smaller_shell_preserves_compact_fits_and_registration_canvas(self):
        legacy=HelmetRebaker(None)
        selected=HelmetRebaker(None,max_height=48)
        for view in ('north','front','east','west'):
            with self.subTest(view=view):
                self.assertEqual(selected.overlay(view,(34,40)).tobytes(),legacy.overlay(view,(34,40)).tobytes())
                original=legacy.overlay(view)
                reduced=selected.overlay(view)
                self.assertEqual(reduced.size,original.size)
                bounds=reduced.getbbox()
                self.assertLessEqual(bounds[3]-bounds[1],48)
                self.assertLess(np.count_nonzero(np.array(reduced)[:,:,3]),np.count_nonzero(np.array(original)[:,:,3]))

    def test_work_retains_standing_helmet_shell_pixels_and_size(self):
        for direction in ('west', 'north', 'south'):
            with self.subTest(direction=direction):
                self.check_direction(direction)

    def check_direction(self, direction):
        idle = json.loads((WATER / f'equipment/dry/bill-idle-{direction}/registration.json').read_text())
        overlay = np.array(HelmetRebaker(None,max_height=48).overlay(Path(idle['overlay']).parent.name))
        source_folder = f'{direction}-actions-style-2026-09-21' if direction in ('west', 'south') else f'{direction}-actions-2026-09-21'
        if direction=='north':source_folder='north-work-identity-2026-09-21'
        if direction=='west':source_folder='west-work-identity-2026-09-21'
        fit = json.loads((ROOT / f'character/major-bill-v3/sources/{source_folder}/helmet-registration.json').read_text())
        self.assertEqual(tuple(fit['overlay_size']), (overlay.shape[1], overlay.shape[0]))
        for row in fit['head_anchors']:
            action = 'repair' if row['folder'].startswith('repair') else 'kneel'
            if direction in ('north','west') and action=='kneel' and row['frame']==0:
                # The selected standing endpoint now uses the exact idle fit;
                # its old generated-pose head anchor is intentionally superseded.
                continue
            with self.subTest(action=action, frame=row['frame']):
                image = np.array(Image.open(ROOT / f'character/major-bill-v3/frames/helmet/{action}-{direction}/{row["frame"]:03}.png').convert('RGBA'))
                x, y = np.array(row['head']) - np.array(fit['overlay_anchor_offset'])
                region = image[y:y+overlay.shape[0], x:x+overlay.shape[1]]
                shell = overlay[:, :, 3] > 0
                self.assertEqual(region.shape, overlay.shape)
                self.assertTrue(np.array_equal(region[shell], overlay[shell]), 'Standing helmet shrank or changed shell pixels during work')


if __name__ == '__main__':
    unittest.main()
