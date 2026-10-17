"""Register the independently authored higher-density midpoint by its skull ruler."""
from pathlib import Path
import numpy as np,hashlib
from PIL import Image
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
def build():
 source=P/'sources/midpoint-detail-v6.png';raw=np.array(Image.open(source).convert('RGBA'));rgb=raw[:,:,:3].astype(float);yy,xx=np.indices(raw.shape[:2])
 ref=np.array(Image.open(P.parent/'crew-runtime-matte-v1/bill/frames/idle-north-breathing-v1/000.png').convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
 neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22);authority=(ref[:,:,3]>200)&(ry>53)&(np.ptp(rr,axis=2)<22);q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1]
 src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(rr.mean(2)[authority],q);mapped=np.interp(rgb.mean(2),src,dst);w=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 graded=raw.copy();graded[:,:,:3]=np.clip(rgb*(1-w[:,:,None])+mapped[:,:,None]*w[:,:,None],0,255).astype('uint8')
 red=(raw[:,:,3]>200)&(((xx>360)&(xx<535)&(yy>210)&(yy<305))|((xx>745)&(xx<925)&(yy>210)&(yy<305)))&(rgb.mean(2)>35)&(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2]);red_ref=(ref[:,:,3]>200)&(ry>53)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2]);red_gain=np.median(rr[red_ref],axis=0)/np.median(rgb[red],axis=0);graded[red,:3]=np.clip(rgb[red]*red_gain,0,255).astype('uint8')
 swim=np.array(Image.open(P.parent/'bill-swim-north-coherent-v1/frames/swim-north/000.png').convert('RGBA'));sr=swim[:,:,:3].astype(float);sy,sx=np.indices(swim.shape[:2])
 hair=(raw[:,:,3]>180)&(abs(xx-637)<85)&(yy>=53)&(yy<195)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2]);hair_ref=(swim[:,:,3]>180)&(abs(sx-104)<12)&(sy>=48)&(sy<57)&(sr[:,:,0]>1.12*sr[:,:,1])&(sr[:,:,1]>1.25*sr[:,:,2]);hair_gain=np.median(sr[hair_ref],axis=0)/np.median(rgb[hair],axis=0);graded[hair,:3]=np.clip(rgb[hair]*hair_gain,0,255).astype('uint8')
 cyan=(raw[:,:,3]>180)&(rgb[:,:,1]>1.4*rgb[:,:,0])&(rgb[:,:,2]>1.4*rgb[:,:,0])&(rgb[:,:,1]>60);cyan_ref=(swim[:,:,3]>180)&(sr[:,:,1]>1.4*sr[:,:,0])&(sr[:,:,2]>1.4*sr[:,:,0])&(sr[:,:,1]>60);cyan_gain=np.median(sr[cyan_ref],axis=0)/np.median(rgb[cyan],axis=0);graded[cyan,:3]=np.clip(rgb[cyan]*cyan_gain,0,255).astype('uint8')
 labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;k=int(counts.argmax());mask=binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0);y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];graded[~mask]=0
 scale=.105;head=(637,53);target=(128,104);im=Image.fromarray(graded).crop(box);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);pos=(round(target[0]-(head[0]-box[0])*scale),round(target[1]-(head[1]-box[1])*scale));plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos)
 record={'source':'sources/midpoint-detail-v6.png','sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'generation':'exec-fd35e1f1-d686-4c3a-b79b-4e1b9b974e36','sourcePose':0,'outputPose':3,'alphaComponent':k,'sourceBox':box,'sourceCrownAxis':head,'targetCrownAxis':target,'position':pos,'scale':scale,'ruler':'independent high-density source;fixed .105 skull scale,not silhouette normalization'}
 grade={'neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'burgundyGain':red_gain.tolist(),'crownGain':hair_gain.tolist(),'cyanGain':cyan_gain.tolist(),'scope':'one material curve per independent authored source using the same selected masters'}
 return plane,record,grade
