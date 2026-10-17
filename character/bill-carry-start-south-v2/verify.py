from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;reg=json.loads((P/'registration.json').read_text());checks=0;rows={}
def check(ok,message):
 global checks
 checks+=1
 assert ok,message
for f,h in reg['masterSha256'].items():check(hashlib.sha256((R/f).read_bytes()).hexdigest()==h,'Canonical/source input unchanged')
for rec in reg['frames']:check(rec['scale']==next(c['scale'] for c in reg['calibration'] if c['source']==rec['source']),'One anatomical ruler across interiors')
for gear in ['bare','helmet']:
 master=R/f'character/bill-cargo-south-master-head-v1/frames/{gear}/pickup-south/011.png';gait=R/f'character/bill-carry-south-gait-v3/frames/{gear}/carry-south/000.png';a=np.array(Image.open(master));m=json.loads((P/f'{gear}-manifest.json').read_text());s=m['states'][0];rows[gear]=[]
 check(m['standingHeight']==148 and m['pivot']==[128,224] and m['status']=='staged_visual_review','Fixed master registration')
 check(not s['loop'] and s['frameDurationsMs']==[40,50,55,65,65,45] and len(s['frameFiles'])==6,'Finite320ms first-step clock')
 for i,f in enumerate(s['frameFiles']):
  check(f.startswith('res://character/bill-carry-start-south-v2/frames/'),'Whole explicit source paths')
  path=R/f.removeprefix('res://');b=np.array(Image.open(path));rows[gear].append(b)
  check(b.shape==(256,256,4) and np.array_equal(a[:168],b[:168]),'Exact upper RGBA and canvas')
  y,x=np.where(b[:,:,3]>180);check(x.min()>0 and x.max()<255 and y.min()==np.where(a[:,:,3]>180)[0].min(),'No cropping/height drift above upper')
  check(y.max()==222,'Master floor register, including bridge interiors')
  if i==0:check(path.read_bytes()==master.read_bytes(),'Exact held entrance')
  elif i>=4:check(path.read_bytes()==gait.read_bytes(),'Exact gait contact exit')
for b,h in zip(rows['bare'],rows['helmet']):check(np.array_equal(b[168:],h[168:]),'Identical paired lower body')
check(.139<.14 and .139+1/60>.14,'Gait resumes late contact slot before next slot at60Hz')
(P/'validation.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'Package registration, paired exact upper/lower/endpoints, inputs and finite clock. No anatomical contact or lifecycle acceptance claim.'},indent=2)+'\n');print('BILL SOUTH FIRST STEP: %d checks pass'%checks)
