from pathlib import Path
import json,hashlib,subprocess,sys
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[]
for gear in ('bare','helmet'):
 m=json.loads((P/f'{gear}-manifest.json').read_text());down,rise,held=m['states'];registration=json.loads((P/('bare-registration.json' if gear=='bare' else 'helmet-registration.json')).read_text())
 check(m['status']=='staged_candidate' and m['pivot']==[128,224] and m['standingHeight']==148,'master ruler')
 check([s['id'] for s in m['states']]==['sit-down-south','sit-rise-south','sit-idle-south'],'paired state coverage')
 check(sum(down['frameDurationsMs'])==800 and not down['loop'] and not rise['loop'] and held['loop'],'finite down/rise, loop held')
 check(rise['frameFiles']==down['frameFiles'][::-1] and rise['frameDurationsMs']==down['frameDurationsMs'][::-1],'exact reverse source and clock')
 check(held['frameFiles']==[down['frameFiles'][-1]],'held/down/rise joins')
 check(all(s['seatContactDepth'] and s['depthOffsets']==[0]*len(s['frameFiles']) for s in m['states']),'registered depth marker')
 master_path=R/(registration['master'] if gear=='bare' else registration['helmetIdle'])
 master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(master_path).convert('RGBA'),(36,52))
 check(master.tobytes()==Image.open(P/down['frameFiles'][0]).tobytes(),'exact selected standing')
 for name in down['frameFiles']:
  path=P/name;im=Image.open(path);files.append(path)
  check(im.mode=='RGBA' and im.size==(256,256),'RGBA canvas')
  bbox=im.getchannel('A').point(lambda a:255 if a>180 else 0).getbbox()
  check(bbox and 222<=bbox[3]-1<=224,'registered grounded feet')
  check(im.getchannel('A').getbbox()[0]>0 and im.getchannel('A').getbbox()[2]<256,'no clipping')
 check(len({sha(P/f) for f in down['frameFiles']})==6,'six distinct articulated down figures')
 files.extend(P/f for f in [f'{gear}-manifest.json','bare-registration.json' if gear=='bare' else 'helmet-registration.json'])
br=json.loads((P/'bare-registration.json').read_text());hr=json.loads((P/'helmet-registration.json').read_text())
check(sha(P/br['source'])==br['sourceSha256'] and sha(R/br['master'])==br['masterSha256'],'source/master bindings')
check(sha(R/hr['nativeComponent'])==hr['nativeComponentSha256'],'native hardware binding')
component=np.array(Image.open(R/hr['nativeComponent']).convert('RGBA'))
for r in hr['frames']:
 slot=r['slot'];bare=np.array(Image.open(P/f'frames/bare/sit-down-south/{slot:03}.png'));fitted=np.array(Image.open(P/f'frames/helmet/sit-down-south/{slot:03}.png'))
 yy,xx=np.indices(bare.shape[:2]);hx,hy=r['headCenter'];x,y=r['componentPosition'];w,h=r['componentSize']
 allowed=(((xx-hx)**2+(yy-hy)**2<r['eraseRadius']**2)&(yy<=r['eraseYMax']))|((xx>=x)&(xx<x+w)&(yy>=y)&(yy<y+h))
 check(np.array_equal(bare[~allowed],fitted[~allowed]),'protected body outside head/component fit')
 opaque=component[:,:,3]==255;check(np.array_equal(fitted[y:y+h,x:x+w][opaque],component[opaque]),'native opaque hardware exact')
 check(r['nativeScale']==1 and r['rotationDegrees']==0 and [w,h]==[35,39],'fixed hardware scale')
files += [P/f for f in ['source-review.json','source-review.png','semantic-masks.png','bare-contact.png','paired-contact.png']]
before={str(p.relative_to(P)):sha(p) for p in files}
for script in ('review_source.py','build_bare.py','build_helmet.py'):subprocess.run([sys.executable,str(P/script)],check=True,capture_output=True)
check(before=={str(p.relative_to(P)):sha(p) for p in files},'deterministic rebuild')
report={'checks':checks,'failures':0,'uniqueExports':12,'stateReferences':26,'normalSelection':False,'files':before,'scope':'paired source pixel/master/scale/clock/reverse/joins/native hardware/protected body/rebuild checks; native/furniture/motion/acceptance distinct'}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'checks':checks,'failures':0,'deterministicFiles':len(before),'normalSelection':False}))
