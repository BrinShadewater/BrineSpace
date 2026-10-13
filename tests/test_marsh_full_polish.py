"""All-state continuity, grading protection and reproducible selected sources."""
from pathlib import Path
import json,hashlib,sys,unittest
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-full-polish-v1'
sys.path.insert(0,str(ROOT/'tools'))
from rebuild_marsh_art import MarshRebaker
from prepare_marsh_full_polish import material_mask

class Polish(unittest.TestCase):
    def test_every_slot_and_shared_pose(self):
        states=json.loads((BASE/'baseline-contract.json').read_text())['states'];selection=json.loads((BASE/'selection.json').read_text());seen={};rebaker=MarshRebaker({})
        self.assertEqual(len(states),192);self.assertEqual(sum(len(s['files']) for s in states.values()),978)
        for k,s in states.items():
            current=rebaker.state_override(k) if k in selection['changedStates'] else None
            for i,(f,h) in enumerate(zip(s['files'],s['hashes'])):
                original=Image.open(BASE/'original'/f).convert('RGBA');selected=Image.open(ROOT/selection['states'][k][i]).convert('RGBA');actual=Image.open(ROOT/f).convert('RGBA')
                self.assertEqual(selected.tobytes(),actual.tobytes(),f);self.assertEqual(original.size,selected.size);self.assertEqual(original.getchannel('A').tobytes(),selected.getchannel('A').tobytes())
                if h in seen:self.assertEqual(seen[h],selected.tobytes(),'Shared pose changed differently: '+k)
                seen[h]=selected.tobytes()
                crop=original.crop(original.getbbox());visual_hash=hashlib.sha256(str(crop.size).encode()+crop.tobytes()).hexdigest();new_crop=selected.crop(selected.getbbox()).tobytes()
                if visual_hash in seen:self.assertEqual(seen[visual_hash],new_crop,'Padded shared pose changed differently: '+k)
                seen[visual_hash]=new_crop
                if current:
                    quality=ROOT/'character/marsh-quality-pass-v2/installation.json'
                    if k=='tread-north' and quality.exists():
                        # Later registration layer preserves the frozen polish
                        # pixels at a different canvas offset, independently audited.
                        self.assertEqual(current[i].crop(current[i].getbbox()).tobytes(),selected.crop(selected.getbbox()).tobytes())
                    else:self.assertEqual(current[i].tobytes(),selected.tobytes())
                if k.startswith(('idle-','walk')):self.assertEqual(original.tobytes(),selected.tobytes())
        for old in (BASE/'original/character/marsh-v2').rglob('manifest.json'):
            self.assertEqual(old.read_bytes(),(ROOT/old.relative_to(BASE/'original')).read_bytes())

    def test_only_material_mask_changes(self):
        records=json.loads((BASE/'colour-lock.json').read_text())
        self.assertGreater(len(records),100)
        for f,r in records.items():
            original=Image.open(ROOT/r['original']).convert('RGBA');selected=Image.open(ROOT/r['source']).convert('RGBA');mask=np.asarray(Image.open(ROOT/r['mask']))>0;a=np.asarray(original);b=np.asarray(selected);_,_,protected=material_mask(original)
            self.assertTrue(np.array_equal(a[~mask],b[~mask]),f);self.assertTrue(np.array_equal(a[protected],b[protected]),f);self.assertTrue(np.array_equal(a[:,:,3],b[:,:,3]),f)
            self.assertEqual(hashlib.sha256((ROOT/r['original']).read_bytes()).hexdigest(),r['before']);self.assertEqual(hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),r['after'])

    def test_north_anatomy_and_staged_white_fluid(self):
        north=ROOT/'character/marsh-shutdown-injury-match-v1';old=Image.open(north/'north-revision-01-backup/death-ground.png').getbbox();new=Image.open(north/'frames/death-ground-north/005.png').getbbox()
        self.assertLess(new[2]-new[0],old[2]-old[0]);self.assertGreater(new[3]-new[1],old[3]-old[1])
        poses=json.loads((north/'registration.json').read_text())['poses']
        self.assertEqual(len([r for r in poses if r['source'].endswith('north-sheet-02.png')]),2)
        for d in ('south','north','east','west'):
            for i in range(6):
                staged=Image.open(BASE/f'frames/injury-ground-{d}/{i:03}.png').convert('RGBA');original=Image.open(north/f'frames/injury-ground-{d}/{i:03}.png').convert('RGBA');a=np.asarray(original);b=np.asarray(staged);white=(a[:,:,3]>0)&(a[:,:,:3].max(2)-a[:,:,:3].min(2)<12)&(a[:,:,:3].mean(2)>180)
                self.assertTrue(np.array_equal(a[white],b[white]));self.assertEqual(a[:,:,3].tobytes(),b[:,:,3].tobytes())
        self.assertNotIn('injury-ground-north',json.loads((BASE/'baseline-contract.json').read_text())['states'])

if __name__=='__main__':unittest.main()
