from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parents[1];raw=P/'raw-held-v1.png';a=np.array(Image.open(raw).convert('RGBA'));lab,n=ndimage.label(a[:,:,3]>200);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==int(sizes.argmax());yy,xx=np.where(mask);a[~ndimage.binary_dilation(mask,iterations=3)]=0
# New independent source density against the actual same-angle packaged master.
reference=Image.open(R/'character/veld-side-foundation-v1/east-standing.png').convert('RGBA');ry,rx=np.where(np.array(reference)[:,:,3]>200);reference_height=int(ry.max()-ry.min()+1)
for adjust in [0,1,-1,2,-2,3,-3]:
 h=round(a.shape[0]*reference_height/(yy.max()-yy.min()+1))+adjust;scale=h/a.shape[0];im=Image.fromarray(a).resize((round(a.shape[1]*scale),h),Image.Resampling.LANCZOS);z=np.array(im);y,x=np.where(z[:,:,3]>200)
 if y.max()-y.min()+1==reference_height:break
else:raise AssertionError('No reference density ruler')
fx=np.where(z[y.max()-3:y.max()+1,:,3]>128)[1];offset=(round(128-(fx.min()+fx.max())/2),223-int(y.max()));f=Image.new('RGBA',(256,256));f.alpha_composite(im,offset);f.save(P/'held-candidate.png')
def measure(im):
 z=np.array(im);y,x=np.where(z[:,:,3]>200);top=int(y.min());hx=np.where(z[top:top+16,:,3]>128)[1];bx=np.where(z[100:140,:,3]>200)[1];fx=np.where(z[214:225,:,3]>128)[1];region=z[142:175,108:149];rgb=region[:,:,:3].astype(float);lum=rgb.mean(2);m=(region[:,:,3]>200)&(np.ptp(rgb,axis=2)<15)&(lum>20)&(lum<180)
 return {'height':int(y.max()-y.min()+1),'headWidth':int(hx.max()-hx.min()+1),'upperBodyWidth':int(bx.max()-bx.min()+1),'soleSpan':int(fx.max()-fx.min()+1),'floor':int(y.max()),'clothQuartiles':np.percentile(lum[m],[25,50,75]).tolist()}
old=Image.new('RGBA',(256,256));old.alpha_composite(Image.open(R/'character/veld-side-foundation-v1/east-standing.png').convert('RGBA'),(36,52));end=Image.open(R/'character/veld-turn-north-east-original-master-v2/frames/bare/005.png').convert('RGBA');rows=[measure(x) for x in [end,old,f]];board=Image.new('RGB',(768,580),'#202a30');d=ImageDraw.Draw(board)
for i,(label,im) in enumerate(zip(['previous East held','original East master','new original-guided held'],[end,old,f])):board.paste(im,(i*256,22),im);d.text((i*256+4,4),label,fill='white');board.paste(im.crop((90,140,166,225)).resize((228,255)),(i*256+10,300))
board.save(P/'held-master-review.png');(P/'held-source-audit.json').write_text(json.dumps({'rows':rows,'scale':scale,'offset':offset,'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'postGenerationRGBChanged':False,'status':'diagnostic pending whole-source fidelity review; no promotion'},indent=2)+'\n',encoding='utf-8');print(json.dumps(rows))
