"""Package four authored pitch interiors with exact selected idle/swim endpoints."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent
SOURCE=P/'sources/interiors-v2.png';IDLE=R/'crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png';SWIM=R/'bill-swim-east-coherent-v1/frames/swim-east/000.png'
SCALE=.27
HEADS=[(448,49),(1175,59),(520,633),(1333,679)]
TARGETS=[(171,88),(177,118),(183,157),(187,188)]
TIMES=[60,90,100,100,90,60]
def padded(path,pivot):
 out=Image.new('RGBA',(320,320));im=Image.open(path).convert('RGBA');out.alpha_composite(im,(160-pivot[0],224-pivot[1]));return out
def main():
 raw=np.array(Image.open(SOURCE).convert('RGBA'));labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());ids=np.argsort(counts[1:])[-4:]+1
 ids=sorted(ids,key=lambda n:(int(np.where(labs==n)[0].min())//512,int(np.where(labs==n)[1].min())))
 rgb=raw[:,:,:3].astype(float);reference=np.array(Image.open(IDLE).convert('RGBA'));ref=reference[:,:,:3].astype(float)
 rr,cc=np.indices(reference.shape[:2]);neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22)
 target=(reference[:,:,3]>200)&(rr>52)&(np.ptp(ref,axis=2)<22)
 quantiles=[0,.05,.15,.35,.50,.70,.85,.95,.98,1]
 src=np.quantile(rgb.mean(2)[neutral],quantiles);dst=np.quantile(ref.mean(2)[target],quantiles)
 mapped=np.interp(rgb.mean(2),src,dst);weight=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 graded=raw.copy();graded[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+mapped[:,:,None]*weight[:,:,None],0,255).astype('uint8')
 # One atlas-wide material curve; warm skin/hair and coloured accents remain unpainted.
 frames=[padded(IDLE,(92,172))];records=[]
 for i,n in enumerate(ids):
  mask=binary_dilation(labs==n,iterations=3)&(raw[:,:,3]>0)
  ys,xs=np.where(mask);box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
  pixels=graded.copy();pixels[~mask]=0;pose=Image.fromarray(pixels).crop(box)
  pose=pose.resize((round(pose.width*SCALE),round(pose.height*SCALE)),Image.Resampling.LANCZOS)
  pos=(round(TARGETS[i][0]-(HEADS[i][0]-box[0])*SCALE),round(TARGETS[i][1]-(HEADS[i][1]-box[1])*SCALE))
  out=Image.new('RGBA',(320,320));out.alpha_composite(pose,pos);frames.append(out)
  records.append({'component':int(n),'sourceBox':box,'sourceCrown':HEADS[i],'targetCrown':TARGETS[i],'position':pos,'scale':SCALE})
 frames.append(padded(SWIM,(122,88)))
 manifest={'name':'Bill staged bare East land/water pose bridge','frameWidth':320,'frameHeight':320,'pivot':[160,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'source_study_unselected','states':[]}
 for key,poses in [('land-swim-east',frames),('swim-land-east',list(reversed(frames)))]:
  files=[]
  for i,im in enumerate(poses):
   file=f'frames/{key}/{i:03}.png';path=P/file;path.parent.mkdir(parents=True,exist_ok=True);im.save(path);files.append(file)
  manifest['states'].append({'id':key,'frameFiles':files,'frameDurationsMs':TIMES,'loop':False,'facings':['east']*6,'waterKinds':['swim']*6,'waterPoses':[True]*6,'provenance':'Four generated articulated interiors; exact padded selected endpoints. Exit source order derived in reverse, not separately authored. No runtime admission.'})
 # Preserve source authority pixels, including transparency; no endpoint grading.
 assert frames[0].crop((68,52,252,236)).tobytes()==Image.open(IDLE).convert('RGBA').tobytes()
 assert frames[-1].crop((38,136,246,320)).tobytes()==Image.open(SWIM).convert('RGBA').tobytes()
 for name,data in [('manifest.json',manifest),('registration.json',{'generation':'exec-3ce1558c-4157-46d6-90cf-b0ce2a737118','sourceSHA256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'scale':SCALE,'interiors':records,'scope':'Fixed anatomical source scale. Prescribed crown trajectory into original shoulder-pivot swim endpoint; physical water/floor support not yet accepted.'}),('material-grade.json',{'quantiles':quantiles,'input':src.tolist(),'output':dst.tolist(),'scope':'One atlas-wide neutral-only curve against selected idle; warm skin/hair/burgundy preserved. No per-pose exposure.'})]:
  (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1920,340),'#182932');draw=ImageDraw.Draw(board)
 for i,im in enumerate(frames):board.paste(im,(i*320,20),im);draw.text((i*320+5,5),['Original idle','Interior 1','Interior 2','Interior 3','Interior 4','Original swim'][i],fill='white')
 board.save(P/'source-review.png')
 frames[0].save(P/'source-enter.png',save_all=True,append_images=frames[1:],duration=TIMES,loop=0,disposal=0,blend=0)
 reverse=list(reversed(frames));reverse[0].save(P/'source-leave.png',save_all=True,append_images=reverse[1:],duration=TIMES,loop=0,disposal=0,blend=0)
 (P/'source-evidence.json').write_text(json.dumps({'endpointRGBAExact':True,'fourAuthoredInteriors':True,'allInteriorScale':SCALE,'sourceOnly':True,'normalProductionSelected':False,'frameSHA256':{f.relative_to(P).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in (P/'frames').rglob('*.png')}},indent=2)+'\n',encoding='utf-8')
 print('Built source-only 500ms East bridge; both original endpoints remain byte-exact.')
if __name__=='__main__':main()
