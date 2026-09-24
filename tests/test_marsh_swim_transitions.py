"""Exact rebuild, endpoint and anatomical profile checks for selected swim pair."""
from pathlib import Path
import sys,unittest,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_marsh_swim_transitions import build

class SwimTransitions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rows={d:build(direction=d) for d in ['east','west','north','south']}
    def test_runtime_pixels_rebuild(self):
        for direction in self.rows:self.check_runtime(direction)
    def check_runtime(self,direction):
        folder=ROOT/f'character/marsh-v2/supplemental/swim-{direction}'
        for state,row in self.rows[direction].items():
            for i,f in enumerate(row):
                actual=Image.open(folder/f'{state}-{i:03}.png').convert('RGBA')
                self.assertEqual(actual.tobytes(),f.tobytes())
                self.assertEqual(actual.size,(184,208 if direction=='west' else 184))
                self.assertLessEqual(set(actual.getchannel('A').tobytes()),{0,255})
        manifest=json.loads((folder/'manifest.json').read_text())
        self.assertEqual(manifest['pivot'],[92,172])
        self.assertEqual(manifest['standingHeight'],148)
        for state in manifest['states']:
            self.assertEqual(sum(state['frameDurationsMs']),400)
            self.assertFalse(state['loop'])
            self.assertEqual(state['waterPoses'],[True]*5)
    def test_exact_existing_endpoints_and_reverse(self):
        for direction in self.rows:self.check_joins(direction)
    def check_joins(self,direction):
        start=self.rows[direction]['swim-start-'+direction];stop=self.rows[direction]['swim-stop-'+direction]
        for action,f in [('tread',start[0]),('swim',start[-1])]:
            current=Image.open(ROOT/f'character/marsh-v2/frames/bare/{action}-{direction}/000.png').convert('RGBA')
            padded=Image.new('RGBA',f.size);padded.alpha_composite(current)
            self.assertEqual(f.tobytes(),padded.tobytes())
        self.assertEqual([f.tobytes() for f in stop],[f.tobytes() for f in reversed(start)])
        self.assertEqual(len({f.tobytes() for f in start}),5)

if __name__=='__main__':unittest.main()
