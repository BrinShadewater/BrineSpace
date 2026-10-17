from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
checks=0;failures=[]
def check(ok,msg):
 global checks
 checks+=1
 if not ok:failures.append(msg)
def pixels(path):return np.array(Image.open(path).convert('RGBA'))
boards=[]
for d in ['east','south','west','north']:
 p=P.parent/('james-lying-'+d+'-v1');m=json.loads((p/'bare-manifest.json').read_text());reg=json.loads((p/'registration.json').read_text());hashes=json.loads((p/'frame-hashes.json').read_text())
 oldroot=P.parent/'chief-engineer-branforth-v2/packs/bare-256x256-p128.0-224.0';old=json.loads((oldroot/'manifest.json').read_text())
 check(reg['sourceSha256']==hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),d+' source hash')
 state={s['id'].split('-'+d)[0]:s for s in m['states']}
 frames={a:[pixels(p/f) for f in s['frameFiles']] for a,s in state.items()}
 for a,s in state.items():
  baseline=next(q for q in old['states'] if q['id']==s['id'])
  for key in ['frameDurationsMs','depthOffsets','waterKinds','waterPoses','facings','loop']:
   expected=baseline[key]
   if key=='depthOffsets' and d=='north' and a in ['lie-down','get-up']:expected=[0,19,58,58,77,96] if a=='lie-down' else [96,77,58,58,19,0]
   check(s[key]==expected,d+a+' selected '+key)
  for j,f in enumerate(s['frameFiles']):
   arr=frames[a][j];check(arr.shape==(256,256,4),f+' canvas');check(hashlib.sha256((p/f).read_bytes()).hexdigest()==hashes[f],f+' hash')
   check(not np.any(arr[[0,-1],:,3]) and not np.any(arr[:,[0,-1],3]),f+' unclipped canvas')
   i=s['provenance']['sourcePoses'][j]
   if i==0:continue
   raw=pixels(p/'registered-ungraded'/f'{i:03d}.png');check(np.array_equal(arr[:,:,3],raw[:,:,3]),f+' exact alpha')
   x0,y0,x1,y1=reg['tracking'][i]['protectedHeadBox'];check(np.array_equal(arr[y0:y1,x0:x1],raw[y0:y1,x0:x1]),f+' protected head')
 for j in range(6):check(np.array_equal(frames['lie-down'][j],frames['get-up'][5-j]),d+' reverse '+str(j))
 check(np.array_equal(frames['lie-down'][5],frames['sleep'][0]) and np.array_equal(frames['sleep'][0],frames['sleep'][5]),d+' sleep joins')
 native=P.parent/'crew-runtime-matte-v1/branforth';mm=json.loads((native/'manifest.json').read_text());sm=next(s for s in mm['states'] if s['id']=='idle-'+d);master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(native/sm['frameFiles'][0]).convert('RGBA'),(36,52));check(np.array_equal(frames['lie-down'][0],np.array(master)),d+' selected master arrival')
 sequence=[('lie-down',j) for j in range(6)]+[('sleep',j) for j in range(6)]+[('get-up',j) for j in range(6)]
 gif=[];dur=[]
 for a,j in sequence:
  b=Image.new('RGB',(1000,330),'#303b40');dr=ImageDraw.Draw(b);dr.text((12,10),'James '+d+' | '+a+' | master scale / 82px / 54px / 27px',fill='white');im=Image.fromarray(frames[a][j]);b.paste(im,(10,38),im)
  for x,h in [(340,82),(600,54),(825,27)]:
   scaled=im.resize((round(256*h/148),round(256*h/148)),Image.Resampling.LANCZOS);at=(x,round(282-224*h/148));b.paste(scaled,at,scaled)
  gif.append(b);dur.append(int(state[a]['frameDurationsMs'][j]))
 gif[0].save(p/'review.gif',save_all=True,append_images=gif[1:],duration=dur,loop=0,disposal=2)
 check(sum(dur)==2560,d+' preview duration')
 gif[4].save(p/'review-frame004.png')
report=dict(checks=checks,failures=failures,status='PASS' if not failures else 'FAIL',scope='Bare staged packaging only; no helmet or live installation acceptance')
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));raise SystemExit(bool(failures))
