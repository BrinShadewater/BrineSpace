"""Package independent seated sources at one directional anatomical scale."""
from pathlib import Path
import json, hashlib, os, copy
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
TIMING={'sit-down':[100,140,160,160,140,100], 'sit-idle':[250]*6, 'read-seated':[350,350,500,600,400,400]}
retained={}
catalog=ROOT/'character/chief-engineer-branforth-v2'
for manifest in json.loads((catalog/'catalog.json').read_text())['body']:
 for state in json.loads((catalog/manifest).read_text())['states']:retained[state['id']]=state

def extract(path):
 a=np.array(Image.open(path).convert('RGBA')); labs,n=label(a[:,:,3]>180)
 counts=np.bincount(labs.ravel());counts[0]=0
 ids=sorted(np.argsort(counts)[-18:], key=lambda k:np.where(labs==k)[0].mean())
 assert min(counts[k] for k in ids)>5000,'Missing full figure'
 result=[]
 for row in range(3):
  keys=sorted(ids[row*6:row*6+6],key=lambda k:np.where(labs==k)[1].mean())
  for k in keys:
   y,x=np.where(labs==k); box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4]
   x0,y0,x1,y1=box;assert x0>=0 and y0>=0 and x1<a.shape[1] and y1<a.shape[0],'Source touches edge'
   cell=a[y0:y1,x0:x1].copy();cell[~binary_dilation(labs[y0:y1,x0:x1]==k,iterations=2)]=0
   result.append((Image.fromarray(cell),box))
 return result

def foot(im):
 a=np.array(im);y,x=np.where(a[:,:,3]>180);floor=int(y.max()); yy=np.indices(a.shape[:2])[0]
 y,x=np.where((a[:,:,3]>180)&(yy>=floor-4));return float(x.mean()),floor

def gold_mask(a):
 r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);yy=np.indices(a.shape[:2])[0];top=np.where(a[:,:,3]>180)[0].min()
 return (a[:,:,3]>180)&(r-b>35)&(g-b>20)&(yy>top+30)&(yy<top+86)

def grade(im,gain):
 a=np.array(im);rgb=a[:,:,:3].astype(float);gold=gold_mask(a);top=np.where(a[:,:,3]>180)[0].min();yy=np.indices(a.shape[:2])[0]
 body=(a[:,:,3]>0)&(yy>top+30)&~gold;lum=rgb.mean(2)
 mapped=np.interp(lum,[0,50,70,90,120,160,200,255],[0,50,68,80,99,126,149,170]);mult=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0)
 rgb[body]*=mult[body,None];rgb[gold]*=gain;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');return Image.fromarray(a)

