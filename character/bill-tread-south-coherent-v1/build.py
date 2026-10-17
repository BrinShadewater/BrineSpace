"""Deterministically package authored south stationary scull; no per-pose scale/exposure."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'sources/tread-v1.png'
AUTHORITY=HERE.parent/'crew-runtime-matte-v1/bill/frames/idle-south-breathing-v1/000.png'
HEADS=[(260, 38), (767, 38), (1274, 39), (259, 539), (768, 535), (1275, 540)]
SCALE=0.24

def main():
 raw=np.array(Image.open(SOURCE).convert('RGBA'));labs,n=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
 ids=sorted(np.argsort(counts)[-6:],key=lambda k:(int(np.where(labs==k)[0].min())//512,int(np.where(labs==k)[1].min())))
 rgb=raw[:,:,:3].astype(float);neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22)
 a=np.array(Image.open(AUTHORITY).convert('RGBA'));ar=a[:,:,:3].astype(float);yy,xx=np.indices(a.shape[:2]);target=(a[:,:,3]>200)&(yy>53)&(np.ptp(ar,axis=2)<22)
 q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(ar.mean(2)[target],q)
 settings={'quantiles':q,'input':src.tolist(),'output':dst.tolist(),'scope':'single atlas-wide neutral curve; warm face/hair and burgundy/cyan excluded','authority':str(AUTHORITY.relative_to(HERE.parent))}
 mapped=np.interp(rgb.mean(2),src,dst);weight=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 region=np.zeros(raw.shape[:2],bool);sy,sx=np.indices(raw.shape[:2])
 for hx,hy in HEADS:region|=(np.abs(sx-hx)>42)&(np.abs(sx-hx)<155)&(sy>hy+50)&(sy<hy+155)
 patch=region&(raw[:,:,3]>200)&(rgb[:,:,0]>rgb[:,:,1]*1.4)&(rgb[:,:,0]>rgb[:,:,2]*1.4)
 ref_patch=(a[:,:,3]>200)&(yy>53)&(ar[:,:,0]>ar[:,:,1]*1.4)&(ar[:,:,0]>ar[:,:,2]*1.4)
 patch_gain=np.median(ar[ref_patch],axis=0)/np.median(rgb[patch],axis=0)
 pq=[0,.1,.35,.5,.7,.9,1]
 psrc=np.quantile(rgb[patch],pq,axis=0);pdst=np.quantile(ar[ref_patch],pq,axis=0)
 settings.update(burgundyQuantiles=pq,burgundyInput=psrc.tolist(),burgundyOutput=pdst.tolist(),burgundyTargetMedian=np.median(ar[ref_patch],axis=0).tolist(),burgundySourceMedian=np.median(rgb[patch],axis=0).tolist())
 graded=raw.copy();graded[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+mapped[:,:,None]*weight[:,:,None],0,255).astype('uint8');
 for channel in range(3):graded[patch,channel]=np.clip(np.interp(rgb[patch,channel],psrc[:,channel],pdst[:,channel]),0,255).astype('uint8')
 hair_region=np.zeros(raw.shape[:2],bool)
 for hx,hy in HEADS:hair_region|=(sx>hx-40)&(sx<hx+40)&(sy>=hy)&(sy<hy+35)
 hair=hair_region&(raw[:,:,3]>180)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,0]<1.95*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])
 ref_hair=(a[:,:,3]>180)&(yy>=25)&(yy<32)&(ar[:,:,0]>1.12*ar[:,:,1])&(ar[:,:,0]<1.95*ar[:,:,1])&(ar[:,:,1]>1.25*ar[:,:,2])
 hair_gain=np.median(ar[ref_hair],axis=0)/np.median(rgb[hair],axis=0)
 graded[hair,:3]=np.clip(rgb[hair]*hair_gain,0,255).astype('uint8')
 settings.update(hairGain=hair_gain.tolist(),hairSourceMedian=np.median(rgb[hair],axis=0).tolist(),hairTargetMedian=np.median(ar[ref_hair],axis=0).tolist(),scope='frozen atlas neutral,anatomical shoulder and crown-hair curves;ear skin excluded by red ratio')
 frames=[];records=[];hashes={}
 for i,k in enumerate(ids):
  mask=binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0);y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
  pix=graded.copy();pix[~mask]=0;im=Image.fromarray(pix).crop(box);size=(round(im.width*SCALE),round(im.height*SCALE));im=im.resize(size,Image.Resampling.LANCZOS)
  anchor=HEADS[i];pos=(round(92-(anchor[0]-box[0])*SCALE),round(34-(anchor[1]-box[1])*SCALE))
  out=Image.new('RGBA',(184,184));out.alpha_composite(im,pos);path=HERE/'frames/tread-south'/f'{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);out.save(path);frames.append(out)
  rel=path.relative_to(HERE).as_posix();hashes[rel]=hashlib.sha256(path.read_bytes()).hexdigest();records.append({'sourceComponent':int(k),'sourceBox':box,'headCrownAxis':anchor,'position':pos,'scale':SCALE})
 files=list(hashes);state={'id':'tread-south','frameFiles':files,'frameDurationsMs':[160]*6,'loop':True,'facings':['south']*6,'waterKinds':['tread']*6,'waterPoses':[True]*6,'depthOffsets':[0]*6}
 manifest={'name':'Bill master-relative south tread candidate','frameWidth':184,'frameHeight':184,'pivot':[92,70],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'owner_visual_review_pending','integration':'selected_by_grid_canvas_2026_09_30','strideDistanceCells':{},'states':[state]}
 registration={'source':'sources/tread-v1.png','sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'sourceGeneration':'exec-17febbba-0c91-4d4b-ae70-b1a959d1789c','originalGeneration':'exec-17febbba-0c91-4d4b-ae70-b1a959d1789c','scale':SCALE,'anchor':'shared head-crown y34/head-axis x92; anatomical scale 0.24 frozen across six poses; front head width ruler matches selected south idle,not a universal source pixel scale; no bounding-height normalization','frames':records}
 for name,obj in [('manifest.json',manifest),('registration.json',registration),('material-grade.json',settings),('frame-hashes.json',hashes)]: (HERE/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 contact=Image.new('RGB',(1104,220),(29,43,51));d=ImageDraw.Draw(contact)
 for i,im in enumerate(frames):contact.paste(im,(184*i,22),im);d.text((184*i+6,6),str(i),fill='white')
 contact.save(HERE/'contact-sheet.png')
 plate=Image.new('RGB',(1104,400),(29,43,51));d=ImageDraw.Draw(plate)
 for row,bg in enumerate([(29,43,51),(218,225,224)]):
  d.rectangle((0,row*200,1104,row*200+199),fill=bg)
  for i,im in enumerate(frames):
   for j,height in enumerate([82,54]):
    s=height/148;thumb=im.resize((round(184*s),round(184*s)),Image.Resampling.LANCZOS);plate.paste(thumb,(184*i+104-round(92*s),row*200+j*90+75-round(70*s)),thumb)
 plate.save(HERE/'gameplay-review.png')
 print('Built six south treading poses; fixed 0.24 scale; 960ms loop; staged')
if __name__=='__main__':main()
