"""Fit the exact selected south swimming helmet at its native pixel scale."""
from pathlib import Path
import copy,hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-death-water-south-coherent-v1'
DONOR=HERE.parent/'bill-swim-helmet-south-coherent-v1'
def main():
 p=json.loads((BARE/'manifest.json').read_text(encoding='utf-8'))
 source=DONOR/'sources/canonical-head.png';target=HERE/'sources/canonical-head.png';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())
 head=Image.open(target).convert('RGBA');yy,xx=np.indices((256,256));images=[];records=[];hashes={}
 for i,file in enumerate(p['states'][0]['frameFiles']):
  b=np.array(Image.open(BARE/file).convert('RGBA'))
  if i==0:
   plane=Image.new('RGBA',(256,256));plane.alpha_composite(Image.open(DONOR/'frames/swim-south/000.png').convert('RGBA'),(24,-24))
  else:
   erase=(xx>=116)&(xx<=140)&(yy>=108)&(yy<142)
   out=b.copy();out[erase]=0;plane=Image.fromarray(out);plane.alpha_composite(head,(128-head.width//2,106));a=np.array(plane)
   foreground=(b[:,:,3]>0)&((xx<116)|(xx>140))&(yy<142);a[foreground]=b[foreground];a[146:]=b[146:];plane=Image.fromarray(a)
   records.append({'frame':i,'position':[128-head.width//2,106],'crownAxis':[128,110],'componentNativeScale':1,'eraseBox':[116,108,141,142],'protectedBodyFromY':146,'foreground':'original opaque forearms outside x116..140 above y142','bareSha256':hashlib.sha256((BARE/file).read_bytes()).hexdigest()})
  outpath=HERE/file;outpath.parent.mkdir(parents=True,exist_ok=True);plane.save(outpath);hashes[file]=hashlib.sha256(outpath.read_bytes()).hexdigest();images.append(plane)
 p.update(name='Bill south helmet underwater death candidate',equipment='diving-helmet')
 p['states'][0]['provenance']='exact selected swimming helmet at native pixel scale over independently authored death body;exact equipped swim entry;finite terminal hold'
 reg={'component':'sources/canonical-head.png','donor':'bill-swim-helmet-south-coherent-v1/sources/canonical-head.png','componentSha256':hashlib.sha256(target.read_bytes()).hexdigest(),'componentNativeScale':1,'endpointAuthority':'bill-swim-helmet-south-coherent-v1/frames/swim-south/000.png','endpointPadding':[24,-24],'frames':records}
 for file,data in [('manifest.json',p),('helmet-registration.json',reg),('frame-hashes.json',hashes)]: (HERE/file).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(29,43,51))
 for i,im in enumerate(images):
  board.paste(im,(i*256,0),im);bare=Image.open(BARE/p['states'][0]['frameFiles'][i]);board.paste(bare,(i*256,256),bare)
 board.save(HERE/'contact-sheet.png');print('Built south helmet death;native selected head,exact swim entry')
if __name__=='__main__':main()
