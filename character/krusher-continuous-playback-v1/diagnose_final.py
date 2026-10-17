from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json
from scipy import ndimage
R=Path.cwd();H=R/'character/krusher-continuous-playback-v1';lib=json.loads((H/'library.json').read_text());states=lib['states'];cache={};issues=[];transitions=[]
def frame(key,i):
 s=states[key];path=s['files'][i]
 if path not in cache:
  im=Image.open(R/path.lstrip('/')).convert('RGBA');a=np.array(im);labels,n=ndimage.label(a[:,:,3]>96);areas=np.bincount(labels.ravel());areas[0]=0;cache[path]=(im,a,labels,areas.argmax())
 return cache[path]
def metrics(key,i):
 im,a,l,largest=frame(key,i);s=states[key];cx,cy=s['heads'][i];x0=max(0,cx-22);x1=min(im.width,cx+22);y0=max(0,cy-32);y1=min(im.height,cy+12);b=a[y0:y1,x0:x1];r,g,bl=[b[:,:,k].astype(float) for k in range(3)];warm=(b[:,:,3]>190)&(r>g*1.1)&(r>bl*1.15)&(r>55);ys,xs=np.where(warm);main=l[y0:y1,x0:x1]==largest;frac=float(main[warm].mean()) if len(xs) else 1
 return {'warm':len(xs),'attached':frac,'center':[(float(xs.mean()+x0)-s['pivot'][0]),(float(ys.mean()+y0)-s['pivot'][1])] if len(xs) else None}
for key,s in states.items():
 ms=[metrics(key,i) for i in range(len(s['files']))]
 for i,m in enumerate(ms):
  if m['warm']>12 and m['attached']<.95:issues.append({'key':key,'slot':i,**m})
 for i in range(len(ms)-1):
  a,b=ms[i:i+2]
  if a['center'] and b['center']:
   d=float(np.linalg.norm(np.array(a['center'])-b['center']));ratio=max(a['warm'],b['warm'])/max(1,min(a['warm'],b['warm']))
   if d>9 or ratio>2.6:transitions.append({'key':key,'from':i,'to':i+1,'headTravel':round(d,2),'areaRatio':round(ratio,2)})
report={'componentFlags':issues,'motionFlags':sorted(transitions,key=lambda q:-q['headTravel']),'states':len(states),'slots':sum(len(s['files']) for s in states.values())};(H/'motion-diagnostics-v11.json').write_text(json.dumps(report,indent=2));print({'componentFlags':len(issues),'motionFlags':len(transitions),'componentExamples':issues[:12],'travelExamples':report['motionFlags'][:12]})
