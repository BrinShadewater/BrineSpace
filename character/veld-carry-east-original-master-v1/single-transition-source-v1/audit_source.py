"""One complete master-derived transition at one whole-source standing ruler."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2];raw=P/'raw-transition-v1.png'
source=Image.open(raw).convert('RGBA');a=np.array(source);a[a[:,:,3]==0,:3]=0;source=Image.fromarray(a)
y,x=np.where(a[:,:,3]>200);estimate=round(source.height*148/(y.max()-y.min()+1))
for delta in [0,1,-1,2,-2,3,-3]:
    h=estimate+delta;scale=h/source.height;im=source.resize((round(source.width*scale),h),Image.Resampling.LANCZOS)
    z=np.array(im);y,x=np.where(z[:,:,3]>200)
    if int(y.max()-y.min()+1)==148:break
else:raise AssertionError('No whole-pose148 ruler')
top=int(y.min());hx=np.where(z[top:top+16,:,3]>128)[1]
offset=(round(123.5-(hx.min()+hx.max())/2),223-int(y.max()))
candidate=Image.new('RGBA',(256,256));candidate.alpha_composite(im,offset);candidate.save(P/'transition-candidate.png')
held_path=R/'character/veld-east-held-original-master-v1/frames/bare/000.png';held=Image.open(held_path).convert('RGBA')
empty=Image.new('RGBA',(256,256));empty.alpha_composite(Image.open(R/'character/veld-side-foundation-v1/east-standing.png').convert('RGBA'),(36,52))
def measure(image):
    a=np.array(image);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1]
    torso=np.where(a[110:155,:,3]>200)[1];cloth=a[125:165,105:140];rgb=cloth[:,:,:3].astype(float);lum=rgb.mean(2)
    mask=(cloth[:,:,3]>200)&(np.ptp(rgb,axis=2)<18)&(lum>20)&(lum<160)
    return {'height':int(y.max()-y.min()+1),'headWidth':int(hx.max()-hx.min()+1),'headTop':top,'upperBodyWidth':int(torso.max()-torso.min()+1),'floor':int(y.max()),'clothRGBMedian':np.median(rgb[mask],axis=0).tolist(),'clipped':bool(np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20))}
rows=[measure(i) for i in [held,candidate,empty]]
board=Image.new('RGB',(1200,820),'#202a30');d=ImageDraw.Draw(board)
for i,(name,image) in enumerate(zip(['Original held master','One whole transition','Original empty master'],[held,candidate,empty])):
    board.paste(image,(i*400+65,30),image);d.text((i*400+12,10),name,fill='white')
    head=image.crop((100,70,151,113)).resize((255,215),Image.Resampling.NEAREST);board.paste(head,(i*400+40,325),head)
    legs=image.crop((90,155,170,230)).resize((240,225),Image.Resampling.NEAREST);board.paste(legs,(i*400+40,570),legs)
board.save(P/'source-master-review.png')
report={'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sourceSize':list(source.size),'scale':scale,'offset':list(offset),'rows':rows,'scope':'Independent whole figure, unchanged pose upper body guided only by original held source, one entire-source148 density ruler/shared foot floor and whole head-axis translation. No head/limb/body RGB patch or per-region resize. Head/material/proportion/contact/native fidelity independently pending.'}
(P/'source-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'rows':rows,'scale':scale}))
