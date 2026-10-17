"""Author pitch interiors between exact padded new tread/swim endpoints."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent
HEADS=[(274,48),(767,56),(1278,83),(274,593),(775,583),(1281,583)]
TARGET=[(128,92),(128,95),(128,98),(128,100),(128,102),(128,104)]
SCALE=.25;TIMES=[70,90,100,100,90,70]
AUTHORITIES=['bill-tread-north-coherent-v1/frames/tread-north/000.png','bill-swim-north-coherent-v1/frames/swim-north/000.png']
def endpoint(file,offset):
 im=Image.open(HERE.parent/file).convert('RGBA');out=Image.new('RGBA',(256,256));out.alpha_composite(im,offset);return out
def main():
 source=HERE/'sources/transition-v1.png';raw=np.array(Image.open(source).convert('RGBA'));labs,n=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
 ids=sorted(np.argsort(counts)[-6:],key=lambda k:(int(np.where(labs==k)[0].min())//512,int(np.where(labs==k)[1].min())))
 rgb=raw[:,:,:3].astype(float);neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22)
 a=np.array(Image.open(HERE.parent/'crew-runtime-matte-v1/bill/frames/idle-north-breathing-v1/000.png').convert('RGBA'));ar=a[:,:,:3].astype(float);yy,xx=np.indices(a.shape[:2]);target=(a[:,:,3]>200)&(yy>53)&(np.ptp(ar,axis=2)<22)
 q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(ar.mean(2)[target],q)
 settings={'quantiles':q,'input':src.tolist(),'output':dst.tolist(),'scope':'single atlas-wide neutral curve; warm face/hair and burgundy/cyan excluded','authority':'crew-runtime-matte-v1/bill/frames/idle-north-breathing-v1/000.png'}
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
 for hx,hy in HEADS:hair_region|=(sx>hx-40)&(sx<hx+40)&(sy>=hy)&(sy<hy+54)
 hair=hair_region&(raw[:,:,3]>180)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,0]<1.95*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])
 ref_hair=(a[:,:,3]>180)&(yy>=25)&(yy<42)&(ar[:,:,0]>1.12*ar[:,:,1])&(ar[:,:,0]<1.95*ar[:,:,1])&(ar[:,:,1]>1.25*ar[:,:,2])
 hair_gain=np.median(ar[ref_hair],axis=0)/np.median(rgb[hair],axis=0)
 graded[hair,:3]=np.clip(rgb[hair]*hair_gain,0,255).astype('uint8')
 settings.update(hairGain=hair_gain.tolist(),hairSourceMedian=np.median(rgb[hair],axis=0).tolist(),hairTargetMedian=np.median(ar[ref_hair],axis=0).tolist(),scope='frozen atlas neutral,anatomical shoulder and rear-hair curves;ear skin excluded by red ratio')
 frames=[endpoint(AUTHORITIES[0],(36,58))];records=[]
 for i in [1,2,3,4]:
  mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
  a=graded.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.LANCZOS)
  pos=(round(TARGET[i][0]-(HEADS[i][0]-box[0])*SCALE),round(TARGET[i][1]-(HEADS[i][1]-box[1])*SCALE));out=Image.new('RGBA',(256,256));out.alpha_composite(im,pos);frames.append(out);records.append({'sourceCell':i,'sourceBox':box,'sourceHead':HEADS[i],'targetHead':TARGET[i],'position':pos,'scale':SCALE})
 frames.append(endpoint(AUTHORITIES[1],(24,56)))
 manifest={'name':'Bill exact-endpoint north swim pitch transitions','frameWidth':256,'frameHeight':256,'pivot':[128,128],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'owner_visual_review_pending','integration':'selected_by_grid_canvas_2026_09_30','states':[]};hashes={}
 for key,ims,kinds in [('swim-start-north',frames,['tread']+['swim']*5),('swim-stop-north',list(reversed(frames)),['swim']*5+['tread'])]:
  files=[]
  for i,im in enumerate(ims):
   file=f'frames/{key}/{i:03}.png';path=HERE/file;path.parent.mkdir(parents=True,exist_ok=True);im.save(path);files.append(file);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest()
  manifest['states'].append({'id':key,'frameFiles':files,'frameDurationsMs':TIMES,'loop':False,'facings':['north']*6,'waterKinds':kinds,'waterPoses':[True]*6,'depthOffsets':[0]*6,'provenance':'four authored pitch interiors; exact padded new tread/swim endpoints; stop derived in reverse without mirroring'})
 registration={'source':'sources/transition-v1.png','sourceGeneration':'exec-8199cf9d-d2ab-4bb5-bef8-ca045f99fdf7','sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':SCALE,'omittedSourceCells':[0,5],'endpointAuthorities':AUTHORITIES,'endpointOffsets':[[36,58],[24,56]],'frames':records}
 for name,obj in [('manifest.json',manifest),('registration.json',registration),('frame-hashes.json',hashes),('material-grade.json',settings)]:(HERE/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 contact=Image.new('RGB',(1536,256),(29,43,51));d=ImageDraw.Draw(contact)
 for i,im in enumerate(frames):contact.paste(im,(256*i,0),im);d.text((256*i+5,5),str(i),fill='white')
 contact.save(HERE/'contact-sheet.png');print('Built start/stop: four authored interiors, exact registered endpoints; 520ms each')
if __name__=='__main__':main()
