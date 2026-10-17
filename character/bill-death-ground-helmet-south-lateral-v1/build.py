from pathlib import Path
import json,hashlib,math,copy
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parents[1];BARE=P.parent/'bill-death-ground-south-lateral-v1';DONOR=P.parent/'bill-seated-helmet-south-coherent-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cfg={'sourceNecks': [[765, 250], [1310, 280], [357, 768], [909, 839], [1421, 839]], 'tilts': [0, 18, 35, 90, 90], 'nativeNeckAnchor': [18, 33]}
def main():
 m=json.loads((BARE/'manifest.json').read_text());r=json.loads((BARE/'registration.json').read_text());state=m['states'][0]
 source=DONOR/'sources/canonical-head.png';target=P/'sources/canonical-head.png';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes());head=Image.open(target).convert('RGBA')
 idle=DONOR/'frames/sit-down-south/000.png';frames=[Image.open(idle).convert('RGBA')];records=[];yy,xx=np.indices((256,256))
 for i,row in enumerate(r['frames'],1):
  b=np.array(Image.open(BARE/state['frameFiles'][i]).convert('RGBA'));rgb=b[:,:,:3].astype(float);sx,sy=r['fixedRuler'];bx,by=row['box'][:2];px,py=row['position'];nx,ny=cfg['sourceNecks'][i-1];neck=[px+(nx-bx)*sx,py+(ny-by)*sy];angle=cfg['tilts'][i-1]
  selected_head=Image.open(P/"sources/canonical-closed-eyes.png").convert("RGBA") if i>=4 else head
  rotated=selected_head.rotate(-angle,resample=Image.Resampling.BICUBIC,expand=True);rad=math.radians(angle);ax,ay=cfg['nativeNeckAnchor'];dx=ax-head.width/2;dy=ay-head.height/2
  anchor=[rotated.width/2+math.cos(rad)*dx-math.sin(rad)*dy,rotated.height/2+math.sin(rad)*dx+math.cos(rad)*dy];position=[round(neck[0]-anchor[0]),round(neck[1]-anchor[1])]
  hx,hy=r['heads'][row['pose']];center=[px+(hx-bx)*sx,py+(hy-by)*sy]
  local=((xx-center[0])/17)**2+((yy-center[1])/19)**2<1
  warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2]);erase=local&warm
  out=b.copy();out[erase]=0;im=Image.fromarray(out);im.alpha_composite(rotated,position);frames.append(im)
  records.append({'frame':i,'sourceNeck':[nx,ny],'neck':neck,'tiltDegrees':angle,'position':position,'componentSize':list(rotated.size),'nativeScale':1,'eraseEllipse':{'center':center,'radii':[17,19]},'bareSha256':sha(BARE/state['frameFiles'][i]),'scope':'native dry canonical helmet, head-local warm removal; unchanged body outside equipment region'})
 hashes={}
 for i,(file,im) in enumerate(zip(state['frameFiles'],frames)):
  f=P/file;f.parent.mkdir(parents=True,exist_ok=True);im.save(f);hashes[file]=sha(f)
 m.update(name='Bill south lateral collapse with canonical front helmet candidate',equipment='diving-helmet',status='staged_candidate');state['provenance']='exact equipped standing entry; native selected dry helmet follows authored neck/tilt over bare collapse bodies'
 reg={**cfg,'component':'sources/canonical-head.png','componentSha256':sha(target),'donor':source.relative_to(ROOT).as_posix(),'donorSha256':sha(source),'endpoint':idle.relative_to(ROOT).as_posix(),'endpointSha256':sha(idle),'bareRegistrationSha256':sha(BARE/'registration.json'),'frames':records,'closedEyeComponent':'sources/canonical-closed-eyes.png','closedEyeComponentSha256':sha(P/'sources/canonical-closed-eyes.png'),'scope':'candidate helmet/collar visual registration; no normal mortality/restore proof; selected face unchanged'}
 for name,data in [('manifest.json',m),('helmet-registration.json',reg),('frame-hashes.json',hashes)]: (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,768),(34,52,62))
 for i,im in enumerate(frames):
  board.paste(im,(i*256,0),im);bare=Image.open(BARE/state['frameFiles'][i]);board.paste(bare,(i*256,256),bare);board.paste(frames[0],(i*256,512),frames[0])
 board.save(P/'contact-sheet.png');print('Built south helmet collapse; native equipment scale, paired authored bodies')
if __name__=='__main__':main()
