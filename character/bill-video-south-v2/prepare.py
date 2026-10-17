from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
source=P.parent/'bill-front-proportion-v3/master-input.png'
a=np.array(Image.open(source).convert('RGB'));v=a.astype(float)
key=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90)
ys,xs=np.where(~key);box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
neutral=(~key)&(np.ptp(v,axis=2)<24)&(v.mean(axis=2)>25)&(v.mean(axis=2)<145)
median=np.median(v[neutral],axis=0);gain=np.minimum(1,np.array([69,68,69])/median)
weight=np.clip((40-np.ptp(v,axis=2))/16,0,1)*np.clip((160-v.mean(axis=2))/35,0,1)*np.clip(v.mean(axis=2)/25,0,1)
rgb=np.rint(v+(v*gain-v)*weight[:,:,None]).clip(0,255).astype('uint8')
im=Image.fromarray(np.dstack([rgb,(~key).astype('uint8')*255])).crop(box)
pose=im.resize((round(im.width*800/im.height),800),Image.Resampling.LANCZOS)
bg=Image.new('RGB',(1024,1024),(48,190,72));bg.paste(pose,(512-pose.width//2,130),pose);bg.save(P/'master-input.png')
pose=im.resize((round(im.width*148/im.height),148),Image.Resampling.LANCZOS)
out=Image.new('RGBA',(184,184));out.alpha_composite(pose,(92-pose.width//2,24));out.save(P/'master-standing.png')
(P/'source-selection.json').write_text(json.dumps(dict(source=str(source.relative_to(P.parent)),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),crop=box,inputSize=[1024,1024],inputStandingHeight=800,scaleAt768=148/600,offsetAt768=[-3,-2],neutralInputMedian=median.tolist(),inputGain=gain.tolist(),status='Owner continued from midpoint head revision; dark neutral input correction; video candidate'),indent=2))
