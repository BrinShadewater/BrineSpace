from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;old=P/'revisions/material-v3';checks=[]
def check(ok,label):checks.append({'passed':bool(ok),'check':label})
metrics=[]
for i in range(7):
    f=P/f'frames/bare/{i:03}.png';before=np.array(Image.open(old/f'frames/bare/{i:03}.png'));after=np.array(Image.open(f))
    check(np.array_equal(before[:,:,3],after[:,:,3]),'Exact preserved alpha/geometry '+str(i))
    changed=(before[:,:,:3]!=after[:,:,:3]).any(2)
    check(not changed.any() if i in [0,6] else changed.any(),'Unchanged exact donor' if i in [0,6] else 'Interior palette corrected '+str(i))
    mask=after[:,:,3]>180;y,x=np.where(mask)
    metrics.append({'frame':i,'changedRGBPixels':int(changed.sum()),'crown':int(y.min()),'sole':int(y.max()),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
new=json.loads((P/'registration.json').read_text());prior=json.loads((old/'registration.json').read_text())
check(new['frames']==prior['frames'] and new['sources']==prior['sources'],'Exact fixed source rulers/registration')
check(json.loads((P/'manifest.json').read_text())==json.loads((old/'manifest.json').read_text()),'Exact state metadata/timing/reverse refs')
c=new['grades']['primary']['boundedMaterialCorrection']
check(all(a<=b for a,b in zip(c['hardwareOutput'],c['hardwareOutput'][1:])),'Monotonic hardware palette curve')
result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks,'metrics':metrics,'scope':'bounded RGB correction preserving alpha, geometry, timing and exact donors; visual identity acceptance separate'}
(P/'material-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':result['passed'],'checks':len(checks),'metrics':[{k:r[k] for k in ['frame','changedRGBPixels','crown','sole']} for r in metrics]}));raise SystemExit(0 if result['passed'] else 1)
