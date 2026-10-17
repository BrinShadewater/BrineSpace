from pathlib import Path
import json,hashlib,math
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def idle(folder):
 m=json.loads((folder/'manifest.json').read_text());s=next(s for s in m['states'] if s['id']=='idle-east');return Image.open(folder/s['frameFiles'][0]).convert('RGBA')
def face(im):
 a=np.array(im);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>180)[0].min()
 mask=(r>g+10)&(r>b+12)&(g>b+2)&(a[:,:,3]>150)&(yy<top+28)&(r+g+b>180)
 labs,n=label(mask);count=np.bincount(labs.ravel());count[0]=0;y,x=np.where(labs==count.argmax());assert len(x)>25
 return np.array([x.mean(),y.mean()])
def main():
 raw=Image.open(HERE/'source.png').convert('RGBA');cells=[]
 for i in range(12):
  cell=raw.crop((i%6*362,i//6*362,(i%6+1)*362,(i//6+1)*362));a=np.array(cell);labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());keep=np.isin(labs,np.where(counts>300)[0]);keep[labs==0]=False;a[~binary_dilation(keep,iterations=2)]=0;cells.append(Image.fromarray(a))
 canonical=idle(ROOT/'character/crew-runtime-matte-v1/branforth');fitted=idle(ROOT/'character/james-shared-helmet-runtime-v1');ref=np.array(canonical);cy,cx=np.where(ref[:,:,3]>180)
 a=np.array(cells[0]);sy,sx=np.where(a[:,:,3]>180);scale_y=(cy.max()-cy.min()+1)/(sy.max()-sy.min()+1)
 ratios=[]
 for off in range(100,127,2):
  ir=int(cy.min()+off);sr=round(sy.min()+off/scale_y);ix=np.where(ref[ir,:,3]>180)[0];xx=np.where((a[sr,:,3]>180)&(np.arange(362)<225))[0]
  ratios.append((ix.max()-ix.min()+1)/(xx.max()-xx.min()+1))
 scale_x=float(np.median(ratios));frames=[];records=[]
 for i,cell in enumerate(cells):
  a=np.array(cell);y,x=np.where(a[:,:,3]>180)
  if i<6:
   bottom=(a[:,:,3]>180)&(np.indices(a.shape[:2])[0]>350);by,bx=np.where(bottom);anchor=float(bx.min()+35);pos=(round(138-anchor*scale_x),round(224-357*scale_y))
  else:
   head=face(cell);target=face(frames[5]);pos=(round(target[0]-head[0]*scale_x),round(224-348*scale_y))
  out=Image.new('RGBA',(256,256));out.alpha_composite(cell.resize((round(362*scale_x),round(362*scale_y)),Image.Resampling.LANCZOS),pos)
  frames.append(out);records.append({'sourcePose':i,'position':pos})
 # Fixed neutral material correction; preserve warm skin, hair and yellow patches.
 for i,im in enumerate(frames):
  a=np.array(im);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);rgb=a[:,:,:3].astype(float);warm=(r>b+12)&(r>g+5);yellow=(r>b+18)&(g>b+10);neutral=~warm&~yellow&(a[:,:,3]>0);lum=rgb@np.array([.2126,.7152,.0722]);rgb[neutral]=np.repeat(lum[neutral,None],3,axis=1);a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');frames[i]=Image.fromarray(a)
 # Ground case is fixed across standing endpoint and the initial reach.
 case=frames[0].crop((155,190,230,225));ground=Image.new('RGBA',(256,256));ground.alpha_composite(canonical,(36,52));ground.alpha_composite(case,(155,190));frames[0]=ground
 shell=Image.open(ROOT/'character/james-shared-helmet-east-v1/helmet.png').convert('RGBA');reference=face(canonical);offset=reference-np.array([73,16]);worn=[];tracking=[]
 for i,im in enumerate(frames):
  target=face(im);angle=-10.0 if i in [1,2] else 0.0;rot=shell.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True);center=np.array(shell.size)/2;pt=offset-center;c=math.cos(math.radians(angle));si=math.sin(math.radians(angle));point=np.array([c*pt[0]+si*pt[1],-si*pt[0]+c*pt[1]])+np.array(rot.size)/2;at=np.rint(target-point).astype(int)
  out=im.copy();d=ImageDraw.Draw(out);d.polygon([tuple(target+v) for v in [(-13,-18),(10,-18),(15,7),(7,14),(-13,9)]],fill=(0,0,0,0));out.alpha_composite(rot,tuple(at));worn.append(out);tracking.append({'sourcePose':i,'face':target.tolist(),'helmetPosition':at.tolist(),'angle':angle})
 out=Image.new('RGBA',(256,256));out.alpha_composite(fitted,(36,52));out.alpha_composite(case,(155,190));worn[0]=out
 clips={'pickup-east':list(range(6)),'carry-east':list(range(6,12)),'unload-east':list(reversed(range(6)))};packs=[];hashes={}
 legacy={}
 catalog=json.loads((ROOT/'character/chief-engineer-branforth-v2/catalog.json').read_text())
 for f in catalog['body']:
  m=json.loads((ROOT/'character/chief-engineer-branforth-v2'/f).read_text());legacy.update({s['id']:s for s in m['states']})
 for mode,rows in [('bare',frames),('helmet',worn)]:
  m=dict(name='James east cargo '+mode,frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_james_east_cargo_v1',strideDistanceCells={'carry-east':.0872972972972973},states=[])
  for key,indices in clips.items():
   st=dict(legacy['unload-east' if key=='pickup-east' else key]);st.update(id=key,frameCount=6,frameFiles=[],frameDurationsMs=([70,80,90,100,100,80] if key=='pickup-east' else [140]*6 if key=='carry-east' else [80,100,100,90,80,70]),loop=key=='carry-east',provenance={'source':'source.png','sourcePoses':indices,'fixedScale':[scale_x,scale_y],'derivation':'Independent pickup and complete6-pose alternating carry; unload reverses pickup','helmet':'Selected shared east shell follows moving face'})
   for j,idx in enumerate(indices):
    f=HERE/'frames'/mode/key/f'{j:03}.png';f.parent.mkdir(parents=True,exist_ok=True);rows[idx].save(f);rel=f.relative_to(HERE).as_posix();st['frameFiles'].append(rel);hashes[rel]=hashlib.sha256(f.read_bytes()).hexdigest()
   m['states'].append(st)
  (HERE/(mode+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n');packs.append(m)
 previews=[];times=[]
 for key,repeats in [('pickup-east',1),('carry-east',3),('unload-east',1)]:
  for _ in range(repeats):
   for j in range(6):
    board=Image.new('RGB',(1000,330),'#303b40');d=ImageDraw.Draw(board);d.text((8,8),'James east cargo - '+key+' / bare / shared helmet / 82px / 54px / 27px',fill='white')
    for mode,m,base in [('bare',packs[0],0),('helmet',packs[1],230)]:
     st=next(s for s in m['states'] if s['id']==key);im=Image.open(HERE/st['frameFiles'][j]).convert('RGBA');board.paste(im,(base,70),im)
     for h,x in [(82,510),(54,725),(27,870)]:
      sc=h/148;small=im.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);dx=x+(0 if mode=='bare' else round(256*sc)+8);board.paste(small,(dx,294-round(224*sc)),small)
    previews.append(board);times.append(st['frameDurationsMs'][j])
 times[-1]+=500;previews[0].save(HERE/'review.gif',save_all=True,append_images=previews[1:],duration=times,loop=0)
 sheet=Image.new('RGB',(1536,1536),'#303b40');d=ImageDraw.Draw(sheet)
 for row,(mode,m,key) in enumerate([(mode,m,key) for key in clips for mode,m in [('bare',packs[0]),('helmet',packs[1])]]):
  st=next(s for s in m['states'] if s['id']==key)
  for j,f in enumerate(st['frameFiles']):
   im=Image.open(HERE/f).convert('RGBA');sheet.paste(im,(j*256,row*256),im);d.text((j*256+8,row*256+8),mode+' '+key+' '+str(j),fill='white')
 sheet.save(HERE/'contact.png');(HERE/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');(HERE/'registration.json').write_text(json.dumps({'sourceSha256':hashlib.sha256((HERE/'source.png').read_bytes()).hexdigest(),'fixedScale':[scale_x,scale_y],'records':records,'tracking':tracking,'limits':['Cargo phase joins visually continuous but not identical pixels; source gait enters stride from pickup neutral.','First/last actor body exact installed idle; floor case retained.','Staged, owner review pending.']},indent=2)+'\n');print('Cargo36 references,6 pickup/6 alternating carry/6 reversed unload per mode; fixed scale',scale_x,scale_y)
if __name__=='__main__':main()
