from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;checks=[]
def check(ok,why):checks.append({'passed':bool(ok),'check':why})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((P/'registration.json').read_text(encoding='utf-8'));check(sha(P/'sources/entry-v1.png')==r['sourceSha256'],'raw source binding');check(r['fixedRuler']==[.214,.251],'fixed source ruler')
check(sha(P/'sources/entry-right-arm-v2.png')==r['correctedSourceSha256'],'Corrected right-arm source binding')
check(r['correctedOpaqueThreshold']==240 and r['correctedRuler']==[.214,.2455],'Frozen edited source extraction/ruler')
check(r['frames'][0]['source']=='entry-right-arm-v2.png' and all(row['source']=='entry-v1.png' for row in r['frames'][1:]),'Only corrected arm cell selected from edit')
for file,digest in json.loads((P/'frame-hashes.json').read_text(encoding='utf-8')).items():check(sha(P/file)==digest,'frame binding '+file)
for gear,folder in [('bare','bill-seated-north-coherent-v1'),('helmet','bill-seated-helmet-north-coherent-v1')]:
 m=json.loads((P/(gear+'-manifest.json')).read_text(encoding='utf-8'));enter,exit=m['states'];check(m['pivot']==[128,224] and m['standingHeight']==148,gear+' shared figure plane');check(exit['frameFiles']==enter['frameFiles'][::-1] and exit['frameDurationsMs']==enter['frameDurationsMs'][::-1],gear+' exact reversed exit');check(sum(enter['frameDurationsMs'])==480 and not enter['loop'] and not exit['loop'],gear+' finite480ms')
 first=Image.open(P/enter['frameFiles'][0]).convert('RGBA');last=Image.open(P/enter['frameFiles'][-1]).convert('RGBA');check(first.tobytes()==Image.open(P.parent/folder/'frames/sit-down-north/005.png').convert('RGBA').tobytes(),gear+' exact seated join');check(last.tobytes()==Image.open(P.parent/'bill-reading-north-v1'/f'frames/{gear}/000.png').convert('RGBA').tobytes(),gear+' exact reading join')
 for f in enter['frameFiles']:
  a=np.array(Image.open(P/f));y,x=np.where(a[:,:,3]>180);check(y.max()==222 and x.min()>0 and x.max()<255,gear+' planted local boots/contained art')
for row in r['frames']:
 i=row['frame'];sy=row['protectedBodyFromY'];a=np.array(Image.open(P/f'frames/bare/{i:03}.png'));b=np.array(Image.open(P/f'frames/helmet/{i:03}.png'));check(np.array_equal(a[sy:],b[sy:]),'body preserved below helmet')
result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks};(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'checks':len(checks)}));raise SystemExit(0 if result['passed'] else 1)
