from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
source=P/'master-source.png';raw=np.array(Image.open(source).convert('RGBA'));ys,xs=np.where(raw[:,:,3]>=128);box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
im=Image.open(source).convert('RGBA').crop(box);a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);im=Image.fromarray(a)
v=a[:,:,:3].astype(float);mask=(a[:,:,3]>=128)&(np.ptp(v,axis=2)<24)&(v.mean(axis=2)>25)&(v.mean(axis=2)<145);med=np.median(v[mask],axis=0);gain=np.minimum(1,np.array([69,68,69])/med);weight=np.clip((40-np.ptp(v,axis=2))/16,0,1)*np.clip((160-v.mean(axis=2))/35,0,1)*np.clip(v.mean(axis=2)/25,0,1);a[:,:,:3]=np.rint(v+(v*gain-v)*weight[:,:,None]).clip(0,255).astype('uint8');im=Image.fromarray(a);(P/'input-colour.json').write_text(json.dumps({'sourceMedian':med.tolist(),'gain':gain.tolist(),'target':[69,68,69]},indent=2))
height=800;width=round(im.width*height/im.height);pose=im.resize((width,height),Image.Resampling.LANCZOS)
pos=(512-width//2,130);bg=Image.new('RGB',(1024,1024),(48,190,72));bg.paste(pose,pos,pose);bg.save(P/'master-input.png')
standing=im.resize((round(im.width*148/im.height),148),Image.Resampling.LANCZOS);out=Image.new('RGBA',(184,184));out.alpha_composite(standing,(92-standing.width//2,24));out.save(P/'master-standing.png')
(P/'source-selection.json').write_text(json.dumps({'status':'Selected reference-derived front master for owner-authorized south-walk pilot; wider inferred reference-sheet details remain review candidates.','source':source.relative_to(P.parent).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'crop':box,'inputSize':[1024,1024],'inputStandingHeight':800,'inputPlacement':pos,'inputSoleY':930,'alphaThreshold':128,'palette':'Fixed neutral correction to accepted Bill side midtones. Dark graphite, silver, burgundy operations accents.','scaleAt768':148/600,'offsetAt768':[-3,0],'registrationNote':'Fixed clip-wide calibration for source body expansion; no per-frame resizing'},indent=2)+'\n')
