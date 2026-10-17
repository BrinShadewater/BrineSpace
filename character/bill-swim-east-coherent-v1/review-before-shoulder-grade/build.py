"""Deterministically package authored east stroke; no per-pose scale/exposure."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'sources/swim-alpha-v2.png'
AUTHORITY=HERE.parent/'crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png'
HEADS=[(393,164),(920,164),(1440,165),(407,613),(920,612),(1425,614)]
SCALE=.28

def main():
 raw=np.array(Image.open(SOURCE).convert('RGBA'));labs,n=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
 ids=sorted(np.argsort(counts)[-6:],key=lambda k:(int(np.where(labs==k)[0].min())//512,int(np.where(labs==k)[1].min())))
 rgb=raw[:,:,:3].astype(float);neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22)
 a=np.array(Image.open(AUTHORITY).convert('RGBA'));ar=a[:,:,:3].astype(float);yy,xx=np.indices(a.shape[:2]);target=(a[:,:,3]>200)&(yy>53)&(np.ptp(ar,axis=2)<22)
 q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(ar.mean(2)[target],q)
 settings={'quantiles':q,'input':src.tolist(),'output':dst.tolist(),'scope':'single atlas-wide neutral curve; warm face/hair and burgundy/cyan excluded','authority':str(AUTHORITY.relative_to(HERE.parent))}
 mapped=np.interp(rgb.mean(2),src,dst);weight=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 graded=raw.copy();graded[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+mapped[:,:,None]*weight[:,:,None],0,255).astype('uint8')
 frames=[];records=[];hashes={}
 for i,k in enumerate(ids):
  mask=binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0);y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
  pix=graded.copy();pix[~mask]=0;im=Image.fromarray(pix).crop(box);size=(round(im.width*SCALE),round(im.height*SCALE));im=im.resize(size,Image.Resampling.LANCZOS)
  anchor=HEADS[i];pos=(round(148-(anchor[0]-box[0])*SCALE),round(64-(anchor[1]-box[1])*SCALE))
  out=Image.new('RGBA',(208,184));out.alpha_composite(im,pos);path=HERE/'frames/swim-east'/f'{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);out.save(path);frames.append(out)
  rel=path.relative_to(HERE).as_posix();hashes[rel]=hashlib.sha256(path.read_bytes()).hexdigest();records.append({'sourceComponent':int(k),'sourceBox':box,'headCrownAxis':anchor,'position':pos,'scale':SCALE})
 files=list(hashes);state={'id':'swim-east','frameFiles':files,'frameDurationsMs':[160]*6,'loop':True,'facings':['east']*6,'waterKinds':['swim']*6,'waterPoses':[True]*6,'depthOffsets':[0]*6}
 manifest={'name':'Bill master-relative east swim candidate','frameWidth':208,'frameHeight':184,'pivot':[122,88],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'owner_visual_review_pending','integration':'selected_by_grid_canvas_2026_09_30','strideDistanceCells':{'swim':.16},'states':[state]}
 registration={'source':'sources/swim-alpha-v2.png','sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'sourceGeneration':'exec-97cb7f2f-7726-489f-ae5a-bb05dce772b5','originalGeneration':'exec-b0f05407-37eb-49e6-9aa5-108f6228a109','scale':SCALE,'anchor':'shared head-crown y64/head-axis x148; anatomical scale .28 frozen across six poses; no bounding-height normalization','frames':records}
 for name,obj in [('manifest.json',manifest),('registration.json',registration),('material-grade.json',settings),('frame-hashes.json',hashes)]: (HERE/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 contact=Image.new('RGB',(1248,240),(29,43,51));d=ImageDraw.Draw(contact)
 for i,im in enumerate(frames):contact.paste(im,(208*i,22),im);d.text((208*i+6,6),str(i),fill='white')
 contact.save(HERE/'contact-sheet.png')
 plate=Image.new('RGB',(1248,400),(29,43,51));d=ImageDraw.Draw(plate)
 for row,bg in enumerate([(29,43,51),(218,225,224)]):
  d.rectangle((0,row*200,1248,row*200+199),fill=bg)
  for i,im in enumerate(frames):
   for j,height in enumerate([82,54]):
    s=height/148;thumb=im.resize((round(208*s),round(184*s)),Image.Resampling.LANCZOS);plate.paste(thumb,(208*i+104-round(122*s),row*200+j*90+75-round(88*s)),thumb)
 plate.save(HERE/'gameplay-review.png')
 print('Built six east swimming poses; fixed .28 scale; 960ms loop; staged')
if __name__=='__main__':main()