def build(d):
 p=ROOT/'character'/('james-seated-'+d+'-v1');cells=extract(p/'source.png')
 folder=ROOT/'character/crew-runtime-matte-v1/branforth';master_pack=json.loads((folder/'manifest.json').read_text());st=next(s for s in master_pack['states'] if s['id']=='idle-'+d);master=Image.open(folder/st['frameFiles'][0]).convert('RGBA')
 ma=np.array(master);y,x=np.where(ma[:,:,3]>180);height=int(y.max()-y.min()+1);a=np.array(cells[0][0]);y,x=np.where(a[:,:,3]>180);scale=height/(y.max()-y.min()+1);target=foot(master)
 raw=[];tracking=[]
 for i,(cell,box) in enumerate(cells):
  anchor=foot(cell);at=[round(target[0]-anchor[0]*scale),round(target[1]-anchor[1]*scale)]
  im=Image.new('RGBA',(184,192));im.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),at)
  raw.append(im);tracking.append(dict(sourcePose=i,sourceBox=box,translation=at))
 a=np.array(raw[0]);gain=np.median(ma[:,:,:3][gold_mask(ma)],axis=0)/np.median(a[:,:,:3][gold_mask(a)],axis=0)
 rows=[grade(im,gain) for im in raw]
 # Shared seat and standing arrivals; original independent source remains untouched.
 rows[0]=master.copy();rows[6]=rows[5].copy();rows[11]=rows[5].copy();rows[12]=rows[5].copy();rows[17]=rows[5].copy()
 for i,im in enumerate(raw):
  dest=p/'registered-ungraded'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);im.save(dest)
 state_indices={'sit-down':list(range(6)),'sit-idle':list(range(6,12)),'read-seated':list(range(12,18)),'sit-rise':list(reversed(range(6)))}
 pack=dict(name='James '+d+' seated candidate',frameWidth=184,frameHeight=192,pivot=[92,172],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_seated_master_revision',states=[]);hashes={}
 for action,indices in state_indices.items():
  files=[]
  for i,idx in enumerate(indices):
   im=rows[idx]
   if im.size!=(184,192):out=Image.new('RGBA',(184,192));out.alpha_composite(im);im=out
   dest=p/'frames'/action/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True,parents=True);im.save(dest);rel=dest.relative_to(p).as_posix();files.append(rel);hashes[rel]=hashlib.sha256(dest.read_bytes()).hexdigest()
  timing=TIMING.get(action,list(reversed(TIMING['sit-down'])))
  pack['states'].append(dict(id=action+'-'+d,frameCount=6,frameFiles=files,frameDurationsMs=timing,loop=action in ['sit-idle','read-seated'],facings=[d]*6,waterKinds=[action]*6,waterPoses=[False]*6,depthOffsets=[0]*6,provenance=dict(source='source.png',prompt='prompt.txt',fixedScale=float(scale),sourcePoses=indices,derivation='Independent facing, one anatomical scale, foot registration; shared selected standing and seated endpoints; rise reverses sit-down exactly')))
  # Furniture contact also requires the retained depth-order contract.
  for field in ['waterKinds','waterPoses','depthOffsets']:
   pack['states'][-1][field]=copy.deepcopy(retained[action+'-'+d][field])
 (p/'bare-manifest.json').write_text(json.dumps(pack,indent=2)+'\n');(p/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');(p/'registration.json').write_text(json.dumps(dict(fixedScale=float(scale),masterHeight=height,targetFoot=target,goldGain=gain.tolist(),tracking=tracking,sourceSha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest()),indent=2)+'\n')
 contact=Image.new('RGB',(1792,960),'#303b40');draw=ImageDraw.Draw(contact)
 for i,im in enumerate(rows):
  tile=Image.new('RGBA',(256,256));tile.alpha_composite(im,(36,52));contact.paste(tile,(i%6*256,55+i//6*320),tile);draw.text((i%6*256+8,i//6*320+8),d+' pose '+str(i),fill='white')
 ref=Image.new('RGBA',(256,256));ref.alpha_composite(master,(36,52));contact.paste(ref,(1536,55),ref);draw.text((1544,8),'selected standing master',fill='white');contact.save(p/'contact.png')
 boards=[];dur=[]
 for action in ['sit-down','sit-idle','read-seated','sit-rise']:
  s=next(s for s in pack['states'] if s['id']==action+'-'+d)
  for i,f in enumerate(s['frameFiles']):
   im=Image.open(p/f).convert('RGBA');board=Image.new('RGB',(800,330),'#303b40');draw=ImageDraw.Draw(board);draw.text((8,8),'James '+d+' '+action+' / master / 82px / 54px / 27px',fill='white')
   tile=Image.new('RGBA',(256,256));tile.alpha_composite(im,(36,52));board.paste(tile,(0,70),tile);board.paste(ref,(230,70),ref)
   for h,atx in [(82,510),(54,650),(27,740)]:sc=h/148;small=tile.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);board.paste(small,(atx,294-round(224*sc)),small)
   boards.append(board);dur.append(s['frameDurationsMs'][i])
 boards[0].save(p/'review.gif',save_all=True,append_images=boards[1:],duration=dur,loop=0)
 print(d,'24 references, fixed scale',round(scale,5),'gold',np.round(gain,3).tolist())
 return pack,p

if __name__=='__main__':
 import sys
 combined=None
 for d in (sys.argv[1:] or ['east','south','west','north']):
  m,p=build(d)
  if combined is None:combined={k:copy.deepcopy(v) for k,v in m.items() if k!='states'};combined.update(name='James seated family bare candidate',states=[])
  for st in m['states']:
   st=copy.deepcopy(st);st['frameFiles']=[Path(os.path.relpath(p/f,HERE)).as_posix() for f in st['frameFiles']];combined['states'].append(st)
 (HERE/'bare-manifest.json').write_text(json.dumps(combined,indent=2)+'\n')
