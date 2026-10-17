"""Native selected dry helmet follows authored head positions and tilts."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;BARE=P.parent/'bill-seated-west-coherent-v1';DONOR=P.parent/'bill-shared-helmet-runtime-v2'
def main():
 manifest=json.loads((BARE/'manifest.json').read_text(encoding='utf-8'));r=json.loads((BARE/'registration.json').read_text(encoding='utf-8'));dm=json.loads((DONOR/'manifest.json').read_text(encoding='utf-8'));ds=next(s for s in dm['states'] if s['id']=='idle-west');idle=Image.open(DONOR/ds['frameFiles'][0]).convert('RGBA')
 box=(72,20,107,58);head=idle.crop(box);mask=Image.new('L',head.size);ImageDraw.Draw(mask).polygon([(0,0),(35,0),(35,25),(23,26),(15,32),(8,38),(0,38)],fill=255);a=np.array(head);a[:,:,3]=np.minimum(a[:,:,3],np.array(mask));head=Image.fromarray(a);source=P/'sources/canonical-head.png';source.parent.mkdir(parents=True,exist_ok=True);head.save(source)
 rows={record['frame']:record for record in r['frames']};images=[];records=[];hashes={};yy,xx=np.indices((256,256))
 for i,file in enumerate(manifest['states'][0]['frameFiles']):
  bare=np.array(Image.open(BARE/file).convert('RGBA'))
  if i==0:
   result=Image.new('RGBA',(256,256));result.paste(idle,(36,52))
  else:
   row=rows[i];hx,hy=row['headAxis'];angle=row['headTiltDegrees'];tilted=head.rotate(-angle,resample=Image.Resampling.BICUBIC,expand=True)
   radians=math.radians(angle);dx=20-head.width/2;dy=4-head.height/2;anchor=(tilted.width/2+math.cos(radians)*dx-math.sin(radians)*dy,tilted.height/2+math.sin(radians)*dx+math.cos(radians)*dy);position=(round(hx-anchor[0]),round(hy-anchor[1]))
   br=bare[:,:,:3].astype(float);warm=(br[:,:,0]>1.12*br[:,:,1])&(br[:,:,1]>1.14*br[:,:,2]);erase=(xx>=hx-14)&(xx<=hx+16)&(yy>=hy-2)&(yy<hy+31)&warm
   out=bare.copy();out[erase]=0;result=Image.fromarray(out);result.alpha_composite(tilted,position);a=np.array(result);protected=hy+31;a[protected:]=bare[protected:];result=Image.fromarray(a)
   records.append({'frame':i,'headAxis':[hx,hy],'tiltDegrees':angle,'position':position,'nativeScale':1,'protectedBodyFromY':protected,'bareSha256':hashlib.sha256((BARE/file).read_bytes()).hexdigest()})
  dest=P/file;dest.parent.mkdir(parents=True,exist_ok=True);result.save(dest);hashes[file]=hashlib.sha256(dest.read_bytes()).hexdigest();images.append(result)
 manifest.update(name='Bill west helmet sitting candidate',equipment='diving-helmet');manifest['states'][0]['provenance']='native selected dry helmet shell follows authored head tilt;original body/legs preserved;exact equipped standing endpoint;original body preserved'
 reg={'donor':(DONOR/ds['frameFiles'][0]).relative_to(P.parent).as_posix(),'donorSha256':hashlib.sha256((DONOR/ds['frameFiles'][0]).read_bytes()).hexdigest(),'sourceBox':box,'component':'sources/canonical-head.png','componentSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'nativeScale':1,'frames':records,'maskPolygon':[(0,0),(35,0),(35,25),(23,26),(15,32),(8,38),(0,38)]}
 for name,data in [('manifest.json',manifest),('helmet-registration.json',reg),('frame-hashes.json',hashes)]: (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(29,43,51))
 for i,im in enumerate(images):board.paste(im,(i*256,0),im);b=Image.open(BARE/manifest['states'][0]['frameFiles'][i]);board.paste(b,(i*256,256),b)
 board.save(P/'contact-sheet.png');print('Built west helmet recovery;native tilted head;exact idle ends')
if __name__=='__main__':main()
