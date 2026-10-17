from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
from palette import match_master
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def idle(folder):
 m=json.loads((folder/'manifest.json').read_text());s=next(s for s in m['states'] if s['id']=='idle-north');return Image.open(folder/s['frameFiles'][0]).convert('RGBA')
def face(im):
 a=np.array(im);yy,xx=np.indices(a.shape[:2]);y,x=np.where(a[:,:,3]>180);top=y.min();height=y.max()-top+1;mask=(a[:,:,3]>180)&(yy<top+height*7/148);y,x=np.where(mask);return np.array([x.mean(),float(top+height*10/148)])
def main():
 raw=Image.open(HERE/'source.png').convert('RGBA');cells=[]
 for i in range(6):
  cell=raw.crop((round(i*raw.width/6),0,round((i+1)*raw.width/6),raw.height));a=np.array(cell);labs,n=label(a[:,:,3]>180);count=np.bincount(labs.ravel());count[0]=0;mask=labs==count.argmax();a[~binary_dilation(mask,iterations=2)]=0;cells.append(Image.fromarray(a))
 canonical=idle(ROOT/'character/crew-runtime-matte-v1/branforth');target=face(canonical)+[36,52];a=np.array(cells[0]);y,x=np.where(a[:,:,3]>180);scale=148/(y.max()-y.min()+1);floor=int(y.max());rows=[];tracking=[]
 shell=Image.open(ROOT/'character/james-shared-helmet-actions-north-v1/selected-shell.png').convert('RGBA');helmet_offset=face(canonical)-[76,22]
 for i,cell in enumerate(cells):
  h=face(cell);at=(round(target[0]-h[0]*scale),round(224-floor*scale));body=Image.new('RGBA',(256,256));body.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),at)
  a=np.array(body);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>180)[0].min();warm=(r>b+12)&(r>g+5);yellow=(r>b+18)&(g>b+10);mask=(a[:,:,3]>0)&~warm&~yellow&(yy>top+30);lum=rgb.mean(2);mapped=np.interp(lum,[0,18,34,52,72.5,93,115,160,220,255],[0,18,31,47,63,85,101,136,182,211]);gain=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0);a[mask,:3]=np.rint(rgb[mask]*gain[mask,None]).clip(0,255).astype('uint8');body=Image.fromarray(a)
  body=match_master(body)
  f=face(body);helmet_at=np.rint(f-helmet_offset).astype(int);out=body.copy();d=ImageDraw.Draw(out);d.polygon([tuple(f+v) for v in [(-12,-11),(12,-11),(14,8),(8,12),(-8,12),(-14,8)]],fill=(0,0,0,0));out.alpha_composite(shell,tuple(helmet_at));rows.append((body,out));tracking.append({'sourcePose':i,'position':at,'face':f.tolist(),'helmetPosition':helmet_at.tolist()})
 hashes={};packs=[]
 for mode,idx in [('bare',0),('helmet',1)]:
  paths=[]
  for i,row in enumerate(rows):
   f=HERE/'frames'/mode/f'{i:03}.png';f.parent.mkdir(exist_ok=True,parents=True);row[idx].save(f);rel=f.relative_to(HERE).as_posix();paths.append(rel);hashes[rel]=hashlib.sha256(f.read_bytes()).hexdigest()
  m=dict(name='James north cargo carry '+mode,frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_north_carry_v1',strideDistanceCells={'carry-north':.0827027027027027},states=[dict(id='carry-north',frameCount=6,frameFiles=paths,frameDurationsMs=[140]*6,loop=True,facings=['north']*6,waterKinds=['carry']*6,waterPoses=[False]*6,depthOffsets=[0]*6,provenance={'source':'source.png','walkingGuideSourceFrames':[0,6,12,18,24,30],'direction':'Independent north view','palette':'Fixed master-matched hardware highlight compression and gold calibration; head protected'})]);(HERE/(mode+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n');packs.append(m)
 previews=[]
 for i,row in enumerate(rows):
  board=Image.new('RGB',(1000,330),'#303b40');d=ImageDraw.Draw(board);d.text((8,8),'James north carrying - bare / shared helmet / 82px / 54px / 27px',fill='white')
  for mode,im,base in [('bare',row[0],0),('helmet',row[1],230)]:
   board.paste(im,(base,70),im)
   for h,x in [(82,510),(54,725),(27,870)]:
    sc=h/148;small=im.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);dx=x+(0 if mode=='bare' else round(256*sc)+8);board.paste(small,(dx,294-round(224*sc)),small)
  previews.append(board)
 previews[0].save(HERE/'review.gif',save_all=True,append_images=previews[1:],duration=[140]*6,loop=0)
 sheet=Image.new('RGB',(1536,640),'#303b40');d=ImageDraw.Draw(sheet)
 for j,row in enumerate(rows):
  for i,im in enumerate(row):sheet.paste(im,(j*256,i*320+60),im);d.text((j*256+5,i*320+8),('bare' if i==0 else 'helmet')+' '+str(j),fill='white')
 sheet.save(HERE/'contact.png');(HERE/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');(HERE/'registration.json').write_text(json.dumps({'sourceSha256':hashlib.sha256((HERE/'source.png').read_bytes()).hexdigest(),'fixedScale':scale,'fixedFloor':floor,'tracking':tracking,'guide':'walking-pose-guide.png'},indent=2)+'\n');(HERE/'index.html').write_text('<style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>James north carrying</h1><p>Independent north carry, accepted walk pose guide, fixed matte grade. Staged for owner review.</p><img src="review.gif"><img src="contact.png">');print('North carrying12 references;6 poses per mode,840ms; fixed scale',scale)
if __name__=='__main__':
 main()
 if (HERE/'source-pickup-v1.png').exists():
  from build_pickup import main as build_pickup
  build_pickup()
