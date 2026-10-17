from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;checks=0;rows={}
def check(ok,msg):
 global checks
 checks+=1
 assert ok,msg
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text());s=m['states'][0];master=np.array(Image.open(R/f'character/bill-cargo-south-master-head-v1/frames/{gear}/pickup-south/011.png'));rows[gear]=[]
 check(m['standingHeight']==148 and m['pivot']==[128,224] and m['status']=='staged_visual_review','Fixed master contract')
 check(s['loop'] and s['frameDurationsMs']==[140]*6 and m['strideDistanceCells']['carry']==.12,'Original cadence/stride')
 for i,f in enumerate(s['frameFiles']):
  path=R/f.removeprefix('res://');a=np.array(Image.open(path));rows[gear].append(a);check(np.array_equal(a[:168],master[:168]),'Exact master upper');y,x=np.where(a[:,:,3]>180);check(222<=y.max()<=224,'Single-ruler grounded sole')
  if i!=4:check(path.read_bytes()==(R/f'character/bill-carry-south-gait-v1/frames/{gear}/carry-south/{i:03}.png').read_bytes(),'Other5slots byte unchanged')
for a,h in zip(rows['bare'],rows['helmet']):check(np.array_equal(a[168:],h[168:]),'Paired exact legs')
def lift(a):
 y,x=np.indices(a.shape[:2]);l=np.where((a[:,:,3]>180)&(y>=190)&(x<128))[0];rr=np.where((a[:,:,3]>180)&(y>=190)&(x>=128))[0];return int(rr.max()-l.max())
old=lift(np.array(Image.open(R/'character/bill-carry-south-gait-v1/frames/bare/carry-south/004.png')));new=lift(rows['bare'][4]);check(0<new<old,'Authored passing foot lowers rather than stretching old limb')
(P/'validation.json').write_text(json.dumps({'checks':checks,'passed':True,'oldPassingFootLiftPixels':old,'newPassingFootLiftPixels':new,'scope':'Exact other5slots/master upper/paired legs/fixed clock and discrete lift metric; not contact or full smoothness certification'},indent=2)+'\n');print('BILL SOUTH GAIT LOW PASS:',checks,'checks; lift',old,'->',new)
