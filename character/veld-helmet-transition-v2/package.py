"""Reviewable helmet-to-hands study, not a complete locker transition."""
from pathlib import Path
import json,hashlib
import numpy as np,imageio.v2 as iio
from scipy import ndimage
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
reader=iio.get_reader(P/'endpoint-source.mp4');raw=[a for a in reader];reader.close()
scale=148/911/.78/.75;size=round(768*scale);offset=(92-round(384*scale),196-round(705*scale))
# Remove the long above-head hesitation by using actual authored poses at a faster
# cadence there. No crossfades, interpolated poses or geometric deformation.
indices=list(range(0,43,2))+list(range(43,81,5))+list(range(81,99))
frames=[];checks=[]
for n in indices:
 a=np.asarray(raw[n]).astype(float);patch=a[530:565,333:367];m=(np.ptp(patch,axis=2)<24)&(patch.mean(axis=2)>25)&(patch.mean(axis=2)<145);median=np.median(patch[m],axis=0)
 gain=np.array([78,77,77])/median
 value=a.mean(axis=2);weight=np.clip((32-np.ptp(a,axis=2))/16,0,1)*np.clip((160-value)/45,0,1)*np.clip(value/25,0,1)
 b=np.rint(a+(a*gain-a)*weight[:,:,None]).clip(0,255).astype('uint8')
 key=(a[:,:,1]>a[:,:,0]*1.3)&(a[:,:,1]>a[:,:,2]*1.3)&(a[:,:,1]>90)
 lab,_=ndimage.label(~key);counts=np.bincount(lab.ravel());counts[0]=0;mask=lab==counts.argmax()
 im=Image.fromarray(np.dstack([b,mask.astype('uint8')*255]));f=Image.new('RGBA',(184,208));f.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),offset);frames.append(f)
 aa=np.array(f);ys,xs=np.where(aa[:,:,3]>=128)
 corrected=b[530:565,333:367][m]
 checks.append(dict(sourceFrame=n,gain=gain.tolist(),fabricMedianRGB=np.median(corrected,axis=0).tolist(),bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]))
manifest=dict(name='Veld helmet lift/lower motion study',status='candidate_not_installed_incomplete_locker_handoff',frameWidth=184,frameHeight=208,pivot=[92,196],standingHeight=148,precomposed=True,states=[],remaining='Pickup/return to locker and joins to bare idle; source after frame 98 rejected because helmet disappears.')
for key,order,total in [('remove-helmet-to-hands-east',list(range(len(frames))),2240),('fit-helmet-from-hands-east',list(reversed(range(len(frames)))),2140)]:
 dest=P/'frames'/key;dest.mkdir(parents=True,exist_ok=True);paths=[]
 for i,n in enumerate(order):
  path=dest/f'{i:03d}.png';frames[n].save(path);paths.append(path.relative_to(P).as_posix())
 manifest['states'].append(dict(id=key,frameCount=len(order),frameFiles=paths,frameDurationsMs=[round((i+1)*total/len(order))-round(i*total/len(order)) for i in range(len(order))],loop=False,sourceVideo='endpoint-source.mp4',sourceFrames=[indices[n] for n in order],derivation='Authored source poses, reversed for fitting; fixed registration, neutral-midtone colour correction.'))
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
audit=dict(sourceSha256=hashlib.sha256((P/'endpoint-source.mp4').read_bytes()).hexdigest(),selectedFrames=len(frames),processing='Small per-frame neutral-midtone gain from stationary shin sample to bare-master RGB78,77,77. No pose edits. Bright silver and chromatic pixels retained.',frames=checks,installed=False)
audit['exportClippedFrames']=[c['sourceFrame'] for c in checks if c['bounds'][0]<=0 or c['bounds'][1]<=0 or c['bounds'][2]>=184 or c['bounds'][3]>=208]
assert not audit['exportClippedFrames']
(P/'checks.json').write_text(json.dumps(audit,indent=2)+'\n')
review=[]
for i in range(len(frames)):
 bg=Image.new('RGB',(736,478),'#263139');d=ImageDraw.Draw(bg)
 for col,(n,label) in enumerate([(i,'REMOVE TO HANDS'),(len(frames)-1-i,'FIT FROM HANDS')]):
  f=frames[n].resize((368,416),Image.Resampling.NEAREST);bg.paste(f,(col*368,26),f);d.text((col*368+12,8),label,fill='white')
 d.text((12,454),'Motion study - locker pickup/return still pending',fill='#edc182');review.append(bg)
review[0].save(P/'fit-remove-review.gif',save_all=True,append_images=review[1:],duration=50,loop=0,optimize=False)
print(json.dumps({'framesPerAction':len(frames),'exportClipping':audit['exportClippedFrames'],'fabricMedianRange':[np.min([c['fabricMedianRGB'] for c in checks],axis=0).tolist(),np.max([c['fabricMedianRGB'] for c in checks],axis=0).tolist()]}))
