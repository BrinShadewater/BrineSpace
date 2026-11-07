from pathlib import Path
import json,hashlib,unittest
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-quality-pass-v4'
def visual(im):
 crop=im.crop(im.getbbox());return hashlib.sha256(str(crop.size).encode()+crop.tobytes()).hexdigest()
class FullSet(unittest.TestCase):
 def test_source_integrity_geometry_and_shared_poses(self):
  old=json.loads((BASE/'baseline-contract.json').read_text())['states'];selected=json.loads((BASE/'selection.json').read_text())['states'];shared={}
  self.assertEqual(len(selected),204);self.assertEqual(sum(len(s) for s in selected.values()),1058)
  for key,s in old.items():
   for f,h,p in zip(s['files'],s['hashes'],selected[key]):
    self.assertEqual(hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),h)
    before=Image.open(ROOT/f).convert('RGBA');after=Image.open(ROOT/p).convert('RGBA');a=np.array(before);b=np.array(after)
    self.assertEqual(before.size,after.size);self.assertTrue(np.array_equal(a[:,:,3],b[:,:,3]),p)
    old_id=visual(before);new_id=visual(after)
    if old_id in shared:self.assertEqual(shared[old_id],new_id,key+' shared pose diverged')
    shared[old_id]=new_id
    if key.startswith(('idle-','walk','crew-chat-','injury-','death-','torch-','weld')):self.assertTrue(np.array_equal(a,b),key+' protected art changed')
    if key.split('-')[0] in ('interact','repair','inspect','salvage','kneel','stand'):
     self.assertTrue(np.array_equal(a[:58],b[:58]));self.assertTrue(np.array_equal(a[145:],b[145:]))
 def test_current_metadata_and_selection(self):
  old=json.loads((BASE/'baseline-contract.json').read_text())['states'];new=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states'];selection=json.loads((BASE/'selection.json').read_text())['states']
  self.assertEqual(old.keys(),new.keys())
  for key in old:
   self.assertEqual(new[key]['files'],selection[key])
   for field in ('durations','loop','pivot','standingHeight'):self.assertEqual(old[key][field],new[key][field],key+' '+field)
 def test_all_export_hashes(self):
  for f,r in json.loads((BASE/'installation.json').read_text())['frames'].items():self.assertEqual(hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),r['sha256'])
 def test_water_and_furniture_metadata(self):
  original=json.loads((BASE/'original-state-entries.json').read_text())
  for rel in json.loads((BASE/'manifest-list.json').read_text()):
   manifest=ROOT/'character/marsh-v2'/rel
   for entry in json.loads(manifest.read_text())['states']:
    expected={k:v for k,v in original[entry['id']].items() if k!='frameFiles'}
    actual={k:v for k,v in entry.items() if k!='frameFiles'}
    self.assertEqual(actual,expected,entry['id'])
if __name__=='__main__':unittest.main()
