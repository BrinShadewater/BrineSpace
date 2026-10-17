"""Fit the exact selected east swimming helmet at its native pixel scale."""
from pathlib import Path
import copy,hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-salvage-east-coherent-v1'
DONOR=HERE.parent/'bill-swim-helmet-east-coherent-v1'
def main():
 p=json.loads((BARE/'manifest.json').read_text(encoding='utf-8'))
 source=DONOR/'sources/canonical-head.png';target=HERE/'sources/canonical-head.png';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())
 head=Image.open(target).convert('RGBA');yy,xx=np.indices((256,256));images=[];records=[];hashes={}
 for i,file in enumerate(p['states'][0]['frameFiles']):
  b=np.array(Image.open(BARE/file).convert('RGBA'))
  br=b[:,:,:3].astype(float);warm=(br[:,:,0]>1.13*br[:,:,1])&(br[:,:,1]>1.14*br[:,:,2]);erase=(abs(xx-154)<=24)&(yy>=102)&(yy<135)&warm
  out=b.copy();out[erase]=0;plane=Image.fromarray(out);plane.alpha_composite(head,(130,96));a=np.array(plane)
  foreground=(b[:,:,3]>0)&((yy>=135)|((xx>=160)&(yy>=128)));a[foreground]=b[foreground];a[135:]=b[135:];plane=Image.fromarray(a)
  records.append({'frame':i,'position':[130,96],'crownAxis':[154,104],'componentNativeScale':1,'eraseBox':[130,102,179,135],'protectedBodyFromY':135,'foreground':'original opaque forward arm at x>=160,y>=128','bareSha256':hashlib.sha256((BARE/file).read_bytes()).hexdigest()})
  outpath=HERE/file;outpath.parent.mkdir(parents=True,exist_ok=True);plane.save(outpath);hashes[file]=hashlib.sha256(outpath.read_bytes()).hexdigest();images.append(plane)
 p.update(name='Bill east helmet underwater salvage candidate',equipment='diving-helmet')
 p['states'][0]['provenance']='exact selected swimming helmet at native pixel scale over independently authored distress body; exact first equipped working pose repeated at wrap'
 reg={'component':'sources/canonical-head.png','donor':'bill-swim-helmet-east-coherent-v1/sources/canonical-head.png','componentSha256':hashlib.sha256(target.read_bytes()).hexdigest(),'componentNativeScale':1,'frames':records}
 for file,data in [('manifest.json',p),('helmet-registration.json',reg),('frame-hashes.json',hashes)]: (HERE/file).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(29,43,51))
 for i,im in enumerate(images):
  board.paste(im,(i*256,0),im);bare=Image.open(BARE/p['states'][0]['frameFiles'][i]);board.paste(bare,(i*256,256),bare)
 board.save(HERE/'contact-sheet.png');print('Built east helmet salvage;native selected head and authored cutter poses')
if __name__=='__main__':main()
