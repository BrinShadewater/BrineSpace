from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parents[1];BARE=P.parent/'bill-death-ground-south-coherent-v1';DONOR=P.parent/'bill-seated-helmet-south-coherent-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cfg={'generation': 'exec-cad07484-a967-44cd-a49a-4533e1a6d26e', 'helmetRuler': [0.3, 0.31], 'sourceBoxes': [[210, 56, 334, 194], [708, 94, 828, 229], [1196, 140, 1309, 246], [210, 587, 334, 699], [710, 598, 827, 694], [1202, 599, 1320, 695]], 'sourceNecks': [[766, 227], [1255, 241], [266, 699], [768, 693], [1261, 697]]}
def main():
 m=json.loads((BARE/'manifest.json').read_text());r=json.loads((BARE/'registration.json').read_text());s=m['states'][0];source=P/'sources/equipment-v1.png';raw=Image.open(source).convert('RGBA');reference=DONOR/'sources/canonical-head.png';ref=np.array(Image.open(reference).convert('RGBA'));rgb=ref[:,:,:3].astype(float)
 first=np.array(raw.crop(cfg['sourceBoxes'][0]));fr=first[:,:,:3].astype(float);q=[0,.05,.15,.35,.5,.7,.85,.95,1];valid=(first[:,:,3]>180)&(np.ptp(fr,axis=2)<35);authority=(ref[:,:,3]>180)&(np.ptp(rgb,axis=2)<35)
 curve=np.quantile(fr.mean(2)[valid],q);target=np.quantile(rgb.mean(2)[authority],q);curve,unique=np.unique(curve,return_index=True);target=target[unique]
 ref_skin=(ref[:,:,3]>180)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2])&(rgb.mean(2)>65);first_skin=(first[:,:,3]>180)&(fr[:,:,0]>1.12*fr[:,:,1])&(fr[:,:,1]>1.14*fr[:,:,2])&(fr.mean(2)>65);skin_gain=np.median(rgb[ref_skin],axis=0)/np.median(fr[first_skin],axis=0)
 idle=DONOR/'frames/sit-down-south/000.png';frames=[Image.open(idle).convert('RGBA')];records=[];yy,xx=np.indices((256,256))
 for i,row in enumerate(r['frames'],1):
  head=np.array(raw.crop(cfg['sourceBoxes'][i]));hr=head[:,:,:3].astype(float);neutral=(head[:,:,3]>0)&(np.ptp(hr,axis=2)<35);mapped=np.interp(hr.mean(2)[neutral],curve,target);head[neutral,:3]=np.clip(hr[neutral]*mapped[:,None]/np.maximum(hr.mean(2)[neutral,None],1),0,255).astype('uint8');skin=(head[:,:,3]>0)&(hr[:,:,0]>1.12*hr[:,:,1])&(hr[:,:,1]>1.14*hr[:,:,2])&(hr.mean(2)>65);head[skin,:3]=np.clip(hr[skin]*skin_gain,0,255).astype('uint8');im=Image.fromarray(head)
  hsx,hsy=cfg['helmetRuler'];im=im.resize((round(im.width*hsx),round(im.height*hsy)),Image.Resampling.LANCZOS)
  sx,sy=r['fixedRuler'];bx,by=row['box'][:2];px,py=row['position'];nx,ny=cfg['sourceNecks'][i-1];neck=[px+(nx-bx)*sx,py+(ny-by)*sy];position=[round(neck[0]-im.width/2),round(neck[1]-im.height)]
  b=np.array(Image.open(BARE/s['frameFiles'][i]).convert('RGBA'));br=b[:,:,:3].astype(float);hx,hy=r['heads'][row['pose']];center=[px+(hx-bx)*sx,py+(hy-by)*sy];local=((xx-center[0])/13)**2+((yy-center[1])/13)**2<1;warm=(br[:,:,0]>1.12*br[:,:,1])&(br[:,:,1]>1.14*br[:,:,2]);erase=local&warm;out=b.copy();out[erase]=0;plane=Image.fromarray(out);plane.alpha_composite(im,position);frames.append(plane)
  records.append({'frame':i,'sourceBox':cfg['sourceBoxes'][i],'sourceNeck':[nx,ny],'neck':neck,'position':position,'componentSize':list(im.size),'fixedHelmetRuler':cfg['helmetRuler'],'eraseEllipse':{'center':center,'radii':[13,13]},'bareSha256':sha(BARE/s['frameFiles'][i]),'scope':'authored axial front-shell projection, original body outside declared head/equipment region'})
 hashes={}
 for file,im in zip(s['frameFiles'],frames):
  f=P/file;f.parent.mkdir(parents=True,exist_ok=True);im.save(f);hashes[file]=sha(f)
 m.update(name='Bill south dry collapse with authored front helmet perspective candidate',equipment='diving-helmet',status='staged_candidate');s['provenance']='exact equipped idle; generated pose-specific front shell over unchanged bare fall bodies, fixed helmet ruler and master matte grade'
 reg={**cfg,'source':'sources/equipment-v1.png','sourceSha256':sha(source),'authority':reference.relative_to(ROOT).as_posix(),'authoritySha256':sha(reference),'endpoint':idle.relative_to(ROOT).as_posix(),'endpointSha256':sha(idle),'bareRegistrationSha256':sha(BARE/'registration.json'),'skinGain':skin_gain.tolist(),'curveInput':curve.tolist(),'curveOutput':target.tolist(),'frames':records,'scope':'staged axial equipment design/perspective candidate; final art/physical clearance/runtime mortality pending'}
 for name,data in [('manifest.json',m),('helmet-registration.json',reg),('frame-hashes.json',hashes)]: (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,768),(34,52,62))
 for i,im in enumerate(frames):
  board.paste(im,(i*256,0),im);bare=Image.open(BARE/s['frameFiles'][i]);board.paste(bare,(i*256,256),bare);board.paste(frames[0],(i*256,512),frames[0])
 board.save(P/'contact-sheet.png');print('Built south helmet collapse; authored perspective, fixed equipment ruler, paired bodies')
if __name__=='__main__':main()
