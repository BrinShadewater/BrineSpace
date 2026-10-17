from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;BASE=P.parent/'veld-seated-north-coherent-v1'
checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
files=[]
for gear in ('bare','helmet'):
 m=json.loads((P/f'{gear}-manifest.json').read_text());s=m['states'][0]
 check(m['pivot']==[128,224] and m['standingHeight']==148,'canonical scale')
 check(s['loop'] and sum(s['frameDurationsMs'])==3600,'breathing loop clock')
 check(s['seatContactDepth'] and s['depthOffsets']==[0]*6,'registered seat ordering')
 a=np.array(Image.open(BASE/f'frames/{gear}/sit-down-north/005.png'))
 ys,xs=np.indices(a.shape[:2]);allowed=(ys>146)&(ys<178)&(abs(xs-128)>10)&(abs(xs-128)<34)
 arrays=[]
 for f in s['frameFiles']:
  path=P/f;im=Image.open(path);b=np.array(im);arrays.append(b);files.append(path)
  check(im.mode=='RGBA' and im.size==(256,256),'canonical canvas')
  check(np.array_equal(a[~allowed],b[~allowed]),'head/collar/panel/support pixels protected')
  check(np.array_equal(a[178:],b[178:]),'belt and contact exact')
 check(np.array_equal(arrays[0],a) and np.array_equal(arrays[-1],a),'held/down/rise neutral joins')
 check(len({v.tobytes() for v in arrays})==5,'four actual breathing interiors')
files += [P/f'{g}-manifest.json' for g in ('bare','helmet')]+[P/'fitted-registration.json',P/'fitted-contact.png']
def hashes():return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
before=hashes();subprocess.run([sys.executable,str(P/'fit_breathing.py')],check=True,capture_output=True)
check(before==hashes(),'deterministic fit')
r={'checks':checks,'failures':0,'scope':'paired local breathing source fit, pixel protection, exact neutral joins, clock, fixed scale, deterministic PNG/metadata rebuild; native/full motion/contact/acceptance distinct','hashes':before,'normalSelection':False}
(P/'fitted-verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'checks':checks,'failures':0,'boundFiles':len(before)}))
