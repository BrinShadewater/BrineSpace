from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent.parent.parent;checks=0
def check(ok,msg):
 global checks
 checks+=1
 assert ok,msg
for bank,state,expected_rows,durations in [('bill-carry-east-gait-v3','carry-east',8,[105]*8),('bill-carry-start-east-v4','carry-start-east',6,[40,50,55,65,65,45])]:
 P=R/'character'/bank;reg=json.loads((P/'registration.json').read_text());paired={}
 for f,h in reg['sourceSha256'].items():check(hashlib.sha256((R/f.removeprefix('res://')).read_bytes()).hexdigest()==h,'Original inputs unchanged')
 for gear in ['bare','helmet']:
  m=json.loads((P/f'{gear}-manifest.json').read_text());s=m['states'][0];paired[gear]=[]
  check(m['standingHeight']==148 and m['pivot']==[128,224] and m['status']=='staged_visual_review','Metadata unchanged')
  check(len(s['frameFiles'])==expected_rows and s['frameDurationsMs']==durations,'Original clock and rows')
  for i,f in enumerate(s['frameFiles']):
   rec=next(r for r in reg['frames'] if r['gear']==gear and r['row']==i);src=Image.open(R/rec['source'].removeprefix('res://')).convert('RGBA');out=Image.open(R/f.removeprefix('res://')).convert('RGBA');a=np.array(out);paired[gear].append(a);expected=Image.new('RGBA',(256,256));expected.alpha_composite(src,tuple(rec['wholeFigureTranslation']))
   check(np.array_equal(a,np.array(expected)),'Only rigid RGBA translation')
   check(np.count_nonzero(a[:,:,3])==np.count_nonzero(np.array(src)[:,:,3]),'No visible source loss')
   check(int(np.where(a[:,:,3]>180)[0].max())==223,'Exact opaque directional master sole')
   if state=='carry-start-east' and i>=4:check((R/f.removeprefix('res://')).read_bytes()==(R/f'character/bill-carry-east-gait-v3/frames/{gear}/carry-east/000.png').read_bytes(),'Byte-identical contact exit')
 for b,h in zip(paired['bare'],paired['helmet']):check(np.array_equal(b[170:],h[170:]),'Paired identical moving lower body')
 (P/'validation.json').write_text(json.dumps({'passed':True,'scope':'Rigid pixel-preserving floor registration, original inputs/timing and paired endpoints','checksCumulative':checks},indent=2)+'\n')
print('EAST FLOOR REGISTRATION:',checks,'checks pass')
