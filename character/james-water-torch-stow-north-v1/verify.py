from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;checks=[]
def check(ok,message):checks.append({'passed':bool(ok),'check':message})
m=json.loads((P/'helmet-manifest.json').read_text());reg=json.loads((P/'registration.json').read_text());st=m['states'][0]
check(m['pivot']==[128,128] and m['standingHeight']==148,'Selected water density and pivot preserved')
check(reg['fixedScale']==.28,'One recorded physical ruler for all authored poses')
check(hashlib.sha256((P/'source.png').read_bytes()).hexdigest()==reg['sourceSha256'],'Raw generated source provenance')
check(sum(st['frameDurationsMs'])==400 and not st['loop'],'Finite400ms stow')
check(all(st['waterPoses']),'Every whole source pose remains prone water')
refs=[np.array(Image.open(P.parent/'james-water-cargo-north-v1/frames/helmet/salvage/003.png').convert('RGBA')),np.array(Image.open(P.parent/'james-water-north-v1/frames/helmet/swim/000.png').convert('RGBA'))]
rows=[np.array(Image.open(P/f).convert('RGBA')) for f in st['frameFiles']]
check(np.array_equal(rows[0],refs[0]),'Exact actual extraction source3 entrance')
check(np.array_equal(rows[-1],refs[-1]),'Exact selected empty swim0 terminal')
def metrics(a):
 r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);neutral=(a[:,:,3]>180)&(abs(r-g)<12)&(abs(g-b)<15)&(r>20)&(r<150);h=np.zeros(neutral.shape,bool);h[92:128,110:148]=True
 yy,xx=np.where((a[:,:,3]>180)&h)
 face=np.zeros(h.shape,bool);face[139:153,120:137]=True;skin=face&(a[:,:,3]>180)&(r-g>14)&(g-b>12)&(r>60)&(b<160)
 return {'bodyMedian':np.median(a[:,:,:3][neutral & ~h],axis=0).tolist(),'helmetMedian':np.median(a[:,:,:3][neutral & h],axis=0).tolist(),'helmetCrown':int(yy.min()),'helmetWidth':int(xx.max()-xx.min()+1),'helmetHeight':int(yy.max()-yy.min()+1)}
masters=[metrics(a) for a in refs];records=[]
for i,a in enumerate(rows):
 rec=metrics(a);rec['index']=i;records.append(rec)
 check(a.shape==(276,256,4),'Whole source canvas '+str(i))
 check(not np.any(a[0,:,3]) and not np.any(a[-1,:,3]) and not np.any(a[:,0,3]) and not np.any(a[:,-1,3]),'No clipped alpha '+str(i))
 check(abs(rec['helmetCrown']-masters[0]['helmetCrown'])<=3,'Stable helmet crown '+str(i))
 check(abs(rec['helmetWidth']-masters[0]['helmetWidth'])<=4 and abs(rec['helmetHeight']-masters[0]['helmetHeight'])<=4,'Independent helmet proportion band '+str(i))
 for key in ['bodyMedian','helmetMedian']:
  values=np.array([x[key] for x in masters]);margin=10 if key=='faceMedian' else 7;check(np.all(np.array(rec[key])>=values.min(axis=0)-margin) and np.all(np.array(rec[key])<=values.max(axis=0)+margin),'Selected material '+key+' '+str(i))
report={'checks':len(checks),'failures':sum(not x['passed'] for x in checks),'records':records,'masters':masters,'results':checks,'scope':'Selected source fit/material/density and exact whole endpoints; no controller installation, saved cancellation clock or arbitrary source entrance certification.'}
(P/'fit-evidence.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'checks':report['checks'],'failures':report['failures'],'failed':[x['check'] for x in checks if not x['passed']]}));raise SystemExit(bool(report['failures']))
