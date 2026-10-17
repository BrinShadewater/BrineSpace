from pathlib import Path
import json,hashlib,subprocess,sys
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=[]
def check(ok,why):checks.append({'passed':bool(ok),'check':why})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ground(path):
    out=Image.new('RGBA',(256,256));out.alpha_composite(Image.open(path).convert('RGBA'),(36,52));return np.array(out)
r=json.loads((P/'registration.json').read_text());hashes=json.loads((P/'frame-hashes.json').read_text())
check(sha(P/'sources/death-v1.png')==r['sourceSha256'],'Bound authored source')
check(abs(r['fixedRuler']-148/494)<1e-12,'One standing-derived isotropic ruler for every pose')
for gear in ['bare','helmet']:
    m=json.loads((P/f'{gear}-manifest.json').read_text());s=m['states'][0]
    check(m['pivot']==[128,224] and m['standingHeight']==148 and m['frameWidth']==256 and m['frameHeight']==256,'Shared dry plane '+gear)
    check(s['frameDurationsMs']==[180,160,180,180,220,500] and not s['loop'] and s['terminalFrame']==5,'Original1420ms and finite terminal '+gear)
    authority=R/r[gear+'Idle'];check(sha(authority)==r[gear+'IdleSha256'],'Current selected master bound '+gear)
    frames=[np.array(Image.open(P/f)) for f in s['frameFiles']]
    check(np.array_equal(frames[0],ground(authority)),'Exact selected whole idle entry '+gear)
    check(s['waterPoses']==[False]*6 and s['waterKinds']==['death-ground']*6 and s['facings']==['east']*6 and s['depthOffsets']==[0]*6,'Dry camera metadata '+gear)
    crowns=[]
    for i,(f,a) in enumerate(zip(s['frameFiles'],frames)):
        y,x=np.where(a[:,:,3]>180);crowns.append(int(y.min()))
        check(a.shape==(256,256,4) and min(x.min(),y.min())>0 and max(x.max(),y.max())<255,'Unclipped whole source pose '+gear+str(i))
        check(abs(int(y.max())-223)<=1,'Actual dry floor contact '+gear+str(i))
        check(sha(P/f)==hashes[f],'Bound exported pixels '+gear+str(i))
    check(all(a<b for a,b in zip(crowns,crowns[1:])),'Authored lowering without standing height normalization '+gear)
    if gear=='helmet':
        for i,row in enumerate(r['frames'],1):
            a=frames[i];b=np.array(Image.open(P/f'frames/bare/death-ground-east/{i:03}.png'));yy,xx=np.indices(a.shape[:2]);c=row['headCenter'];allowed=(xx-c[0])**2+(yy-c[1])**2<20**2
            native=Image.open(P/'sources/canonical-head.png').rotate(-row['tiltDegrees'],resample=Image.Resampling.BICUBIC,expand=True);x,y=row['helmetPosition'];allowed[max(0,y):min(256,y+native.height),max(0,x):min(256,x+native.width)]=True
            check(np.array_equal(a[~allowed],b[~allowed]),'Exact paired body outside local helmet region '+str(i))
            check(row['nativeScale']==1,'Native canonical helmet scale '+str(i))
before={f:sha(P/f) for f in [*hashes,'bare-manifest.json','helmet-manifest.json']}
run=subprocess.run([sys.executable,str(P/'build.py')],capture_output=True,text=True)
check(run.returncode==0 and all(sha(P/f)==v for f,v in before.items()),'Deterministic12frame/2manifest rebuild')
result={'passed':all(x['passed'] for x in checks),'checks':len(checks),'results':checks,'scope':'paired source packaging/master rulers/pixels/timing; no normal mortality/restore/world proof; terminal expression and contact/pacing/detail polish remain'}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'checks':len(checks),'failures':[x['check'] for x in checks if not x['passed']]}));raise SystemExit(0 if result['passed'] else 1)
