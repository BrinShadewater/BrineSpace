"""Keep original meal sources and all non-South selections unchanged."""
from pathlib import Path
import hashlib,json,sys,unittest
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from publish_marsh_gesture_review import selected,resolve

class Meals(unittest.TestCase):
    def test_originals_and_scope(self):
        current=selected()
        prior=json.loads((ROOT/'character/marsh-meal-review-2026-10-14/selected-before.json').read_text())
        changes=[]
        for key,old in prior.items():
            p,m,s=current[key]
            self.assertEqual({k:v for k,v in s.items() if k!='frameFiles'},{k:v for k,v in old['state'].items() if k!='frameFiles'})
            self.assertEqual({k:v for k,v in m.items() if k not in ['revision','states']},{k:v for k,v in old['metadata'].items() if k!='revision'})
            for i,f in enumerate(old['state']['frameFiles']):
                self.assertEqual(hashlib.sha256(resolve((ROOT/old['manifest']).parent,f).read_bytes()).hexdigest(),old['hashes'][i])
                if hashlib.sha256(resolve(p.parent,s['frameFiles'][i]).read_bytes()).hexdigest()!=old['hashes'][i]:changes.append((key,i))
        self.assertEqual(sorted(changes),sorted((key,i) for key in ['eat-south','drink-south'] for i in range(6)))

    def test_complete_generated_bodies(self):
        for p in (ROOT/'character/marsh-meal-polish-v1').glob('meal-body-*.png'):
            a=np.array(Image.open(p).convert('RGBA'));y,x=np.where(a[:,:,3]>160)
            self.assertEqual(a.shape,(184,184,4))
            self.assertEqual(int(y.max()),170)
            self.assertGreater(int(x.min()),0);self.assertLess(int(x.max()),183)
            self.assertGreater(len(x),3000)

if __name__=='__main__':unittest.main()
