import importlib.util
import unittest
import sys
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build_marsh_opposite_swim_turns as opposite
spec=importlib.util.spec_from_file_location('turns',ROOT/'tools/build_marsh_swim_turns.py')
turns=importlib.util.module_from_spec(spec);spec.loader.exec_module(turns)

class SwimTurns(unittest.TestCase):
    def test_reproduction_endpoints_and_reverse(self):
        for pair in turns.PAIRS:
            with self.subTest(pair=pair):self.check_pair(pair)
        for pair in opposite.PAIRS:
            with self.subTest(pair=pair):self.check_pair(pair,opposite)

    def check_pair(self,pair,builder=turns):
        clips=builder.build(pair=pair)
        runtime=ROOT/f'character/marsh-v2/supplemental/swim-turn-{pair}'
        for name,row in clips.items():
            directions=name.removeprefix('swim-turn-').split('-')
            for index,direction in [(0,directions[0]),(-1,directions[1])]:
                endpoint=Image.new('RGBA',(184,208))
                endpoint.alpha_composite(Image.open(ROOT/f'character/marsh-v2/frames/bare/swim-{direction}/000.png').convert('RGBA'))
                self.assertEqual(row[index].tobytes(),endpoint.tobytes())
            for i,frame in enumerate(row):
                self.assertEqual(frame.tobytes(),Image.open(runtime/f'{name}-{i:03}.png').convert('RGBA').tobytes())
                self.assertLessEqual(set(frame.getchannel('A').tobytes()),{0,255})
        origin,destination=pair.split('-')
        self.assertEqual([f.tobytes() for f in clips[f'swim-turn-{pair}']], [f.tobytes() for f in reversed(clips[f'swim-turn-{destination}-{origin}'])])

if __name__=='__main__':unittest.main()
