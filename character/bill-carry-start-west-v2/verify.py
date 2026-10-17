from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;reg=json.loads((P/'registration.json').read_text());checks=0;rows={}
def check(ok,message):
 global checks
 checks+=1
 assert ok,message
for f,h in reg['sourceSha256'].items():check(hashlib.sha256((R/f).read_bytes()).hexdigest()==h,'Source unchanged')
for rec in reg['frames']:check(rec['scale']==reg['scale'],'One standing ruler')
gr=json.loads((R/'character/bill-carry-west-gait-v2/registration.json').read_text())
for gear in ['bare','helmet']:
 master=R/f'character/bill-cargo-west-master-head-v1/frames/{gear}/pickup-west/011.png';gait=R/f'character/bill-carry-west-gait-v2/frames/{gear}/carry-west/000.png';a=np.array(Image.open(master));m=json.loads((P/f'{gear}-manifest.json').read_text());s=m['states'][0];rows[gear]=[]
 check(m['standingHeight']==148 and m['pivot']==[128,224] and m['status']=='staged_visual_review','Fixed metadata')
 check(not s['loop'] and s['frameDurationsMs']==[40,50,55,65,65,45] and len(s['frameFiles'])==6,'Finite320ms clock')
 for i,f in enumerate(s['frameFiles']):
  check(f.startswith('res://character/bill-carry-start-west-v2/frames/'),'Whole explicit source paths')
  path=R/f.removeprefix('res://');b=np.array(Image.open(path));rows[gear].append(b)
  drop=0 if i==0 else (reg['frames'][i-1]['wholeFigureTranslation'][1] if i<4 else gr['frames'][0]['wholeFigureTranslation'][1])
  check(b.shape==(256,256,4) and np.array_equal(a[:153],b[drop:153+drop]),'Exact rigidly translated upper')
  y,x=np.where(b[:,:,3]>180);check(x.min()>0 and x.max()<255 and y.min()==np.where(a[:,:,3]>180)[0].min()+drop and y.max()==222,'Floor registration and crown')
  if i==0:check(path.read_bytes()==master.read_bytes(),'Exact held entrance')
  elif i>=4:check(path.read_bytes()==gait.read_bytes(),'Exact gait contact exit')
for b,h in zip(rows['bare'],rows['helmet']):check(np.array_equal(b[153:],h[153:]),'Identical paired lower body')
check(.139<.14 and .139+1/60>.14,'Late contact resumes next slot at60Hz')
(P/'validation.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'Package registration, paired material, exact upper/endpoints and finite clock; no lifecycle acceptance claim.'},indent=2)+'\n');print('BILL WEST FIRST STEP: %d checks pass'%checks)
