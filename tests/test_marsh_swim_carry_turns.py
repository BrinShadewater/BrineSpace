import sys,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from build_marsh_swim_carry_turns import build,PAIRS
import build_marsh_opposite_swim_carry_turns as opposite

class LoadedSwimTurns(unittest.TestCase):
    def test_reproduction_and_joins(self):
        for pair in PAIRS:
            with self.subTest(pair=pair):self.check_pair(pair,build,5)
        for pair in opposite.PAIRS:
            with self.subTest(pair=pair):self.check_pair(pair,opposite.build,9)

    def check_pair(self,pair,builder,count):
        clips=builder(pair=pair);runtime=ROOT/f'character/marsh-v2/supplemental/swim-carry-turn-{pair}'
        for key,row in clips.items():
            origin,dest=key.removeprefix('swim-carry-turn-').split('-');self.assertEqual(len(row),count)
            for i,d in [(0,origin),(-1,dest)]:
                current=ROOT/f'character/marsh-v2/supplemental/loaded-swim-{d}/swim-carry-{d}-000.png'
                self.assertEqual(row[i].tobytes(),Image.open(current).convert('RGBA').tobytes())
            for i,f in enumerate(row):
                self.assertEqual(f.tobytes(),Image.open(runtime/f'{key}-{i:03}.png').convert('RGBA').tobytes())
                self.assertLessEqual(set(f.getchannel('A').tobytes()),{0,255})
                left,top,right,bottom=f.getbbox()
                self.assertTrue(0<left and 0<top and right<224 and bottom<208)
        origin,dest=pair.split('-')
        self.assertEqual([f.tobytes() for f in clips[f'swim-carry-turn-{pair}']],
            [f.tobytes() for f in reversed(clips[f'swim-carry-turn-{dest}-{origin}'])])

if __name__=='__main__':unittest.main()
