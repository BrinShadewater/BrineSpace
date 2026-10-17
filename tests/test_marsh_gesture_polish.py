"""Selected gesture joins, whole-body extraction and narrowly preserved library contract."""
from pathlib import Path
import hashlib
import json
import unittest
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def resolve(parent,f):return ROOT/f[6:] if f.startswith('res://') else (parent/f).resolve()


def selected():
    c=ROOT/'character/marsh-v2/catalog.json';out={}
    for rel in json.loads(c.read_text())['body']:
        p=(c.parent/rel).resolve();m=json.loads(p.read_text())
        for s in m['states']:out[s['id']]=(p,m,s)
    return out


class Gestures(unittest.TestCase):
    def test_exact_selected_idle_holds(self):
        d=selected()
        for direction in ['east','west','north','south']:
            p,m,s=d['crew-chat-'+direction];q,n,idle=d['idle-'+direction]
            reference=Image.open(resolve(q.parent,idle['frameFiles'][0])).convert('RGBA')
            for slot in [0,1,6,7]:
                with self.subTest(direction=direction,slot=slot):
                    self.assertEqual(Image.open(resolve(p.parent,s['frameFiles'][slot])).convert('RGBA').tobytes(),reference.tobytes())

    def test_preserved_scope_and_whole_pose_registration(self):
        d=selected();records=json.loads((ROOT/'character/marsh-gestures-review-2026-10-14/selected-before.json').read_text());changes=[]
        for key,prior in records.items():
            p,m,s=d[key]
            self.assertEqual({k:v for k,v in s.items() if k!='frameFiles'},{k:v for k,v in prior['state'].items() if k!='frameFiles'})
            self.assertEqual({k:v for k,v in m.items() if k not in ['states','revision']},{k:v for k,v in prior['metadata'].items() if k!='revision'})
            for slot,old in enumerate(prior['files']):
                self.assertEqual(hashlib.sha256((ROOT/old['path']).read_bytes()).hexdigest(),old['sha256'])
                if hashlib.sha256(resolve(p.parent,s['frameFiles'][slot]).read_bytes()).hexdigest()!=old['sha256']:changes.append((key,slot))
        self.assertEqual(changes,[('crew-chat-south',i) for i in range(8)])
        p,m,s=d['crew-chat-south'];neutral=np.array(Image.open(resolve(p.parent,s['frameFiles'][0])).convert('RGBA'))
        for slot in [2,3,4,5]:
            a=np.array(Image.open(resolve(p.parent,s['frameFiles'][slot])).convert('RGBA'))
            self.assertEqual(a.shape,neutral.shape)
            mask=a[:,:,3]>160;yy,xx=np.where(mask)
            self.assertEqual(int(yy.max()),170,'planted sole follows canonical sampled edge')
            self.assertLessEqual(abs(int(yy.min())-24),1)
            self.assertGreater(int(mask.sum()),int((neutral[:,:,3]>160).sum())*.85)
            self.assertGreater(int(mask[140:].sum()),100,'complete lower body retained')


if __name__=='__main__':unittest.main()
