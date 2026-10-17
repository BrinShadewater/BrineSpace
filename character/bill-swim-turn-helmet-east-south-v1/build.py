"""Reuse reviewed prone-yaw helmets on independently authored basic swim bodies."""
from pathlib import Path
import copy,hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-swim-turn-east-south-v1'
DONOR=HERE.parent/'bill-swim-carry-turn-helmet-east-south-v1'
ENDPOINTS=[('bill-swim-helmet-east-coherent-v1/frames/swim-east/000.png',(6,40)),('bill-swim-helmet-south-coherent-v1/frames/swim-south/000.png',(24,-24))]
def main():
 p=json.loads((BARE/'manifest.json').read_text(encoding='utf-8'));r=json.loads((BARE/'registration.json').read_text(encoding='utf-8'));d=json.loads((DONOR/'helmet-registration.json').read_text(encoding='utf-8'));records=[];components=[];images=[];hashes={}
 (HERE/'components').mkdir(exist_ok=True)
 for c in d['components']:
  path=HERE/c['file'];path.write_bytes((DONOR/c['file']).read_bytes());components.append(copy.deepcopy(c))
 for path,pad in ENDPOINTS:
  plane=Image.new('RGBA',(256,256));plane.alpha_composite(Image.open(HERE.parent/path).convert('RGBA'),pad);images.append(plane)
 start,end=images;images=[start];yy,xx=np.indices((256,256))
 for i,registration in enumerate(r['frames'],1):
  bare=Image.open(BARE/p['states'][0]['frameFiles'][i]).convert('RGBA');b=np.array(bare);hx,hy=map(round,registration['targetCrownAxis']);head=Image.open(HERE/components[i]['file']).convert('RGBA');pos=(hx-head.width//2,hy-5)
  br=b[:,:,:3].astype(float);warm=(br[:,:,0]>1.13*br[:,:,1])&(br[:,:,1]>1.14*br[:,:,2]);erase=(abs(xx-hx)<=24)&(yy>=hy-2)&(yy<hy+31)&warm;out=b.copy();out[erase]=0;plane=Image.fromarray(out);plane.alpha_composite(head,pos);a=np.array(plane)
  protected_y=max(hy+31,pos[1]+head.height);foreground=(b[:,:,3]>0)&((yy>=protected_y)|((abs(xx-hx)>20)&(yy>=hy+20)));a[foreground]=b[foreground];a[protected_y:]=b[protected_y:];images.append(Image.fromarray(a))
  records.append({'sourcePose':i,'file':p['states'][0]['frameFiles'][i],'component':components[i]['file'],'position':pos,'crownAxis':[hx,hy],'eraseBox':[hx-24,hy-2,hx+25,hy+31],'eraseMethod':'bounded warm hair/skin support;neutral collar/quilt preserved','protectedBodyFromY':protected_y,'bareSha256':hashlib.sha256((BARE/p['states'][0]['frameFiles'][i]).read_bytes()).hexdigest()})
 images.append(end);manifest=copy.deepcopy(p);manifest.update(name='Bill east/south pitched helmet basic swim turn candidate',equipment='diving-helmet')
 for state,frames in zip(manifest['states'],[images,images[::-1]]):
  for file,im in zip(state['frameFiles'],frames):
   path=HERE/file;path.parent.mkdir(parents=True,exist_ok=True);im.save(path);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest()
  state['provenance']='reviewed cargo-independent prone-yaw shell components at exact native pixel scale;new basic swim bodies;exact equipped loop endpoints;reverse derived'
 reg={'source':'../bill-swim-carry-turn-helmet-east-south-v1/'+d['source'],'sourceGeneration':d['sourceGeneration'],'sourceSha256':d['sourceSha256'],'scale':d['scale'],'componentNativeScale':1,'donorPack':'../bill-swim-carry-turn-helmet-east-south-v1/helmet-registration.json','components':components,'endpointAuthorities':[{'path':path,'padding':pad} for path,pad in ENDPOINTS],'frames':records}
 for file,data in [('manifest.json',manifest),('helmet-registration.json',reg),('frame-hashes.json',hashes)]: (HERE/file).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(29,43,51))
 for i,im in enumerate(images):
  board.paste(im,(256*i,0),im);bare=Image.open(BARE/p['states'][0]['frameFiles'][i]);board.paste(bare,(256*i,256),bare)
 board.save(HERE/'contact-sheet.png');print('Built paired basic swim helmet turns;reviewed shell pixels reused')
if __name__=='__main__':main()
