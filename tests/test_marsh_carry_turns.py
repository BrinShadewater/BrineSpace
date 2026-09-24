import sys,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from build_marsh_carry_turns import build,PAIRS
import build_marsh_opposite_carry_turns as opposite
class CarryTurns(unittest.TestCase):
    def test_reproduction_and_joins(self):
        for pair in PAIRS:
            with self.subTest(pair=pair):self.check_pair(pair)
        for pair in opposite.PAIRS:
            with self.subTest(pair=pair):self.check_pair(pair,opposite.build)
    def check_pair(self,pair,builder=build):
        clips=builder(pair=pair);runtime=ROOT/f'character/marsh-v2/supplemental/carry-turn-{pair}'
        for key,row in clips.items():
            origin,dest=key.removeprefix('carry-turn-').split('-')
            for i,d in [(0,origin),(-1,dest)]:
                self.assertEqual(row[i].tobytes(),Image.open(ROOT/f'character/marsh-v2/frames/bare/carry-{d}/000.png').convert('RGBA').tobytes())
            for i,f in enumerate(row):
                self.assertEqual(f.tobytes(),Image.open(runtime/f'{key}-{i:03}.png').convert('RGBA').tobytes())
                self.assertLessEqual(set(f.getchannel('A').tobytes()),{0,255})
        origin,dest=pair.split('-')
        self.assertEqual([f.tobytes() for f in clips[f'carry-turn-{pair}']],[f.tobytes() for f in reversed(clips[f'carry-turn-{dest}-{origin}'])])
if __name__=='__main__':unittest.main()
