from pathlib import Path
import hashlib,json,subprocess,sys
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(condition):
    global checks
    assert condition;checks+=1
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
m=json.loads((P/'bare-manifest.json').read_text());registration=json.loads((P/'bare-registration.json').read_text())
check(m['status']=='staged_candidate' and m['pivot']==[128,224] and m['standingHeight']==148)
down,rise,held=m['states'];check([s['id'] for s in m['states']]==['sit-down-north','sit-rise-north','sit-idle-north'])
check(sum(down['frameDurationsMs'])==800);check(rise['frameFiles']==down['frameFiles'][::-1]);check(rise['frameDurationsMs']==down['frameDurationsMs'][::-1])
check(not down['loop'] and not rise['loop'] and held['loop']);check(held['frameFiles']==[down['frameFiles'][-1]])
check(all(s.get('seatContactDepth') is True and all(v==0 for v in s['depthOffsets']) for s in m['states']))
check(sha(P/registration['source'])==registration['sourceSha256']);check(sha(R/registration['master'])==registration['masterSha256'])
standing=Image.new('RGBA',(256,256));standing.alpha_composite(Image.open(R/registration['master']).convert('RGBA'),(36,52))
check(standing.tobytes()==Image.open(P/down['frameFiles'][0]).tobytes())
for path in down['frameFiles']:
    im=Image.open(P/path);check(im.mode=='RGBA' and im.size==(256,256))
    solid=im.getchannel('A').point(lambda a:255 if a>180 else 0).getbbox();check(solid is not None and 222<=solid[3]-1<=224)
    check(im.getchannel('A').getbbox()[0]>0 and im.getchannel('A').getbbox()[2]<256)
check(len({sha(P/f) for f in down['frameFiles']})==6)
tracked=down['frameFiles']+['bare-manifest.json','bare-registration.json','bare-contact-sheet.png','source-scale-review.json','source-scale-review.png']
before={f:sha(P/f) for f in tracked}
for script in ['review_scale.py','build_bare.py']:subprocess.run([sys.executable,str(P/script)],check=True,capture_output=True)
check(before=={f:sha(P/f) for f in tracked})
helmet=json.loads((P/'helmet-manifest.json').read_text());hr=json.loads((P/'helmet-registration.json').read_text())
check(helmet['equipment']=='diving-helmet' and len(helmet['states'])==3)
check(helmet['states'][0]['frameDurationsMs']==down['frameDurationsMs'])
check(helmet['states'][1]['frameFiles']==helmet['states'][0]['frameFiles'][::-1])
check(helmet['states'][2]['frameFiles']==[helmet['states'][0]['frameFiles'][-1]])
check(all(s.get('seatContactDepth') is True and all(v==0 for v in s['depthOffsets']) for s in helmet['states']))
check(sha(R/hr['nativeComponent'])==hr['nativeComponentSha256'])
check(sha(R/hr['helmetIdle'])==hr['helmetIdleSha256'])
equipped=Image.new('RGBA',(256,256));equipped.alpha_composite(Image.open(R/hr['helmetIdle']).convert('RGBA'),(36,52))
check(equipped.tobytes()==Image.open(P/helmet['states'][0]['frameFiles'][0]).tobytes())
component=np.array(Image.open(R/hr['nativeComponent']).convert('RGBA'))
for slot,record in enumerate(hr['frames'],1):
    bare=np.array(Image.open(P/down['frameFiles'][slot]));fitted=np.array(Image.open(P/helmet['states'][0]['frameFiles'][slot]))
    yy,xx=np.indices(bare.shape[:2]);hx,hy=record['headCenter'];x,y=record['componentPosition'];w,h=record['componentSize']
    allowed=(((xx-hx)**2+(yy-hy)**2<record['eraseRadius']**2)&(yy<=record['eraseYMax']))|((xx>=x)&(xx<x+w)&(yy>=y)&(yy<y+h))
    check(np.array_equal(bare[~allowed],fitted[~allowed]))
    check(record['nativeScale']==1 and record['rotationDegrees']==0 and [w,h]==[33,35])
    opaque=component[:,:,3]==255;check(np.array_equal(fitted[y:y+h,x:x+w][opaque],component[opaque]))
    check(fitted[record['eraseYMax']+4:,:,3].sum()==bare[record['eraseYMax']+4:,:,3].sum())
tracked+=helmet['states'][0]['frameFiles']+['helmet-manifest.json','helmet-registration.json','paired-contact-sheet.png']
before={f:sha(P/f) for f in tracked}
subprocess.run([sys.executable,str(P/'build_helmet.py')],check=True,capture_output=True)
check(before=={f:sha(P/f) for f in tracked})
result={'checks':checks,'failures':0,'bareStates':3,'helmetStates':3,'uniqueExports':12,'references':26,'durationMs':800,'deterministicFiles':len(tracked),'normalSelection':False,'scope':'paired candidate source/pixel/registration/finite reverse/held/native canonical hardware/protected body/determinism; native player/anatomy/cadence/furniture/world distinct'}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
