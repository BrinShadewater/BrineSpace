from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];m=json.loads((P/'manifest.json').read_bytes());selection=json.loads((P/'selection.json').read_bytes());checks=0;failures=[]
def check(ok,why):
 global checks
 checks+=1
 if not ok:failures.append(why)
def pixels(p):return np.array(Image.open(p).convert('RGBA'))
def extent(a):
 y,x=np.where(a[:,:,3]>180);return [int(y.min()),int(y.max()),int(y.max()-y.min()+1)]
def band(a,y0,y1):
 widths=[]
 for row in a[y0:y1]:
  x=np.where(row[:,3]>180)[0]
  if len(x):widths.append(int(x.max()-x.min()+1))
 return float(np.median(widths))
def neutral(a):
 rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);y,x=np.indices(a.shape[:2]);mask=(a[:,:,3]>180)&(y>54)&(y<149)&(abs(r-g)<12)&(abs(g-b)<12);return np.median(rgb[mask],axis=0)
base=R/'character/crew-runtime-matte-v1/branforth';m0=json.loads((base/'manifest.json').read_bytes());st=next(s for s in m0['states'] if s['id']=='idle-south');master=pixels(base/st['frameFiles'][0]);held=pixels(R/'character/james-meal-south-v1/frames/eat/000.png')
state=m['states'][0];check(state['id']=='meal-acquire-south' and not state['loop'],'South finite pickup');check(len(state['frameFiles'])==6 and sum(state['frameDurationsMs'])==900,'Six whole poses900ms');check(m['pivot']==[92,172] and m['standingHeight']==148,'Selected ruler/pivot')
first=pixels(P/state['frameFiles'][0]);last=pixels(P/state['frameFiles'][-1]);check(np.array_equal(first[:184],master) and not first[184:,:,3].any(),'Exact padded idle');check(np.array_equal(last[:held.shape[0]],held) and not last[held.shape[0]:,:,3].any(),'Exact padded held meal')
rows=[]
for i,rel in enumerate(state['frameFiles']):
 a=pixels(P/rel);check(a.shape==(192,184,4),'Canvas'+str(i));check(not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any(),'Unclipped'+str(i));ex=extent(a);check(abs(ex[2]-extent(master)[2])<=2,'Master height'+str(i));check(abs(ex[1]-extent(master)[1])<=2,'Opaque sole'+str(i));head=band(a,26,48);calf=band(a,132,148);boot=band(a,158,171);colour=neutral(a);check(abs(head-band(master,26,48))<=3,'Master head band'+str(i));check(abs(calf-band(master,132,148))<=4,'Master calf band'+str(i));check(abs(boot-band(master,158,171))<=5,'Master boot band'+str(i));check(np.max(abs(colour-neutral(master)))<=18,'Master neutral cloth'+str(i));rows.append({'pose':i,'extent':ex,'headWidth':head,'calfWidth':calf,'bootWidth':boot,'neutralRGB':colour.tolist()})
raw=pixels(P/'source.png');check(int((raw[:,:,3]==0).sum())>500000,'Real transparent source');check(len({r['sourcePose'] for r in selection['poses']})==6,'Six independent source figures')
e={'checks':checks,'failures':failures,'rows':rows,'sourceSha256':hashlib.sha256((P/'source.png').read_bytes()).hexdigest(),'scope':'Fixed shared ruler/whole source crops, independent master head/calf/boot bands, matte neutral palette, exact selected endpoints. Not native hand/worktop or owner motion acceptance.'};(P/'fit-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf8');print({'checks':checks,'failures':failures,'rows':rows});raise SystemExit(bool(failures))
