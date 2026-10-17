"""Package independent pickup source; preserve accepted carry pixels exactly."""
from pathlib import Path
import json, hashlib, math
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation
from build import face, idle
from palette import match_master
from unload_timing import add_midrise
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def main():
 raw=Image.open(HERE/'source-pickup-v1.png').convert('RGBA'); cells=[]
 for i in range(6):
  cell=raw.crop((i*362,0,(i+1)*362,724));a=np.array(cell);labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
  mask=np.isin(labs,np.where(counts>200)[0]);a[~binary_dilation(mask,iterations=2)]=0;cells.append(Image.fromarray(a))
 canonical=idle(ROOT/'character/crew-runtime-matte-v1/branforth');fitted=idle(ROOT/'character/james-shared-helmet-runtime-v1')
 a=np.array(cells[0]);y,x=np.where(a[:,:,3]>180);scale=148/(y.max()-y.min()+1);floor=int(y.max());target=face(canonical)+[36,52]
 initial_x=round(target[0]-face(cells[0])[0]*scale);yy,xx=np.indices(a.shape[:2]);rear=float(xx[(a[:,:,3]>180)&(yy>floor-12)].max())
 rows=[];registration=[]
 for i,cell in enumerate(cells):
  a=np.array(cell);yy,xx=np.indices(a.shape[:2]);contact=float(xx[(a[:,:,3]>180)&(yy>floor-12)].max());at=(round(target[0]-face(cell)[0]*scale),round(224-floor*scale))
  body=Image.new('RGBA',(256,256));body.alpha_composite(cell.resize((round(362*scale),round(724*scale)),Image.Resampling.LANCZOS),at)
  a=np.array(body);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>180)[0].min();warm=(r>b+12)&(r>g+5);yellow=(r>b+18)&(g>b+10);mask=(a[:,:,3]>0)&~warm&~yellow&(yy>top+30)
  lum=rgb.mean(2);mapped=np.interp(lum,[0,18,34,52,72.5,93,115,160,220,255],[0,18,31,47,63,85,101,136,182,211]);gain=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0);a[mask,:3]=np.rint(rgb[mask]*gain[mask,None]).clip(0,255).astype('uint8');rows.append(match_master(Image.fromarray(a)));registration.append({'sourcePose':i,'position':at,'rearContact':contact})
 # Exact installed idle endpoint: forward floor case fragment is behind legs in this rear view.
 case=rows[0].crop((121,198,138,220));ground=Image.new('RGBA',(256,256));ground.alpha_composite(case,(121,198));ground.alpha_composite(canonical,(36,52));rows[0]=ground
 shell=Image.open(ROOT/'character/james-shared-helmet-actions-north-v1/selected-shell.png').convert('RGBA');offset=face(canonical)-[76,22];worn=[]
 for i,im in enumerate(rows):
  f=face(im);f[1]=float(np.where(np.array(im)[:,:,3]>180)[0].min()+10);angle=0;rot=shell.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True);center=np.array(shell.size)/2;pt=offset-center;c=math.cos(math.radians(angle));s=math.sin(math.radians(angle));point=np.array([c*pt[0]+s*pt[1],-s*pt[0]+c*pt[1]])+np.array(rot.size)/2;at=np.rint(f-point).astype(int)
  out=im.copy();ImageDraw.Draw(out).polygon([tuple(f+v) for v in [(-12,-11),(12,-11),(14,8),(8,12),(-8,12),(-14,8)]],fill=(0,0,0,0));out.alpha_composite(rot,tuple(at));worn.append(out);registration[i].update(face=f.tolist(),helmetPosition=at.tolist(),helmetAngle=angle)
 out=Image.new('RGBA',(256,256));out.alpha_composite(case,(121,198));out.alpha_composite(fitted,(36,52));worn[0]=out
 hashes=json.loads((HERE/'frame-hashes.json').read_text());accepted={k:v for k,v in hashes.items() if '/pickup-' not in k and '/unload-' not in k}
 if not (HERE/'accepted-carry-hashes.json').exists():(HERE/'accepted-carry-hashes.json').write_text(json.dumps(accepted,indent=2)+'\n')
 packs=[]
 for mode,frames in [('bare',rows),('helmet',worn)]:
  path=HERE/(mode+'-manifest.json');m=json.loads(path.read_text());carry=next(s for s in m['states'] if s['id']=='carry-north');frames[5]=Image.open(HERE/carry['frameFiles'][0]).convert('RGBA');states=[]
  for key,indices,times in [('pickup-north',list(range(6)),[70,80,90,100,100,80]),('unload-north',list(reversed(range(6))),[80,100,100,90,80,70])]:
   paths=[]
   for j,index in enumerate(indices):
    f=HERE/'frames'/mode/key/f'{j:03}.png';f.parent.mkdir(parents=True,exist_ok=True);frames[index].save(f);rel=f.relative_to(HERE).as_posix();paths.append(rel);hashes[rel]=hashlib.sha256(f.read_bytes()).hexdigest()
   states.append(dict(id=key,frameCount=6,frameFiles=paths,frameDurationsMs=times,loop=False,facings=['north']*6,waterKinds=['carry']*6,waterPoses=[False]*6,depthOffsets=[0]*6,provenance={'source':'source-pickup-v1.png','sourcePoses':indices,'fixedScale':scale,'registration':'Fixed source floor; front head horizontal camera registration','derivation':'Independent pickup; exact reversed unloading; idle and carry endpoints selected pixels','matte':'Fixed north master-matte-v2 material pipeline; head protected'}))
  add_midrise(states[1])
  m['states']=[states[0],carry,states[1]];m['status']='installed_north_cargo_reused_rise_v364';path.write_text(json.dumps(m,indent=2)+'\n');packs.append(m)
 previews=[];times=[]
 for key,repeats in [('pickup-north',1),('carry-north',3),('unload-north',1)]:
  for _ in range(repeats):
   for i in range(7 if key=='unload-north' else 6):
    board=Image.new('RGB',(1000,330),'#303b40');d=ImageDraw.Draw(board);d.text((8,8),'James north cargo - '+key+' / bare / shared helmet / 82px / 54px / 27px',fill='white')
    for mode,m,base in [('bare',packs[0],0),('helmet',packs[1],230)]:
     st=next(s for s in m['states'] if s['id']==key);im=Image.open(HERE/st['frameFiles'][i]).convert('RGBA');board.paste(im,(base,70),im)
     for h,x in [(82,510),(54,725),(27,870)]:
      sc=h/148;small=im.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);dx=x+(0 if mode=='bare' else round(256*sc)+8);board.paste(small,(dx,294-round(224*sc)),small)
    previews.append(board);times.append(st['frameDurationsMs'][i])
 times[-1]+=500;previews[0].save(HERE/'review-chain-v1.gif',save_all=True,append_images=previews[1:],duration=times,loop=0)
 sheet=Image.new('RGB',(1792,1536),'#303b40');d=ImageDraw.Draw(sheet)
 for row,(m,key) in enumerate([(m,key) for key in ['pickup-north','carry-north','unload-north'] for m in packs]):
  st=next(s for s in m['states'] if s['id']==key)
  for i,f in enumerate(st['frameFiles']):
   im=Image.open(HERE/f).convert('RGBA');sheet.paste(im,(i*256,row*256),im);d.text((i*256+8,row*256+8),m['name']+' '+key+' '+str(i),fill='white')
 sheet.save(HERE/'contact-chain-v1.png');(HERE/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');(HERE/'pickup-registration.json').write_text(json.dumps({'sourceSha256':hashlib.sha256((HERE/'source-pickup-v1.png').read_bytes()).hexdigest(),'scale':scale,'floor':floor,'records':registration,'limits':['Forward case fragment composited behind exact selected idle body','Both source and selected endpoint poses retained; no synthesized inbetweens']},indent=2)+'\n')
 (HERE/'index.html').write_text('<style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>James north cargo</h1><p>Installed accepted north cargo.</p><img src="review-chain-v1.gif"><img src="contact-chain-v1.png">')
 print('North cargo38 references; accepted carry unchanged; pickup/unload520ms; reused mid-rise; scale',scale)
if __name__=='__main__':main()
