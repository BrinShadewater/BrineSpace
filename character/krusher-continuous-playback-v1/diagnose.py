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
report={'componentFlags':issues,'motionFlags':sorted(transitions,key=lambda q:-q['headTravel']),'states':len(states),'slots':sum(len(s['files']) for s in states.values())};(H/'motion-diagnostics.json').write_text(json.dumps(report,indent=2));print({'componentFlags':len(issues),'motionFlags':len(transitions),'componentExamples':issues[:12],'travelExamples':report['motionFlags'][:12]})
# All independent one-shots against the neighboring canonical head pose.
keys=[k for k,s in states.items() if not s['loop'] and '-turn-' not in k and 'cancel-' not in k and 'return-' not in k];font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),18)
for page in range((len(keys)+11)//12):
 sheet=Image.new('RGBA',(1200,12*160),'#263138');d=ImageDraw.Draw(sheet)
 for row,key in enumerate(keys[page*12:(page+1)*12]):
  gear,action=key.split(':');direction=action.rsplit('-',1)[-1];base=gear+':'+('swim' if action.startswith('swim-') else 'idle')+'-'+direction
  if base not in states:base=gear+':idle-east'
  slots=[(base,0),(key,0),(key,min(1,len(states[key]['files'])-1)),(key,max(0,len(states[key]['files'])-2)),(key,len(states[key]['files'])-1),(base,0)]
  d.text((8,row*160+2),key,font=font,fill='white')
  for col,(k,i) in enumerate(slots):
   im=frame(k,i)[0];cx,cy=states[k]['heads'][i];crop=im.crop((cx-28,cy-30,cx+28,cy+30));sheet.alpha_composite(crop.resize((112,120),Image.Resampling.NEAREST),(col*196+40,row*160+30));d.text((col*196+8,row*160+13),('canonical' if k==base else 'pose '+str(i)),font=font,fill='#a9c2ca')
 sheet.save(H/('one-shot-joins-%02d.png'%page))
print({'independentOneShots':len(keys),'joinSheets':(len(keys)+11)//12})
