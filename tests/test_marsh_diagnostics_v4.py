from pathlib import Path
import json,unittest,hashlib,sys
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from prepare_marsh_diagnostics_v4 import scanner_mask
BASE=ROOT/'character/marsh-diagnostics-v4'
class Diagnostics(unittest.TestCase):
 def test_foreground_and_identity(self):
  records=json.loads((BASE/'installation.json').read_text())['frames'];self.assertEqual(len(records),120)
  regression_pixels=0
  for path,r in records.items():
   for f,h in [(path,r['sha256']),(r['source'],r['sourceSha256']),(r['idleSource'],r['idleSha256'])]:self.assertEqual(hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),h)
   source=Image.open(ROOT/r['source']).convert('RGBA');out=np.array(Image.open(ROOT/path).convert('RGBA'));idle=np.array(Image.open(ROOT/r['idleSource']).convert('RGBA'))
   screen=scanner_mask(source);self.assertTrue(np.array_equal(out[screen],np.array(source)[screen]),path)
   direction=Path(path).parent.name.rsplit('-',1)[-1]
   # Face/neck and lower body stay canonical, including side head above the scanner.
   self.assertTrue(np.array_equal(out[:69,80:109],idle[:69,80:109]),path)
   self.assertTrue(np.array_equal(out[129:],idle[129:]),path)
   old=np.array(Image.open(ROOT/'character/marsh-quality-pass-v3/frames'/Path(path).parent.name/Path(path).name).convert('RGBA'))
   regression_pixels+=int(np.any(old[screen]!=out[screen],axis=1).sum())
  self.assertGreater(regression_pixels,0,'Must cover the actual v3 scanner regression')
 def test_transition_joins(self):
  for d in ('south','north','east','west'):
   def pose(a,i):return np.array(Image.open(BASE/f'frames/{a}-{d}/{i:03}.png').convert('RGBA'))
   self.assertTrue(np.array_equal(pose('kneel',2),pose('repair',0)))
   self.assertTrue(np.array_equal(pose('repair',5),pose('stand',0)))
   idle=np.array(Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{d}/000.png').convert('RGBA'))
   self.assertTrue(np.array_equal(pose('kneel',0),idle));self.assertTrue(np.array_equal(pose('stand',2),idle))
 def test_selection_and_timing(self):
  current=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
  original=json.loads((BASE/'source-contract.json').read_text())['states']
  self.assertEqual(len(current),204);self.assertEqual(sum(len(s['files']) for s in current.values()),1058)
  for state in json.loads((BASE/'manifest.json').read_text())['states']:
   key=state['id'];self.assertEqual(current[key]['durations'],original[key]['durations']);self.assertEqual(current[key]['loop'],original[key]['loop'])
   self.assertTrue(all('marsh-diagnostics-v4/' in f for f in current[key]['files']))
if __name__=='__main__':unittest.main()
