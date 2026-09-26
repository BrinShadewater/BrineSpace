"""Canonical Marsh maintenance selection, exact joins and alias isolation."""
from pathlib import Path
import sys,unittest
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from marsh_repair_revision import replacement,DIRECTIONS,STATES

class MarshRepair(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rows={s:replacement('marsh',s,False)['bare'] for s in STATES}

    def test_installed_pixels_rebuild(self):
        for state,row in self.rows.items():
            for i,expected in enumerate(row):
                path=ROOT/f'character/marsh-v2/frames/bare/{state}/{i:03}.png'
                actual=Image.open(path).convert('RGBA')
                self.assertEqual(actual.size,(184,184))
                self.assertEqual(actual.tobytes(),expected.tobytes(),str(path))
                self.assertLessEqual(set(actual.getchannel('A').tobytes()),{0,255})

    def test_equipped_loop_and_exact_joins(self):
        for d in DIRECTIONS:
            draw=self.rows['kneel-'+d];work=self.rows['repair-'+d];stow=self.rows['stand-'+d]
            idle=Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{d}/000.png').convert('RGBA').tobytes()
            self.assertEqual(draw[0].tobytes(),idle)
            self.assertEqual(stow[-1].tobytes(),idle)
            self.assertEqual(draw[-1].tobytes(),work[0].tobytes())
            self.assertEqual(work[-1].tobytes(),stow[0].tobytes())
            self.assertEqual(work[0].tobytes(),work[-1].tobytes())
            self.assertGreaterEqual(len({f.tobytes() for f in work}),3)
            self.assertTrue(all(f.tobytes()!=idle for f in work))

    def test_unrelated_states_are_not_selected(self):
        for d in DIRECTIONS:
            for a in ['weld','torch-draw','torch-stow','interact','eat','sit-down','idle']:
                self.assertIsNone(replacement('marsh',a+'-'+d,False))
            for actor in ['bill','veld','branforth']:
                self.assertIsNone(replacement(actor,'repair-'+d,True))

if __name__=='__main__':unittest.main()
