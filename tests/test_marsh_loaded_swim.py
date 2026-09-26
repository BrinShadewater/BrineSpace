import unittest,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from build_marsh_loaded_swim import build,DIRECTIONS
class LoadedSwim(unittest.TestCase):
    def test_reproduction_and_pickup_join(self):
        for direction in DIRECTIONS:
            with self.subTest(direction=direction):self.check_direction(direction)
    def check_direction(self,direction):
        KEYS=[f'swim-pickup-{direction}',f'swim-carry-{direction}']
        clips=build(direction=direction);folder=ROOT/f'character/marsh-v2/supplemental/loaded-swim-{direction}'
        for key,row in clips.items():
            self.assertEqual(len(row),6)
            for i,f in enumerate(row):self.assertEqual(f.tobytes(),Image.open(folder/f'{key}-{i:03}.png').convert('RGBA').tobytes())
        self.assertEqual(clips[KEYS[0]][-1].tobytes(),clips[KEYS[1]][0].tobytes())
        endpoint=Image.new('RGBA',(224,208));endpoint.alpha_composite(Image.open(ROOT/f'character/marsh-v2/frames/bare/salvage-{direction}/000.png').convert('RGBA'),(20,0))
        self.assertEqual(clips[KEYS[0]][0].tobytes(),endpoint.tobytes())
if __name__=='__main__':unittest.main()
