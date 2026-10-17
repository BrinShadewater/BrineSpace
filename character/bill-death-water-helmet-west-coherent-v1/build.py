"""Fit the exact selected west swimming helmet at its native pixel scale."""
from pathlib import Path
import copy,hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-death-water-west-coherent-v1'
DONOR=HERE.parent/'bill-swim-helmet-west-coherent-v1'
def main():
 p=json.loads((BARE/'manifest.json').read_text(encoding='utf-8'))
 source=DONOR/'sources/canonical-head.png';target=HERE/'sources/canonical-head.png';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())
 head=Image.open(target).convert('RGBA');closed=head.copy();eye_source=HERE/'sources/closed-eye-v1.png';eye=Image.open(eye_source).convert('RGBA').crop((270,565,415,638)).resize((5,3),Image.Resampling.LANCZOS);closed.paste(eye,(4,16));closed.save(HERE/'sources/canonical-closed-head.png');yy,xx=np.indices((256,256));images=[];records=[];hashes={}
 for i,file in enumerate(p['states'][0]['frameFiles']):
  b=np.array(Image.open(BARE/file).convert('RGBA'))
  if i==0:
   plane=Image.new('RGBA',(256,256));plane.alpha_composite(Image.open(DONOR/'frames/swim-west/000.png').convert('RGBA'),(42,40))
  else:
   br=b[:,:,:3].astype(float);warm=(br[:,:,0]>1.13*br[:,:,1])&(br[:,:,1]>1.14*br[:,:,2]);erase=(abs(xx-102)<=24)&(yy>=102)&(yy<135)&warm
   out=b.copy();out[erase]=0;plane=Image.fromarray(out);plane.alpha_composite(closed if i>=3 else head,(87,95));a=np.array(plane)
   foreground=(b[:,:,3]>0)&((yy>=135)|((xx<=96)&(yy>=127)))
   if i>=3:foreground&=~((xx>=84)&(xx<=110)&(yy>=125)&(yy<135))
   a[foreground]=b[foreground];a[129 if i>=3 else 135:]=b[129 if i>=3 else 135:];plane=Image.fromarray(a)
   records.append({'frame':i,'position':[87,95],'crownAxis':[102,104],'componentNativeScale':1,'expression':'authored closed eye patch' if i>=3 else 'selected open face','eraseBox':[78,102,127,135],'protectedBodyFromY':129 if i>=3 else 135,'foreground':'original opaque forward arm x<=96,y>=127;late head overlap x84..110/y125..134 excluded from restoration','bareSha256':hashlib.sha256((BARE/file).read_bytes()).hexdigest()})
  outpath=HERE/file;outpath.parent.mkdir(parents=True,exist_ok=True);plane.save(outpath);hashes[file]=hashlib.sha256(outpath.read_bytes()).hexdigest();images.append(plane)
 p.update(name='Bill west helmet underwater death candidate',equipment='diving-helmet')
 p['states'][0]['provenance']='native selected shell with authored late closed-eye patch;progressive death body;exact equipped swim entry'
 reg={'component':'sources/canonical-head.png','donor':'bill-swim-helmet-west-coherent-v1/sources/canonical-head.png','componentSha256':hashlib.sha256(target.read_bytes()).hexdigest(),'componentNativeScale':1,'expressionSource':'sources/closed-eye-v1.png','expressionSourceSha256':hashlib.sha256(eye_source.read_bytes()).hexdigest(),'eyeSourceBox':[270,565,415,638],'nativeEyeBox':[4,16,9,19],'endpointAuthority':'bill-swim-helmet-west-coherent-v1/frames/swim-west/000.png','endpointPadding':[42,40],'frames':records}
 for file,data in [('manifest.json',p),('helmet-registration.json',reg),('frame-hashes.json',hashes)]: (HERE/file).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(29,43,51))
 for i,im in enumerate(images):
  board.paste(im,(i*256,0),im);bare=Image.open(BARE/p['states'][0]['frameFiles'][i]);board.paste(bare,(i*256,256),bare)
 board.save(HERE/'contact-sheet.png');print('Built west helmet death;native shell,authored closed eye,exact entry')
if __name__=='__main__':main()
