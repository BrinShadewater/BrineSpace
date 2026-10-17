"""Rebuild the existing native material pipeline with one shared interior curve."""
from pathlib import Path
import json,hashlib,copy,shutil
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];OLD=P.parent/'james-west-water-death-polish-v1'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
P.mkdir(exist_ok=True);reg=read(OLD/'registration.json');inputs={};rows={};checks=[];hashes={}
curve={'threshold':50,'slope':.8,'blueHighlightGain':.98,'mask':'alpha>0, RGB spread<30, original shared helmet edit-region excluded','scope':'One fixed smooth highlight compression shared across every interior and gear; no per-frame exposure fit. Exact entry untouched.'}
for mode in ['bare','helmet']:
 mf=OLD/(mode+'-manifest.json');inputs[mf.relative_to(R).as_posix()]=sha(mf);m=read(mf);s=m['states'][0];rows[mode]=[]
 for i,rel in enumerate(s['frameFiles']):
  f=OLD/rel;inputs[f.relative_to(R).as_posix()]=sha(f);a=np.array(Image.open(f).convert('RGBA'));original=a.copy()
  if i:
   rgb=a[:,:,:3].astype(float);mask=(a[:,:,3]>0)&(np.ptp(rgb,axis=2)<30)
   x0,y0,x1,y1=reg['tracking'][i]['editRegion'];mask[y0:y1,x0:x1]=False
   corrected=rgb.copy();corrected=50+np.maximum(rgb-50,0)*.8+np.minimum(rgb-50,0)
   corrected[:,:,2]-=np.maximum(rgb[:,:,2]-50,0)*.02
   a[:,:,:3][mask]=np.rint(corrected[mask]).clip(0,255).astype('uint8')
   assert np.array_equal(a[y0:y1,x0:x1],original[y0:y1,x0:x1])
   assert np.array_equal(a[~mask],original[~mask])
  assert np.array_equal(a[:,:,3],original[:,:,3]);assert Image.fromarray(a).getbbox()==Image.fromarray(original).getbbox()
  checks.append({'mode':mode,'index':i,'alphaExact':True,'boundsExact':True,'entryExact':True if i==0 else None,'changedRGBPixels':int(np.any(a[:,:,:3]!=original[:,:,:3],axis=2).sum())})
  out=P/'frames'/mode/f'{i:03d}.png';out.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(a).save(out);rows[mode].append(a);hashes[out.relative_to(P).as_posix()]=sha(out)
 s['frameFiles']=[f'frames/{mode}/{i:03d}.png' for i in range(6)];s['provenance']={'derivedFrom':'../james-west-water-death-polish-v1/'+mode+'-manifest.json','method':'native source-builder material calibration; no generated pixel source selected','geometryAlphaExact':True,'materialCurve':curve};m['name']='James West water death material v2 '+mode;m['status']='installed_owner_review_pending' if (P/'selection.json').exists() and read(P/'selection.json').get('runtimeInstalled') else 'staged_owner_review_pending';write(P/(mode+'-manifest.json'),m)
for i in range(1,6):
 x0,y0,x1,y1=reg['tracking'][i]['editRegion'];mask=np.ones((360,256),bool);mask[y0:y1,x0:x1]=False;assert np.array_equal(rows['bare'][i][mask],rows['helmet'][i][mask])
inputs[(OLD/'registration.json').relative_to(R).as_posix()]=sha(OLD/'registration.json');write(P/'source-inputs-before.json',inputs);write(P/'material-curve.json',curve);write(P/'frame-hashes.json',hashes);write(P/'package-evidence.json',{'checks':checks,'sharedBodyOutsideHelmetExact':True,'sourceInputs':len(inputs),'scope':'Original source alpha/geometry/entry, helmet edit regions, non-mask pixels and all finite state metadata preserved. Fixed material curve only.'})
# Old/new full-pose review without changing source geometry.
b=Image.new('RGB',(1200,720),'#303b40');d=ImageDraw.Draw(b);events=[]
for i in range(6):
 event=Image.new('RGB',(850,450),'#303b40');ed=ImageDraw.Draw(event)
 for gear,mode in enumerate(['bare','helmet']):
  for version,folder in enumerate([OLD,P]):
   im=Image.open(folder/f'frames/{mode}/{i:03d}.png').convert('RGBA').crop((28,160,228,320));row=gear*2+version;b.paste(im,(i*200,row*180+20),im);d.text((i*200+4,row*180+3),('old ' if version==0 else 'new ')+mode+' '+str(i),fill='white')
   event.paste(im,(version*220,gear*210+30),im);ed.text((version*220+4,gear*210+5),('old ' if version==0 else 'new ')+mode+' '+str(i),fill='white')
  # Actual selected master is resolved from frozen current catalog below.
  cov=read(R/'character/james-locker-continue-v1/runtime-coverage.json');mf=R/cov['body' if mode=='bare' else 'equipment']['idle-west']['path'];mm=read(mf);st=next(s for s in mm['states'] if s['id']=='idle-west');rel=st['frameFiles'][0];f=R/rel.removeprefix('res://') if rel.startswith('res://') else mf.parent/rel;master=Image.open(f).convert('RGBA');event.paste(master,(470,gear*210+20),master);ed.text((475,gear*210+5),mode+' selected master',fill='white')
 events.append(event)
b.save(P/'all-poses-before-after.png');times=read(P/'bare-manifest.json')['states'][0]['frameDurationsMs'];events[0].save(P/'material-comparison.gif',save_all=True,append_images=events[1:]+[events[-1]],duration=[int(x) for x in times]+[2000],loop=0,disposal=2)
after={f:sha(R/f) for f in inputs};assert inputs==after;write(P/'source-inputs-after.json',after)
print(json.dumps({'frames':12,'inputsUnchanged':len(inputs),'changedRGBPixels':sum(c['changedRGBPixels'] for c in checks),'geometryAndAlphaExact':True,'sharedBodyExact':True}))
