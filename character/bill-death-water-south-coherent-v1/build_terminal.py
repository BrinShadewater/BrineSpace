"""Independently authored limp terminal; fixed south anatomical source ruler."""
from pathlib import Path
import hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
def build():
 source=P/'sources/terminal-v3.png';raw=np.array(Image.open(source).convert('RGBA'));rgb=raw[:,:,:3].astype(float);yy,xx=np.indices(raw.shape[:2])
 ref=np.array(Image.open(P.parent/'crew-runtime-matte-v1/bill/frames/idle-south-breathing-v1/000.png').convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
 neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22);authority=(ref[:,:,3]>200)&(ry>53)&(np.ptp(rr,axis=2)<22);q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1]
 src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(rr.mean(2)[authority],q);mapped=np.interp(rgb.mean(2),src,dst);w=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 graded=raw.copy();graded[:,:,:3]=np.clip(rgb*(1-w[:,:,None])+mapped[:,:,None]*w[:,:,None],0,255).astype('uint8')
 red=(raw[:,:,3]>200)&(yy>750)&((xx<490)|(xx>750))&(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2]);red_ref=(ref[:,:,3]>200)&(ry>53)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2]);gain=np.median(rr[red_ref],axis=0)/np.median(rgb[red],axis=0);graded[red,:3]=np.clip(rgb[red]*gain,0,255).astype('uint8')
 swim=np.array(Image.open(P.parent/'bill-swim-south-coherent-v1/frames/swim-south/000.png').convert('RGBA'));sr=swim[:,:,:3].astype(float);sy,sx=np.indices(swim.shape[:2])
 hair=(raw[:,:,3]>180)&(abs(xx-625)<125)&(yy>=770)&(yy<960)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2]);hair_ref=(swim[:,:,3]>180)&(abs(sx-104)<12)&(sy>=134)&(sy<143)&(sr[:,:,0]>1.12*sr[:,:,1])&(sr[:,:,1]>1.25*sr[:,:,2]);hg=np.median(sr[hair_ref],axis=0)/np.median(rgb[hair],axis=0);graded[hair,:3]=np.clip(rgb[hair]*hg,0,255).astype('uint8')
 cyan=(raw[:,:,3]>180)&(rgb[:,:,1]>1.4*rgb[:,:,0])&(rgb[:,:,2]>1.4*rgb[:,:,0])&(rgb[:,:,1]>60);cr=(swim[:,:,3]>180)&(sr[:,:,1]>1.4*sr[:,:,0])&(sr[:,:,2]>1.4*sr[:,:,0])&(sr[:,:,1]>60);cg=np.median(sr[cr],axis=0)/np.median(rgb[cyan],axis=0);graded[cyan,:3]=np.clip(rgb[cyan]*cg,0,255).astype('uint8')
 labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;k=int(counts.argmax());mask=binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0);y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];graded[~mask]=0
 scale=.09;head=(625,761);target=(128,110);im=Image.fromarray(graded).crop(box);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);pos=(round(target[0]-(head[0]-box[0])*scale),round(target[1]-(head[1]-box[1])*scale));plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos)
 record={'source':'sources/terminal-v3.png','sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'generation':'exec-7e8548f5-6407-406e-81c7-7ed55678d951','sourcePose':0,'outputPose':5,'sourceBox':box,'sourceCrownAxis':head,'targetCrownAxis':target,'position':pos,'scale':scale,'ruler':'independent high-density fullfigure;fixed .09 skull and crown-to-sole ruler'}
 grade={'neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'burgundyGain':gain.tolist(),'crownGain':hg.tolist(),'cyanGain':cg.tolist(),'authority':'selected south idle and swim'}
 return plane,record,grade
