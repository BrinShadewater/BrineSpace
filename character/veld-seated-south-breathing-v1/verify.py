from pathlib import Path
import json,hashlib,subprocess,sys
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;BASE=P.parent/'veld-seated-south-coherent-v1'
checks=0;files=[];pairs={}
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
yy,xx=np.indices((256,256));allowed=(yy>130)&(yy<160)&(abs(xx-128)>12)&(abs(xx-128)<31)
for gear in ('bare','helmet'):
 m=json.loads((P/f'{gear}-manifest.json').read_text());s=m['states'][0]
 check(m['pivot']==[128,224] and m['standingHeight']==148,'master ruler/pivot')
 check(s['id']=='sit-idle-south' and s['loop'] and s['frameDurationsMs']==[600]*6,'held loop clock')
 check(s['seatContactDepth'] and s['depthOffsets']==[0]*6,'registered depth')
 a=np.array(Image.open(BASE/f'frames/{gear}/sit-down-south/005.png'));arrays=[]
 for f in s['frameFiles']:
  p=P/f;im=Image.open(p);b=np.array(im);arrays.append(b);files.append(p)
  check(im.mode=='RGBA' and im.size==(256,256),'RGBA native canvas')
  check(np.array_equal(a[~allowed],b[~allowed]),'protected anatomy/hardware exact')
  check(np.array_equal(a[160:],b[160:]),'belt/hands/knees/boots exact')
  check(not np.any(b[[0,-1],:,3]) and not np.any(b[:,[0,-1],3]),'no canvas clipping')
 check(np.array_equal(arrays[0],a) and np.array_equal(arrays[-1],a),'exact neutral loop seam and down/rise join')
 check(len({v.tobytes() for v in arrays})==5,'four distinct interior motion phases')
 pairs[gear]=arrays
for a,b in zip(pairs['bare'],pairs['helmet']):
 check(np.array_equal(a[130:],b[130:]),'paired breathing/body pixels exact')
files += [P/f'{g}-manifest.json' for g in ('bare','helmet')]+[P/'registration.json',P/'contact.png']
def hashes():return {p.relative_to(P).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
before=hashes();subprocess.run([sys.executable,str(P/'build.py')],check=True,capture_output=True)
check(before==hashes(),'deterministic rebuild')
(P/'verification.json').write_text(json.dumps({'checks':checks,'failures':0,'boundFiles':len(before),'hashes':before,'scope':'paired locally authored held loop, protected anatomy/hardware, exact joins, fixed grade/ruler; room contact and selection distinct','normalSelection':False},indent=2)+'\n')
print(json.dumps({'checks':checks,'failures':0,'boundFiles':len(before)}))
