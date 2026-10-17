"""Canonical shared component over protected pitch bodies and exact equipped joins."""
from pathlib import Path
import json,hashlib,copy
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;BARE=HERE.parent/'bill-swim-transitions-west-coherent-v1'
DONOR=HERE.parent/'bill-cargo-helmet-west-v1/sources/canonical-head.png'
POLYGON=[(72,20),(114,20),(114,51),(110,55),(101,58),(90,55),(82,51),(75,48),(72,43)]
OFFSETS=[(104,85),(101,88),(97,91),(93,93),(89,96),(87,95)]
HEADS=[(120,92),(116,95),(112,98),(108,100),(104,103),(102,104)]
ENDPOINTS=['bill-tread-helmet-west-coherent-v1/frames/tread-west/000.png','bill-swim-helmet-west-coherent-v1/frames/swim-west/000.png']
def main():
 component=Image.open(DONOR).convert('RGBA')
 frames=[];records=[]
 for i in range(6):
  if i in [0,5]:
   original=Image.open(HERE.parent/ENDPOINTS[0 if i==0 else 1]).convert('RGBA');result=Image.new('RGBA',(256,256));result.alpha_composite(original,(36,58) if i==0 else (42,40));frames.append(result);continue
  file=f'frames/swim-start-west/{i:03}.png';original=Image.open(BARE/file).convert('RGBA');b=np.array(original);x,y=HEADS[i];ox,oy=OFFSETS[i];chin=29+oy
  erasepoly=[(x-13,y-3),(x+16,y-3),(x+16,y+23),(x-2,y+26),(x-14,y+17)];erase=Image.new('L',(256,256));ImageDraw.Draw(erase).polygon(erasepoly,fill=255);out=b.copy();out[np.array(erase)>0]=0;result=Image.fromarray(out);result.alpha_composite(component,(ox,oy));out=np.array(result)
  yy,xx=np.indices((256,256));fg=(yy>=chin+3)&(xx<=x-6)&(b[:,:,3]>0);out[fg]=b[fg];frames.append(Image.fromarray(out));records.append({'pose':i,'file':file,'offset':[ox,oy],'scale':1,'rotationDegrees':0,'erasePolygon':erasepoly,'foregroundMaxXMinY':[x-6,chin+3],'protectedBodyFromY':oy+40,'donorSha256':hashlib.sha256(DONOR.read_bytes()).hexdigest()})
 manifest=copy.deepcopy(json.loads((BARE/'manifest.json').read_text()));manifest.update(name='Bill canonical helmet exact-endpoint west swim transitions',equipment='diving-helmet');hashes={}
 for state in manifest['states']:
  ims=frames if state['id']=='swim-start-west' else list(reversed(frames))
  for file,im in zip(state['frameFiles'],ims):
   path=HERE/file;path.parent.mkdir(parents=True,exist_ok=True);im.save(path);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest()
  state['provenance']='exact equipped tread/swim endpoint components; four protected authored pitch bodies; native canonical helmet component; stop reverse derived'
 for name,obj in [('manifest.json',manifest),('frame-hashes.json',hashes),('helmet-registration.json',{'donor':DONOR.relative_to(HERE.parent).as_posix(),'componentMethod':'exact installed west canonical crop/mask','endpointAuthorities':ENDPOINTS,'endpointOffsets':[[36,58],[42,40]],'frames':records})]:(HERE/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 (HERE/'sources').mkdir(exist_ok=True);component.save(HERE/'sources/canonical-head.png')
 contact=Image.new('RGB',(1536,256),(29,43,51));d=ImageDraw.Draw(contact)
 for i,im in enumerate(frames):contact.paste(im,(256*i,0),im);d.text((256*i+5,5),str(i),fill='white')
 contact.save(HERE/'contact-sheet.png');print('Built six canonical helmet start poses and reverse stop; exact equipped endpoints')
if __name__=='__main__':main()
