"""Uniform alpha-only extraction trial. Source RGB and whole ruler unchanged."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
from matte import metrics
P=Path(__file__).resolve().parent;D=P/'full-clip-frames-uneroded-v1';D.mkdir(exist_ok=True)
def extract(im):
 rgb=np.asarray(im.convert('RGB'));foreground=np.max(np.abs(rgb.astype(int)-np.array([12,18,24])),axis=2)>8
 lab,n=ndimage.label(foreground);counts=np.bincount(lab.ravel());counts[0]=0
 mask=foreground&(counts[lab]>=20);a=np.dstack([rgb,mask.astype('uint8')*255]);a[~mask]=0
 return Image.fromarray(a).resize((256,256),Image.Resampling.LANCZOS)
raws=sorted((P/'raw-review').glob('raw-*.png'));assert len(raws)==142
frames=[];rows=[];bindings={}
for n,path in enumerate(raws):
 im=extract(Image.open(path));im.save(D/f'{n:03}.png');frames.append(im);rows.append(dict(frame=n,**metrics(im)));bindings[str(path.relative_to(P))]=hashlib.sha256(path.read_bytes()).hexdigest()
control=extract(Image.open(P/'master-input.png'));control.save(P/'input-alpha-control-uneroded.png')
num=24;durations=[round((n+1)*1000/num)-round(n*1000/num) for n in range(len(frames))]
frames[0].save(P/'full-source-review-uneroded.png',save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
replay=Image.open(P/'full-source-review-uneroded.png');assert replay.n_frames==len(frames)
for n,im in enumerate(frames):replay.seek(n);assert np.array_equal(np.asarray(replay.convert('RGBA')),np.asarray(im));assert round(replay.info['duration'])==durations[n]
master=Image.open(P/'registered-reference.png').convert('RGBA');oldcontrol=Image.open(P/'input-alpha-control.png').convert('RGBA')
for start in range(0,len(frames),24):
 b=Image.new('RGB',(1792,1200),'#202a30');draw=ImageDraw.Draw(b)
 for j,im in enumerate(frames[start:start+24]):
  n=start+j;b.paste(im,((j%6)*256,(j//6)*290+20),im);draw.text(((j%6)*256+3,(j//6)*290+3),f'{n} H{rows[n]["height"]} head{rows[n]["headWidth"]} floor{rows[n]["floor"]}',fill='white')
 b.paste(master,(1536,20),master);draw.text((1540,3),'Original native',fill='white');b.save(P/f'uneroded-chronology-{start//24:02}.png')
ims=[master,oldcontrol,control]+[frames[n] for n in [0,35,71,106,141]]
labels=['Original master','Previous erosion control','No erosion control']+[f'No erosion source {n}' for n in [0,35,71,106,141]]
b=Image.new('RGB',(2048,660),'#202a30');draw=ImageDraw.Draw(b)
for j,(im,label) in enumerate(zip(ims,labels)):
 b.paste(im,(j*256,30),im);draw.text((j*256+3,5),label,fill='white');detail=im.crop((100,70,165,170)).resize((195,300),Image.Resampling.NEAREST);b.paste(detail,(j*256+8,330),detail)
b.save(P/'uneroded-master-control-comparison.png')
report=dict(frameCount=len(frames),checks=len(frames)*2,failures=0,control=metrics(control),master=metrics(master),rows=rows,ranges={k:[min(r[k] for r in rows),max(r[k] for r in rows)] for k in ['height','headWidth','headAxis','headTop','floor','upperBodyWidth']},rawBindings=bindings,registration=dict(scale=1/3,offset=[0,0]),alpha='Same darkbackground12/18/24, tolerance8, connected components>=20raw; omit one-raw-pixel erosion uniformly. Whole source RGB unchanged, fixed resample only.',visualReview='pending',scope='Alpha extraction/control trial only; no per-frame contact/palette/anatomy edits; source/native/integration acceptance separate.')
(P/'uneroded-source-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(checks=report['checks'],failures=0,control=report['control'],ranges=report['ranges'])))
