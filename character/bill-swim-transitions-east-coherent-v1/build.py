"""Author pitch interiors between exact padded new tread/swim endpoints."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent
HEADS=[(290,57),(785,77),(1358,107),(376,622),(874,670),(1393,691)]
TARGET=[(136,92),(140,95),(144,98),(148,100),(152,103),(154,104)]
SCALE=.28;TIMES=[70,90,100,100,90,70]
AUTHORITIES=['bill-tread-east-coherent-v1/frames/tread-east/000.png','bill-swim-east-coherent-v1/frames/swim-east/000.png']
def endpoint(file,offset):
 im=Image.open(HERE.parent/file).convert('RGBA');out=Image.new('RGBA',(256,256));out.alpha_composite(im,offset);return out
def main():
 source=HERE/'sources/transition-v1.png';raw=np.array(Image.open(source).convert('RGBA'));labs,n=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
 ids=sorted(np.argsort(counts)[-6:],key=lambda k:(int(np.where(labs==k)[0].min())//512,int(np.where(labs==k)[1].min())))
 rgb=raw[:,:,:3].astype(float);neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22)
 ref=np.array(Image.open(HERE.parent/'crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png').convert('RGBA'));rr=ref[:,:,:3].astype(float);yy,xx=np.indices(ref.shape[:2]);valid=(ref[:,:,3]>200)&(yy>53)&(np.ptp(rr,axis=2)<22)
 q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(rr.mean(2)[valid],q);mapped=np.interp(rgb.mean(2),src,dst);weight=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 region=np.zeros(raw.shape[:2],bool);sy,sx=np.indices(raw.shape[:2])
 for hx,hy in HEADS:region|=(sx>hx-160)&(sx<hx-20)&(sy>hy+50)&(sy<hy+230)
 patch=region&(raw[:,:,3]>200)&(rgb[:,:,0]>rgb[:,:,1]*1.4)&(rgb[:,:,0]>rgb[:,:,2]*1.4)
 ref_patch=(ref[:,:,3]>200)&(yy>53)&(rr[:,:,0]>rr[:,:,1]*1.4)&(rr[:,:,0]>rr[:,:,2]*1.4)
 patch_gain=np.median(rr[ref_patch],axis=0)/np.median(rgb[patch],axis=0)
 graded=raw.copy();graded[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+mapped[:,:,None]*weight[:,:,None],0,255).astype('uint8');graded[patch,:3]=np.clip(rgb[patch]*patch_gain,0,255).astype('uint8')
 frames=[endpoint(AUTHORITIES[0],(36,58))];records=[]
 for i in [1,2,3,4]:
  mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
  a=graded.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.LANCZOS)
  pos=(round(TARGET[i][0]-(HEADS[i][0]-box[0])*SCALE),round(TARGET[i][1]-(HEADS[i][1]-box[1])*SCALE));out=Image.new('RGBA',(256,256));out.alpha_composite(im,pos);frames.append(out);records.append({'sourceCell':i,'sourceBox':box,'sourceHead':HEADS[i],'targetHead':TARGET[i],'position':pos,'scale':SCALE})
 frames.append(endpoint(AUTHORITIES[1],(6,40)))
 manifest={'name':'Bill exact-endpoint east swim pitch transitions','frameWidth':256,'frameHeight':256,'pivot':[128,128],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'owner_visual_review_pending','integration':'selected_by_grid_canvas_2026_09_30','states':[]};hashes={}
 for key,ims,kinds in [('swim-start-east',frames,['tread']+['swim']*5),('swim-stop-east',list(reversed(frames)),['swim']*5+['tread'])]:
  files=[]
  for i,im in enumerate(ims):
   file=f'frames/{key}/{i:03}.png';path=HERE/file;path.parent.mkdir(parents=True,exist_ok=True);im.save(path);files.append(file);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest()
  manifest['states'].append({'id':key,'frameFiles':files,'frameDurationsMs':TIMES,'loop':False,'facings':['east']*6,'waterKinds':kinds,'waterPoses':[True]*6,'depthOffsets':[0]*6,'provenance':'four authored pitch interiors; exact padded new tread/swim endpoints; stop derived in reverse without mirroring'})
 registration={'source':'sources/transition-v1.png','sourceGeneration':'exec-4ef23b43-61cf-4591-88f4-c943d2ff9cd1','sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':SCALE,'omittedSourceCells':[0,5],'endpointAuthorities':AUTHORITIES,'endpointOffsets':[[36,58],[6,40]],'frames':records}
 for name,obj in [('manifest.json',manifest),('registration.json',registration),('frame-hashes.json',hashes),('material-grade.json',{'input':src.tolist(),'output':dst.tolist(),'scope':'atlas-wide frozen neutral and shoulder burgundy curves;selected east idle authority','burgundyGain':patch_gain.tolist(),'burgundySourceMedian':np.median(rgb[patch],axis=0).tolist(),'burgundyTargetMedian':np.median(rr[ref_patch],axis=0).tolist()})]:(HERE/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 contact=Image.new('RGB',(1536,256),(29,43,51));d=ImageDraw.Draw(contact)
 for i,im in enumerate(frames):contact.paste(im,(256*i,0),im);d.text((256*i+5,5),str(i),fill='white')
 contact.save(HERE/'contact-sheet.png');print('Built start/stop: four authored interiors, exact registered endpoints; 520ms each')
if __name__=='__main__':main()
