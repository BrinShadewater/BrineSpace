import sys,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from build_marsh_cargo_drain import build,DIRECTIONS
class CargoDrain(unittest.TestCase):
 def test_reproduction_and_registered_endpoints(self):
  for d in DIRECTIONS:
   with self.subTest(direction=d):
    row=build(direction=d);self.assertEqual(len(row),6)
    for i,f in enumerate(row):
     installed=ROOT/f'character/marsh-v2/supplemental/cargo-drain-{d}/cargo-drain-{d}-{i:03}.png'
     self.assertEqual(f.tobytes(),Image.open(installed).convert('RGBA').tobytes())
     self.assertLessEqual(set(f.getchannel('A').tobytes()),{0,255})
     a,b,c,e=f.getbbox();self.assertTrue(0<a and 0<b and c<224 and e<208)
    self.assertEqual(row[0].tobytes(),Image.open(ROOT/f'character/marsh-v2/supplemental/loaded-swim-{d}/swim-carry-{d}-000.png').convert('RGBA').tobytes())
    dry=Image.new('RGBA',(224,208));dry.alpha_composite(Image.open(ROOT/f'character/marsh-v2/frames/bare/carry-{d}/000.png').convert('RGBA'),(20,0))
    self.assertEqual(row[-1].tobytes(),dry.tobytes())
if __name__=='__main__':unittest.main()
