from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;checks=[]
def check(ok,why):checks.append({'passed':bool(ok),'check':why})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((P/'registration.json').read_text());cfg=json.loads((P/'source-rulers.json').read_text())
for key,spec in r['sources'].items():check(sha(P/spec['source'])==r['sourcesSha256'][key],'Raw source binding '+key)
check(r['sources']==cfg['sources'] and r['sequence']==cfg['sequence'],'Frozen source rulers and explicit interior selection')
component=r['helmetComponent'];check(sha(P.parent/component['path'])==component['sha256'],'Native helmet source binding')
check(max(row['headAxis'][1] for row in r['frames'])-min(row['headAxis'][1] for row in r['frames'])<=3,'Interior standing crown range <=3px')
check(len(r['frames'])==4 and len({(row['source'],row['sourcePose']) for row in r['frames']})==4,'Four authored interior poses')
for file,digest in json.loads((P/'frame-hashes.json').read_text()).items():check(sha(P/file)==digest,'Frame binding '+file)
for gear in ['bare','helmet']:
 m=json.loads((P/(gear+'-manifest.json')).read_text());enter,exit=m['states'];check(m['pivot']==[128,224] and m['standingHeight']==148 and m['precomposed'],gear+' shared figure plane')
 check(exit['frameFiles']==enter['frameFiles'][::-1] and exit['frameDurationsMs']==enter['frameDurationsMs'][::-1],gear+' Exact reverse stow')
 check(sum(enter['frameDurationsMs'])==480 and not enter['loop'] and not exit['loop'] and enter['depthOffsets']==[0]*6,gear+' finite480ms standing')
 for donor,index in zip(r['donors'][gear],[0,-1]):
  path=P.parent/donor['path'];check(sha(path)==donor['sha256'],'Endpoint source binding '+gear)
  check(Image.open(P/enter['frameFiles'][index]).convert('RGBA').tobytes()==Image.open(path).convert('RGBA').tobytes(),'Exact idle/held join '+gear)
 for file in enter['frameFiles']:
  a=np.array(Image.open(P/file));y,x=np.where(a[:,:,3]>180);check(a.shape==(256,256,4) and y.max()==223 and x.min()>0 and x.max()<255,'Planted sole and contained figure '+gear)
for row in r['frames']:
 i=row['frame'];limit=row['protectedBodyFromY'];a=np.array(Image.open(P/f'frames/bare/{i:03}.png'));b=np.array(Image.open(P/f'frames/helmet/{i:03}.png'));check(np.array_equal(a[limit:],b[limit:]),'Original body protected under native helmet')
import importlib.util
spec=importlib.util.spec_from_file_location('face',P.parent/'bill-inspect-west-coherent-v1/audit_face.py');face=importlib.util.module_from_spec(spec);spec.loader.exec_module(face)
master=face.samples(Image.open(P.parent/r['donors']['bare'][0]['path']),[128,76])
check(r.get('nativeFaceGain')==[1.08,1.02,1.07],'Same bounded skin correction as held endpoint')
for row in r['frames']:
 i=row['frame'];a=np.array(Image.open(P/f'frames/bare/{i:03}.png'));old=np.array(Image.open(P/f'prior-face-grade-v1/frames/bare/{i:03}.png'));y,x=np.indices(a.shape[:2]);hx,hy=row['headAxis'];band=(x<hx)&(x>hx-14)&(y>=hy+7)&(y<hy+22)
 check(np.array_equal(a[~band],old[~band]) and np.array_equal(a[:,:,3],old[:,:,3]),'Geometry/body outside skin correction unchanged')
 check(Image.open(P/f'frames/helmet/{i:03}.png').tobytes()==Image.open(P/f'prior-face-grade-v1/frames/helmet/{i:03}.png').tobytes(),'Native helmet pixels unchanged by face correction')
 skin=face.samples(Image.fromarray(a),row['headAxis']);check(np.max(np.abs(np.array(skin['medianRGB'])-master['medianRGB']))<=12,'Bare skin median near selected master')
result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks,'scope':'candidate source/join verification; no normal actor activity proof'};(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'checks':len(checks)}));raise SystemExit(0 if result['passed'] else 1)
