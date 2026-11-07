"""Preserve accepted sources and prove exact new water action handoffs."""
from pathlib import Path
import hashlib,json,sys,unittest
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from publish_marsh_gesture_review import selected,resolve
BASE=ROOT/'character/marsh-water-actions-v1'
def pose(record,i):
    p,m,s=record;im=Image.open(resolve(p.parent,s['frameFiles'][i])).convert('RGBA');out=Image.new('RGBA',(224,208));out.paste(im,(112-round(m['pivot'][0]),172-round(m['pivot'][1])));return out.tobytes()
class WaterActions(unittest.TestCase):
    def test_selection_preservation(self):
        before=json.loads((BASE/'selected-before.json').read_text());current=selected();changes=[]
        self.assertEqual(len(current),len(before)+16)
        for key,old in before.items():
            p,m,s=current[key]
            self.assertEqual({k:v for k,v in s.items() if k!='frameFiles'},{k:v for k,v in old['state'].items() if k!='frameFiles'})
            for i,original in enumerate(old['files']):
                self.assertEqual(hashlib.sha256((ROOT/original['path']).read_bytes()).hexdigest(),original['sha256'])
                if hashlib.sha256(resolve(p.parent,s['frameFiles'][i]).read_bytes()).hexdigest()!=original['sha256']:changes.append((key,i))
        self.assertEqual(sorted(changes),sorted(('swim-pickup-'+d,0) for d in ['north','east','south','west']))
    def test_shared_endpoints_and_reversal(self):
        d=selected()
        for direction in ['north','east','south','west']:
            lift=d['water-lift-'+direction];settle=d['water-settle-'+direction];work=d['water-salvage-'+direction];entry=d['water-salvage-enter-'+direction]
            for a,i,b,j in [(lift,0,d['idle-'+direction],0),(lift,-1,d['tread-'+direction],0),(settle,-1,d['idle-'+direction],0),(entry,0,d['swim-'+direction],0),(entry,-1,work,0),(work,-1,d['swim-pickup-'+direction],0),(d['swim-pickup-'+direction],-1,d['swim-carry-'+direction],0)]:self.assertEqual(pose(a,i),pose(b,j))
            for i in range(4):self.assertEqual(pose(lift,i),pose(settle,3-i))
            self.assertEqual(work[2]['frameDurationsMs'],[150]*6)
    def test_bodies_and_clocks(self):
        d=selected()
        for key in [k for k in d if k.startswith(('water-lift-','water-settle-','water-salvage-'))]:
            p,m,s=d[key];self.assertEqual(m['standingHeight'],148);self.assertEqual(m['pivot'],[112,172])
            self.assertEqual(len(s['frameFiles']),len(s['frameDurationsMs']))
            for f in s['frameFiles']:
                im=Image.open(resolve(p.parent,f)).convert('RGBA');self.assertEqual(im.size,(224,208));self.assertTrue(im.getbbox())
if __name__=='__main__':unittest.main()
