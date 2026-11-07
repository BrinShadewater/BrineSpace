"""Narrow current catalog scope and full generated seated-body registration."""
from pathlib import Path
import json,hashlib,unittest
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def resolve(parent,f):return ROOT/f[6:] if f.startswith('res://') else (parent/f).resolve()
def selected():
    c=ROOT/'character/marsh-v2/catalog.json';result={}
    for rel in json.loads(c.read_text())['body']:
        p=(c.parent/rel).resolve();m=json.loads(p.read_text())
        for s in m['states']:result[s['id']]=(p,m,s)
    return result
class Rest(unittest.TestCase):
    def test_contract_and_original_sources(self):
        d=selected();before=json.loads((ROOT/'character/marsh-rest-review-2026-10-14/selected-before.json').read_text());changes=[]
        for key,prior in before.items():
            p,m,s=d[key]
            self.assertEqual({k:v for k,v in s.items() if k!='frameFiles'},{k:v for k,v in prior['state'].items() if k!='frameFiles'})
            self.assertEqual({k:v for k,v in m.items() if k not in ['states','revision']},{k:v for k,v in prior['metadata'].items() if k!='revision'})
            for i,old in enumerate(prior['files']):
                self.assertEqual(hashlib.sha256((ROOT/old['path']).read_bytes()).hexdigest(),old['sha256'])
                if hashlib.sha256(resolve(p.parent,s['frameFiles'][i]).read_bytes()).hexdigest()!=old['sha256']:changes.append((key,i))
        expected=[]
        for key in ['sit-down-south','sit-idle-south','read-seated-south','sit-rise-south']:
            expected.extend((key,i) for i in range(len(d[key][2]['frameFiles'])))
        expected.extend([('lie-down-south',0),('get-up-south',3)])
        self.assertEqual(sorted(changes),sorted(expected))
    def test_complete_seated_bodies_and_joins(self):
        d=selected();p,m,s=d['idle-south'];idle=Image.open(resolve(p.parent,s['frameFiles'][0])).convert('RGBA').tobytes()
        for key,slot in [('sit-down-south',0),('sit-rise-south',3),('lie-down-south',0),('get-up-south',3)]:
            p,m,s=d[key];self.assertEqual(Image.open(resolve(p.parent,s['frameFiles'][slot])).convert('RGBA').tobytes(),idle)
        for p in (ROOT/'character/marsh-rest-polish-v1').glob('seated-body-*.png'):
            a=np.array(Image.open(p).convert('RGBA'));mask=a[:,:,3]>160;y,x=np.where(mask)
            self.assertEqual(a.shape,(184,184,4));self.assertEqual(int(y.max()),170)
            self.assertGreater(int(mask.sum()),2800);self.assertGreater(int(mask[140:].sum()),200)
            self.assertGreater(int(x.min()),0);self.assertLess(int(x.max()),183)
if __name__=='__main__':unittest.main()
