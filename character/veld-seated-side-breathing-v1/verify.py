from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
checks=0;pairs={};bound=[]
def check(ok,why):
 global checks
 assert ok,why
 checks+=1
reg=json.loads((P/'registration.json').read_text(encoding='utf-8'))
for name,h in reg['sourceBindings'].items():
 check(hashlib.sha256((P.parents[1]/name).read_bytes()).hexdigest()==h,'immutable neutral source')
check(reg['amplitudePx']<.4,'measured subtle North amplitude')
for gear in ('bare','helmet'):
 m=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'));bound.append(P/f'{gear}-manifest.json')
 check(m['pivot']==[128,224] and m['standingHeight']==148,'fixed master ruler')
 check(len(m['states'])==2,'independent side coverage')
 for state in m['states']:
  direction=state['id'].split('-')[-1]
  base=P.parent/f'veld-seated-{direction}-coherent-v1'
  neutral=np.array(Image.open(base/f'frames/{gear}/sit-down-{direction}/005.png'))
  mask_source=np.array(Image.open(base/f'frames/bare/sit-down-{direction}/005.png'))
  yy,xx=np.indices((256,256));low,high=(85,104) if direction=='east' else (150,174)
  rgb=mask_source[:,:,:3].astype(float)
  blue=(rgb[:,:,2]>rgb[:,:,0]*1.15)&(rgb[:,:,2]>rgb[:,:,1]*1.05)
  allowed=(yy>149)&(yy<163)&(xx>low)&(xx<high)&~blue
  check(state['loop'] and state['frameDurationsMs']==[600]*6,'3.6-second loop clock')
  check(state['seatContactDepth'] and state['depthOffsets']==[0]*6,'contact marker without invented depth')
  arrays=[]
  for f in state['frameFiles']:
   p=P/f;bound.append(p);im=Image.open(p);a=np.array(im);arrays.append(a)
   check(im.mode=='RGBA' and im.size==(256,256),'native RGBA')
   check(np.array_equal(a[~allowed],neutral[~allowed]),'protected exact RGBA')
   check(np.array_equal(a[:150],neutral[:150]),'master head/helmet/collar/chest/badge unchanged')
   check(np.array_equal(a[163:],neutral[163:]),'cuffs/hands/belt/hip/knees/boots unchanged')
   check(not np.any(a[[0,-1],:,3]) and not np.any(a[:,[0,-1],3]),'no edge clipping')
  check(np.array_equal(arrays[0],neutral) and np.array_equal(arrays[-1],neutral),'exact neutral cycle seam')
  base_manifest=json.loads((base/f'{gear}-manifest.json').read_text(encoding='utf-8'))
  rise_state=next(s for s in base_manifest['states'] if s['id']==f'sit-rise-{direction}')
  rise=np.array(Image.open(base/rise_state['frameFiles'][0]))
  check(np.array_equal(arrays[0],rise),'exact rise/down join')
  check(len({a.tobytes() for a in arrays})==5,'four distinct interior phases')
  pairs[gear,direction]=arrays
for direction in ('east','west'):
 for a,b in zip(pairs['bare',direction],pairs['helmet',direction]):
  check(np.array_equal(a[145:],b[145:]),'paired body/motion below inherited collar extent exact')
bound.extend([P/'registration.json',P/'contact.png'])
bound.extend(P/f'{g}-{d}-breathing.gif' for g in ('bare','helmet') for d in ('east','west'))
def hashes():return {p.relative_to(P).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in bound}
before=hashes()
subprocess.run([sys.executable,str(P/'build.py')],check=True,capture_output=True)
check(before==hashes(),'deterministic packaging')
(P/'verification.json').write_text(json.dumps({'checks':checks,'failures':0,'boundFiles':len(before),'hashes':before,'normalSelection':False,'scope':'source fidelity, independent side coverage, exact paired body/neutral joins, measured local amplitude, fixed grade/ruler; native contact and service not certified'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'boundFiles':len(before)}))
