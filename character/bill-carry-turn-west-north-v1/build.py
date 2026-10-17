"""Register authored whole-figure turn poses with exact selected cargo endpoints."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'bill-cargo-east-coherent-v1'))
from matte_grade import calibrate,grade
from turn_material import match
ENDPOINTS=[HERE.parent/'bill-cargo-west-coherent-v1/frames/pickup-west/011.png',HERE.parent/'bill-cargo-north-coherent-v1/frames/pickup-north/011.png']

def main():
 raw=np.array(Image.open(HERE/'sources/turn-v1.png').convert('RGBA')); h,w=raw.shape[:2]; masks=[];boxes=[]
 for i in range(6):
  x0=(i%3)*w//3;y0=(i//3)*h//2
  cell=raw[y0:y0+h//2,x0:x0+w//3];labs,n=label(cell[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;ident=int(counts.argmax())
  mask=np.zeros((h,w),bool);mask[y0:y0+h//2,x0:x0+w//3]=labs==ident;masks.append(mask)
  yy,xx=np.where(mask);boxes.append([int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)])
 endpoints=[Image.open(p).convert('RGBA') for p in ENDPOINTS]
 heights=[im.getchannel('A').getbbox()[3]-im.getchannel('A').getbbox()[1] for im in endpoints]
 scale=float(np.mean(heights)/np.mean([boxes[i][3]-boxes[i][1] for i in [0,5]]))
 # Freeze horizontal anatomy calibration from both neutral endpoint shoulders,
 # above the cargo case. Projected widths naturally change through rotation.
 ratios=[];endpoint_width_scales=[]
 for end,cell in zip(endpoints,[0,5]):
  endpoint_ratios=[]
  target=np.array(end);target_top=end.getchannel('A').getbbox()[1];source_top=boxes[cell][1]
  for offset in range(28,41,2):
   tx=np.where(target[target_top+offset,:,3]>180)[0]
   sx=np.where(masks[cell][round(source_top+offset/scale)])[0]
   if len(tx) and len(sx):endpoint_ratios.append(float((tx.max()-tx.min()+1)/(sx.max()-sx.min()+1)))
  endpoint_width_scales.append(float(np.median(endpoint_ratios)));ratios.extend(endpoint_ratios)
 # Use the narrower endpoint calibration throughout so a front-to-diagonal
 # source cannot introduce the bulk increase rejected in the preceding turn.
 scale_x=min(endpoint_width_scales)
 idle=Image.open(HERE.parent/'crew-runtime-matte-v1/bill/frames/idle-north-transition-matte-v1/000.png').convert('RGBA')
 settings=calibrate(raw,masks[0],idle,authority='crew-runtime-matte-v1/bill/frames/idle-north-transition-matte-v1/000.png',facing='north');records=[];frames=[endpoints[0]]
 axes=[]
 for im in endpoints:
  arr=np.array(im);ys,xs=np.where(arr[:,:,3]>180);hy,hx=np.where((arr[:,:,3]>180)&(np.indices(arr.shape[:2])[0]<ys.min()+8));axes.append(float((hx.min()+hx.max())/2))
 for index,cell in enumerate([1,2,3,4]):
  mask=masks[cell];yy,xx=np.where(mask);by=int(yy.min());bottom=int(yy.max());hy,hx=np.where(mask&(np.indices(mask.shape)[0]<by+35));cx=(hx.min()+hx.max())/2
  box=boxes[cell];box=[box[0]-3,box[1]-3,box[2]+3,box[3]+3]
  isolated=raw.copy();isolated[~binary_dilation(mask,iterations=2)]=0
  graded,_=grade(isolated,mask,settings);im=Image.fromarray(graded).crop(box);im=im.resize((round(im.width*scale_x),round(im.height*scale)),Image.Resampling.LANCZOS)
  t=(index+1)/5;target_x=axes[0]*(1-t)+axes[1]*t;pos=(round(target_x-(cx-box[0])*scale_x),round(223-(bottom-box[1])*scale))
  canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,pos);frames.append(canvas)
  records.append({'sourceCell':cell,'sourceBox':box,'position':list(pos),'scale':scale,'scaleX':scale_x,'headAxisSourceX':float(cx),'targetHeadAxisX':target_x})
 frames.append(endpoints[1]);durations=[100,120,140,160,160,120]
 for i,im in enumerate(frames):
  path=HERE/'review-ungraded/frames/carry-turn-west-north'/f'{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
 frames,turn_grade=match(frames)
 (HERE/'turn-material-grade.json').write_text(json.dumps(turn_grade,indent=2)+'\n')
 manifest={'name':'Bill west/north authored cargo turn','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'owner_visual_accepted_staged_2026_09_30_turn_v1','states':[]};hashes={}
 for key,images,times,facings in [('carry-turn-west-north',frames,durations,['west','west','north','north','north','north']),('carry-turn-north-west',list(reversed(frames)),list(reversed(durations)),['north','north','north','north','west','west'])]:
  files=[]
  for i,im in enumerate(images):
   path=HERE/'frames'/key/f'{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);file=path.relative_to(HERE).as_posix();files.append(file);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest()
  manifest['states'].append({'id':key,'frameFiles':files,'frameDurationsMs':times,'loop':False,'water':False,'facings':facings,'provenance':'stationary pivot source cells1/2/3/4;exact loaded neutral pickup endpoints;reverse derived without mirroring'})
 for file,obj in [('manifest.json',manifest),('frame-hashes.json',hashes),('registration.json',{'source':'sources/turn-v1.png','sourceSha256':hashlib.sha256((HERE/'sources/turn-v1.png').read_bytes()).hexdigest(),'scale':scale,'scaleX':scale_x,'widthCalibration':'one frozen shoulder-width calibration from both neutral cardinal authorities;no per-pose normalization','omittedSourceCells':[0,5],'endpointAuthorities':[p.relative_to(HERE.parent).as_posix() for p in ENDPOINTS],'material':settings,'frames':records})]:
  (HERE/file).write_text(json.dumps(obj,indent=2)+'\n')
 out=Image.new('RGB',(1536,256),(29,43,51));draw=ImageDraw.Draw(out)
 for i,im in enumerate(frames):out.paste(im,(i*256,0),im);draw.text((i*256+8,8),str(i),fill='white')
 out.save(HERE/'contact-sheet.png')
 # Actual station-scale samples on light and dark backgrounds.
 review=Image.new('RGB',(600,360));draw=ImageDraw.Draw(review)
 for row,(bg,height) in enumerate([((29,43,51),82),((218,225,224),82),((29,43,51),54),((218,225,224),54)]):
  draw.rectangle((0,row*90,600,row*90+89),fill=bg)
  for i,im in enumerate(frames):
   s=height/148;sample=im.resize((round(256*s),round(256*s)),Image.Resampling.LANCZOS);review.paste(sample,(i*100+50-round(128*s),row*90+87-round(224*s)),sample)
 review.save(HERE/'gameplay-review.png');print('Built 2 stationary turns,12 references,6 unique poses;800ms retained quarter-turn duration;fixed scale',round(scale,5))

if __name__=='__main__':main()
