"""Fit the exact selected east helmet component; preserve authored treading body."""
from pathlib import Path
import hashlib,json,copy
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;BARE=HERE.parent/'bill-tread-east-coherent-v1'
DONOR=HERE.parent/'bill-equipped-east-selected-v1/frames/interact-east/000.png'
POLYGON=[(72,20),(114,20),(114,51),(110,55),(101,58),(90,55),(82,51),(75,48),(72,43)]
OFFSET=(7,7)
def main():
 source=Image.open(DONOR).convert('RGBA');mask=Image.new('L',source.size);ImageDraw.Draw(mask).polygon(POLYGON,fill=255)
 a=np.array(source);a[:,:,3]=np.minimum(a[:,:,3],np.array(mask));a[a[:,:,3]==0]=0;component=Image.fromarray(a)
 (HERE/'sources').mkdir(parents=True,exist_ok=True);component.crop((72,20,115,59)).save(HERE/'sources/canonical-head.png')
 manifest=copy.deepcopy(json.loads((BARE/'manifest.json').read_text()));manifest.update(name='Bill east tread with canonical shared helmet',equipment='diving-helmet',status='owner_visual_review_pending',integration='selected_by_grid_canvas_2026_09_30')
 registrations=[];hashes={};images=[]
 for i,file in enumerate(manifest['states'][0]['frameFiles']):
  original=Image.open(BARE/file).convert('RGBA');base=np.array(original);erase=Image.new('L',original.size)
  ImageDraw.Draw(erase).polygon([(87,31),(114,31),(114,60),(96,63),(86,55)],fill=255);region=np.array(erase)>0;base[region]=0
  result=Image.fromarray(base);result.alpha_composite(component,OFFSET);ra=np.array(result)
  # Authored forward sleeve/hand crosses the bottom-front rim at extension.
  # Retain those original foreground pixels, never a rectangular face patch.
  yy,xx=np.indices((184,184));foreground=(yy>=66)&(xx>=112)&(np.array(original)[:,:,3]>0)
  ra[foreground]=np.array(original)[foreground];result=Image.fromarray(ra)
  path=HERE/file;path.parent.mkdir(parents=True,exist_ok=True);result.save(path);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest();images.append(result)
  changed=np.any(ra!=np.array(original),axis=2);y,x=np.where(changed)
  registrations.append({'frame':i,'file':file,'offset':OFFSET,'donor':DONOR.relative_to(HERE.parent).as_posix(),'donorSha256':hashlib.sha256(DONOR.read_bytes()).hexdigest(),'changedBounds':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],'protectedBodyFromY':66,'foreground':'original authored nontransparent pixels x>=112,y>=66','scale':1,'rotationDegrees':0})
 manifest['states'][0]['provenance']='exact selected east helmet/face/neck component;original treading body and forward sleeve preserved; fixed offset and native component scale'
 for name,obj in [('manifest.json',manifest),('frame-hashes.json',hashes),('helmet-registration.json',{'polygon':POLYGON,'offset':OFFSET,'landmark':'selected face centre x103/chin y49 to authored treader face centre x110/chin y56; crown and collar extend with exact native helmet component','frames':registrations})]:(HERE/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 contact=Image.new('RGB',(1104,368),(29,43,51));d=ImageDraw.Draw(contact)
 for i,im in enumerate(images):contact.paste(im,(184*i,0),im);bare=Image.open(BARE/manifest['states'][0]['frameFiles'][i]).convert('RGBA');contact.paste(bare,(184*i,184),bare);d.text((184*i+4,4),str(i),fill='white')
 contact.save(HERE/'contact-sheet.png');print('Built six canonical-equipped east tread poses; no body re-rendering')
if __name__=='__main__':main()
