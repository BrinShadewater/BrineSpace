"""Protect bounded source restoration and shared walk-tone corrections."""
import hashlib,json,sys,unittest
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import label
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-consistency-v1'
sys.path.insert(0,str(ROOT/'tools'))
from repair_crew_consistency import selected,cloth,WEIGHTS

class Consistency(unittest.TestCase):
    def test_bounded_repairs_and_locked_hues(self):
        entries=json.loads((BASE/'mapping.json').read_text())
        for rel,e in entries.items():
            with self.subTest(file=rel):
                path=ROOT/rel
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),e['after'])
                a=np.array(Image.open(BASE/'originals'/rel).convert('RGBA'));b=np.array(Image.open(path).convert('RGBA'))
                self.assertEqual(a.shape,b.shape)
                if e['reason']=='authored collar restoration':
                    self.assertTrue(np.array_equal(a[a[:,:,3]>0],b[a[:,:,3]>0]))
                    changed=np.any(a!=b,axis=2);ys,xs=np.where(changed)
                    self.assertLessEqual(ys.max()-ys.min(),3,'Only the four erased collar rows may change')
                    self.assertTrue(np.all(b[changed,3]==255))
                    labels,_=label(b[:,:,3]>0)
                    self.assertEqual(len(set(labels[changed])) ,1,'Restored collar must form one connected body')
                    connected=labels[ys[0],xs[0]]
                    self.assertGreater((labels==connected).sum(),1000)
                else:
                    self.assertTrue(np.array_equal(a[:,:,3],b[:,:,3]))
                    actor=rel.split('/')[1];name='veld' if actor=='dr-veld-v2' else 'branforth'
                    pal=json.loads((ROOT/'character/palette-standard-v1/palettes'/f'{name}.json').read_text())
                    ramp={tuple(c) for c in pal['neutralRamp']}
                    changed=np.any(a!=b,axis=2)
                    self.assertTrue(all(tuple(c) in ramp for c in b[changed,:3]),'All corrected cloth shades must come from the locked ramp')
                    self.assertTrue(np.array_equal(a[a[:,:,3]==0],b[a[:,:,3]==0]))

    def test_walk_tone_matches_reference(self):
        for actor in ['veld','branforth']:
            rows,_=selected(actor);values={}
            for action in ['idle','walk']:
                samples=[]
                for direction in ['east','west','south','north']:
                    for rel in rows['body/'+action+'-'+direction]:
                        im=Image.open(ROOT/rel).convert('RGBA');a,mask=cloth(im,actor,im.getbbox()[1]+30)
                        samples.extend((a[mask,:3]@WEIGHTS).tolist())
                values[action]=np.quantile(samples,[.1,.5,.9])
            self.assertTrue(np.all(np.abs(values['idle']-values['walk'])<3),(actor,values))

if __name__=='__main__':unittest.main()
