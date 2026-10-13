from pathlib import Path
import hashlib,json,unittest
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-quality-pass-v3'
class Quality(unittest.TestCase):
 def test_canonical_anatomy_and_provenance(self):
  data=json.loads((BASE/'installation.json').read_text());self.assertEqual(len(data['frames']),120)
  for path,r in data['frames'].items():
   for f,h in [(path,r['sha256']),(r['source'],r['sourceSha256']),(r['idleSource'],r['idleSha256'])]:self.assertEqual(hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),h)
   direction=Path(path).parent.name.rsplit('-',1)[-1];mask=np.array(Image.open(BASE/f'mask-{direction}.png'))>0
   out=np.array(Image.open(ROOT/path).convert('RGBA'));idle=np.array(Image.open(ROOT/r['idleSource']).convert('RGBA'))
   self.assertTrue(np.array_equal(out[~mask],idle[~mask]),path)
   self.assertTrue(np.array_equal(out[:69],idle[:69]),path+' face drift')
 def test_diagnostic_joins(self):
  for d in ('south','north','east','west'):
   def pose(action,slot):return np.array(Image.open(BASE/f'frames/{action}-{d}/{slot:03}.png').convert('RGBA'))
   self.assertTrue(np.array_equal(pose('kneel',2),pose('repair',0)),d+' entering repair')
   self.assertTrue(np.array_equal(pose('repair',5),pose('stand',0)),d+' leaving repair')
   idle=np.array(Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{d}/000.png').convert('RGBA'))
   self.assertTrue(np.array_equal(pose('kneel',0),idle));self.assertTrue(np.array_equal(pose('stand',2),idle))
 def test_complete_set_metadata_and_margin(self):
  contract=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
  self.assertEqual(len(contract),204);self.assertEqual(sum(len(s['files']) for s in contract.values()),1058)
  for key,s in contract.items():
   self.assertEqual(s['standingHeight'],148,key);self.assertEqual(len(s['files']),len(s['durations']),key);self.assertTrue(all(d>0 for d in s['durations']))
   for f in s['files']:
    im=Image.open(ROOT/f);b=im.getbbox();self.assertGreater(b[0],0,f);self.assertGreater(b[1],0,f);self.assertLess(b[2],im.width,f);self.assertLess(b[3],im.height,f)
if __name__=='__main__':unittest.main()
