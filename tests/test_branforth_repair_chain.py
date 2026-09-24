"""Selected repair chains must rebuild exactly and join their actual idle endpoints."""
from pathlib import Path
import sys
import unittest
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from branforth_repair_revision import replacement, STATES

class RepairChain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {state: replacement('branforth', state, True) for state in STATES}

    def test_all_selected_frames_rebuild_exactly(self):
        for state, variants in self.rows.items():
            for variant, row in variants.items():
                for i, expected in enumerate(row):
                    path = ROOT / f'character/chief-engineer-branforth-v2/frames/{variant}/{state}/{i:03}.png'
                    actual = Image.open(path).convert('RGBA')
                    self.assertEqual(actual.tobytes(), expected.tobytes(), str(path))
                    self.assertEqual(actual.size, (256, 256))
                    self.assertLessEqual(set(actual.getchannel('A').tobytes()), {0, 255})

    def test_exact_joins_and_idle_registration(self):
        for direction in ['south','north','west']:
            self.check_joins(direction)

    def check_joins(self, direction):
        for variant in ['bare', 'helmet']:
            kneel = self.rows['kneel-'+direction][variant]
            repair = self.rows['repair-'+direction][variant]
            stand = self.rows['stand-'+direction][variant]
            idle = Image.open(ROOT / f'character/chief-engineer-branforth-v2/frames/{variant}/idle-{direction}/000.png').convert('RGBA')
            registered = Image.new('RGBA', (256, 256))
            registered.alpha_composite(idle, (36, 52))
            self.assertEqual(kneel[0].tobytes(), registered.tobytes())
            self.assertEqual(kneel[-1].tobytes(), repair[0].tobytes())
            self.assertEqual(repair[0].tobytes(), repair[-1].tobytes())
            self.assertEqual(repair[-1].tobytes(), stand[0].tobytes())
            self.assertEqual(stand[-1].tobytes(), registered.tobytes())

    def test_override_does_not_capture_shared_source_aliases(self):
        self.assertIsNone(replacement('branforth', 'interact-south', True))
        self.assertIsNone(replacement('veld', 'repair-south', True))
        self.assertIsNone(replacement('marsh', 'repair-south', False))

if __name__ == '__main__':
    unittest.main()
