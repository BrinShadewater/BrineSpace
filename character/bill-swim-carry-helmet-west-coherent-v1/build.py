"""Fit canonical west head component over protected independently authored water bodies."""
from pathlib import Path
import copy,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-swim-carry-west-coherent-v1'
DONOR=HERE.parent/'bill-cargo-helmet-west-v1/sources/canonical-head.png'
POSITION=(45,55)
ERASE=[(47,61),(74,61),(74,86),(60,90),(47,86)]
FG=(54,87)
def main():
 head=Image.open(DONOR).convert('RGBA');manifest=copy.deepcopy(json.loads((BARE/'manifest.json').read_text()));manifest.update(name='Bill west swimming cargo with canonical shared helmet',equipment='diving-helmet')
 images=[];hashes={};records=[];(HERE/'sources').mkdir(parents=True,exist_ok=True);head.save(HERE/'sources/canonical-head.png')
 for file in manifest['states'][0]['frameFiles']:
  original=Image.open(BARE/file).convert('RGBA');a=np.array(original);mask=Image.new('L',original.size);ImageDraw.Draw(mask).polygon(ERASE,fill=255);a[np.array(mask)>0]=0;result=Image.fromarray(a);result.alpha_composite(head,POSITION);out=np.array(result)
  yy,xx=np.indices(a.shape[:2]);fg=(yy>=FG[1])&(xx<=FG[0])&(np.array(original)[:,:,3]>0);out[fg]=np.array(original)[fg];result=Image.fromarray(out)
  path=HERE/file;path.parent.mkdir(parents=True,exist_ok=True);result.save(path);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest();images.append(result);records.append({'file':file,'position':POSITION,'scale':1,'rotationDegrees':0,'protectedBodyFromY':POSITION[1]+head.height,'foregroundMaxXMinY':FG,'bareBodySha256':hashlib.sha256((BARE/file).read_bytes()).hexdigest()})
 manifest['states'][0]['provenance']='independent authored west water cargo body; exact selected canonical west head/helmet component; foreground sleeve retained'
 for name,obj in [('manifest.json',manifest),('frame-hashes.json',hashes),('helmet-registration.json',{'donor':DONOR.relative_to(HERE.parent).as_posix(),'donorSha256':hashlib.sha256(DONOR.read_bytes()).hexdigest(),'position':POSITION,'erasePolygon':ERASE,'frames':records})]:(HERE/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 w=manifest['frameWidth'];h=manifest['frameHeight'];contact=Image.new('RGB',(w*6,h*2),(29,43,51));d=ImageDraw.Draw(contact)
 for i,im in enumerate(images):contact.paste(im,(w*i,0),im);bare=Image.open(BARE/manifest['states'][0]['frameFiles'][i]).convert('RGBA');contact.paste(bare,(w*i,h),bare);d.text((w*i+5,5),str(i),fill='white')
 contact.save(HERE/'contact-sheet.png');print('Built six canonical west swimming cargo poses')
if __name__=='__main__':main()

