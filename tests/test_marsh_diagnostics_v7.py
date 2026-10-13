from pathlib import Path
import hashlib,json,unittest
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-diagnostics-v7'
class Diagnostics(unittest.TestCase):
 def test_stable_identity_and_foot_art(self):
  for d in ('south','north','east','west'):
   idle=np.array(Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{d}/000.png'))
   for i in range(3):
    pose=np.array(Image.open(BASE/f'poses/{d}-{i}.png'))
    self.assertTrue(np.array_equal(pose[:58],idle[:58]))
    self.assertTrue(np.array_equal(pose[145:],idle[145:]))
 def test_tablet_readability_and_margin(self):
  for d in ('south','north','east','west'):
   for i in range(3):
    im=Image.open(BASE/f'poses/{d}-{i}.png');a=np.array(im).astype(int)
    cyan=(a[:,:,3]>0)&(a[:,:,1]-a[:,:,0]>18)&(a[:,:,2]-a[:,:,0]>18)&(a[:,:,1]>140)
    self.assertGreaterEqual(int(cyan.sum()),2 if d=='north' else 10,(d,i,'scanner unreadable'))
    b=im.getbbox();self.assertGreater(min(b[0],b[1],184-b[2],184-b[3]),1)
 def test_provenance_and_joins(self):
  records=json.loads((BASE/'installation.json').read_text())['frames'];self.assertEqual(len(records),120)
  for p,r in records.items():
   for f,h in [(p,r['sha256']),(r['source'],r['sourceSha256']),(r['idleSource'],r['idleSha256'])]:self.assertEqual(hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),h)
  for d in ('south','north','east','west'):
   def pose(a,i):return np.array(Image.open(BASE/f'frames/{a}-{d}/{i:03}.png'))
   idle=np.array(Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{d}/000.png'))
   self.assertTrue(np.array_equal(pose('kneel',0),idle));self.assertTrue(np.array_equal(pose('stand',2),idle))
   self.assertTrue(np.array_equal(pose('kneel',2),pose('repair',0)));self.assertTrue(np.array_equal(pose('repair',5),pose('stand',0)))
 def test_current_selection(self):
  current=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states'];old=json.loads((BASE/'baseline-contract.json').read_text())['states']
  self.assertEqual(len(current),204);self.assertEqual(sum(len(s['files']) for s in current.values()),1058)
  keys={s['id'] for s in json.loads((BASE/'manifest.json').read_text())['states']}
  for key in keys:
   self.assertTrue(all('marsh-diagnostics-v7/' in f for f in current[key]['files']))
   self.assertEqual(current[key]['durations'],old[key]['durations']);self.assertEqual(current[key]['loop'],old[key]['loop'])
  for key in current.keys()-keys:self.assertEqual(current[key]['files'],old[key]['files'])
if __name__=='__main__':unittest.main()


