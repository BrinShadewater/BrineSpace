"""Mining source preservation and tool/tread handoff contracts."""
from pathlib import Path
import hashlib,json,sys,unittest
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from publish_marsh_gesture_review import selected,resolve
from publish_marsh_remaining_review import registered
BASE=ROOT/'character/marsh-underwater-mining-v1'
class Mining(unittest.TestCase):
    def test_accepted_library_unchanged(self):
        d=selected();old=json.loads((BASE/'selected-before.json').read_text());self.assertEqual(len(d),len(old)+12)
        for key,r in old.items():
            p,m,s=d[key];self.assertEqual(s,r['state']);self.assertEqual({k:v for k,v in m.items() if k!='states'},r['metadata'])
            for f,prior in zip(s['frameFiles'],r['files']):self.assertEqual(hashlib.sha256(resolve(p.parent,f).read_bytes()).hexdigest(),prior['sha256'])
    def test_tool_handoffs(self):
        d=selected()
        for direction in ['north','south','east','west']:
            draw=d['water-mine-draw-'+direction];work=d['water-mine-'+direction];stow=d['water-mine-stow-'+direction]
            for a,i,b,j in [(d['tread-'+direction],0,draw,0),(draw,-1,work,0),(work,-1,work,0),(work,-1,stow,0),(stow,-1,d['swim-pickup-'+direction],0)]:self.assertEqual(registered(a,i).tobytes(),registered(b,j).tobytes())
            for r in [draw,work,stow]:
                p,m,s=r;self.assertEqual(m['standingHeight'],148);self.assertEqual(m['pivot'],[112,172])
                for f in s['frameFiles']:
                    with Image.open(resolve(p.parent,f)) as im:self.assertEqual(im.size,(224,208))
if __name__=='__main__':unittest.main()
