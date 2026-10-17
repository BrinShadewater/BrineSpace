"""Register independently generated meal sources; fixed scale, preserved perspective."""
from pathlib import Path
import json,hashlib,copy,os
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
ROOT=Path(__file__).resolve().parents[2]
GAINS={'east':[.756,.843,.786],'south':[.855,.95,1.359],'west':[.895,1.018,1.333],'north':[.907,1.0,1.152]}
TIMING={'eat':[250,200,200,350,200,300],'drink':[350,350,450,850,400,600]}
def figures(path):
 raw=Image.open(path).convert('RGBA');a=np.array(raw);labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;ids=sorted(np.argsort(counts)[-12:],key=lambda k:np.where(labs==k)[0].mean());out=[]
 for row in range(2):
  keys=sorted(ids[row*6:row*6+6],key=lambda k:np.where(labs==k)[1].mean());centers=[np.where(labs==k)[1].mean() for k in keys];edges=[0]+[round((centers[i]+centers[i+1])/2) for i in range(5)]+[raw.width]
  for i,k in enumerate(keys):
   yy,xx=np.where(labs==k);y0=max(0,int(yy.min())-3);y1=min(raw.height,int(yy.max())+4);cell=a[y0:y1,edges[i]:edges[i+1]].copy();primary=labs[y0:y1,edges[i]:edges[i+1]]==k;cell[~binary_dilation(primary,iterations=2)]=0;out.append(Image.fromarray(cell))
 return out
def feet(im):
 a=np.array(im);yy,xx=np.where(a[:,:,3]>180);floor=yy.max();mask=(a[:,:,3]>180)&(np.indices(a.shape[:2])[0]>=floor-4);y,x=np.where(mask);return float(x.mean()),int(floor)
def grade(im,d):
 a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>180)[0].min();gold=(a[:,:,3]>0)&(r-b>35)&(g-b>20)&(yy>top+30)&(yy<top+86);body=(a[:,:,3]>0)&(yy>top+30)&~gold;lum=rgb.mean(2);mapped=np.interp(lum,[0,50,70,90,120,160,200,255],[0,50,68,80,99,126,149,170]);gain=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0);rgb[body]*=gain[body,None];rgb[gold]*=GAINS[d];a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');return Image.fromarray(a)
def build(d):
 p=ROOT/'character'/('james-meal-'+d+'-v1');cells=figures(p/'source.png');folder=ROOT/'character/crew-runtime-matte-v1/branforth';m=json.loads((folder/'manifest.json').read_text());st=next(s for s in m['states'] if s['id']=='idle-'+d);master=Image.open(folder/st['frameFiles'][0]).convert('RGBA');ma=np.array(master);my,mx=np.where(ma[:,:,3]>180);height=int(my.max()-my.min()+1);y,x=np.where(np.array(cells[0])[:,:,3]>180);scale=height/(y.max()-y.min()+1);target=feet(master);rows=[];records=[];hashes={}
 for i,cell in enumerate(cells):
  anchor=feet(cell);at=(round(target[0]-anchor[0]*scale),round(target[1]-anchor[1]*scale));out=Image.new('RGBA',(184,192));out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),at);ungraded=out.copy();out=grade(out,d);rows.append(out);records.append(dict(sourcePose=i,position=at));u=p/'registered-ungraded'/f'{i:03d}.png';u.parent.mkdir(exist_ok=True);ungraded.save(u)
 for base in [0,6]:rows[base+5]=rows[base].copy();records[base+5]=dict(records[base],sharedNeutralEndpoint=True)
 pack=dict(name='James '+d+' meals',frameWidth=184,frameHeight=192,pivot=[92,172],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_master_matched_meals_owner_review_pending',states=[])
 eq=copy.deepcopy(pack);eq['name']+=' sealed-helmet substitutes';im=json.loads((ROOT/'character/james-inspect-tablet-v1/helmet-manifest.json').read_text());inspect=next(s for s in im['states'] if s['id']=='inspect-'+d);eq['frameHeight']=im['frameHeight'];indices=[0,int(len(inspect['frameFiles'])*.18),int(len(inspect['frameFiles'])*.4),int(len(inspect['frameFiles'])*.6),int(len(inspect['frameFiles'])*.8),len(inspect['frameFiles'])-1]
 for action,base in [('eat',0),('drink',6)]:
  files=[]
  for i in range(6):
   dest=p/'frames'/action/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True,parents=True);rows[base+i].save(dest);rel=dest.relative_to(p).as_posix();files.append(rel);hashes[rel]=hashlib.sha256(dest.read_bytes()).hexdigest()
  state=dict(id=action+'-'+d,frameCount=6,frameFiles=files,frameDurationsMs=TIMING[action],loop=True,facings=[d]*6,waterKinds=[action]*6,waterPoses=[False]*6,depthOffsets=[0]*6,provenance=dict(source='source.png',prompt='prompt.txt',independentFacing=d,fixedScale=float(scale),sourcePoses=[base+i if i!=5 else base for i in range(6)],materialGain=GAINS[d],derivation='Independent meal source at one fixed scale; translated by source foot anchor, no per-frame resizing; exact shared neutral loop endpoint'))
  pack['states'].append(state);sub=copy.deepcopy(state);sub['frameFiles']=[Path(os.path.relpath((ROOT/'character/james-inspect-tablet-v1'/inspect['frameFiles'][i]).resolve(),p)).as_posix() for i in indices];sub['provenance']=dict(visualSubstitution='Closed-helmet tablet inspection; crew_life selects inspect instead of food action',sourceManifest='character/james-inspect-tablet-v1/helmet-manifest.json',sourceState=inspect['id'],sourcePoses=indices,originalPixels=True);eq['states'].append(sub)
 for mode,value in [('bare',pack),('helmet',eq)]:(p/(mode+'-manifest.json')).write_text(json.dumps(value,indent=2)+'\n')
 (p/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');(p/'registration.json').write_text(json.dumps(dict(fixedScale=float(scale),masterHeight=height,targetFoot=target,tracking=records,sourceSha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),goldGain=GAINS[d]),indent=2)+'\n')
 boards=[];times=[];contact=Image.new('RGB',(1792,640),'#303b40');draw=ImageDraw.Draw(contact)
 for row,action in enumerate(['eat','drink']):
  for i in range(6):
   body=rows[row*6+i];full=Image.new('RGBA',(256,256));full.alpha_composite(body,(36,52));contact.paste(full,(i*256,row*320+55),full);draw.text((i*256+6,row*320+8),action+' '+d+' '+str(i),fill='white')
  full=Image.new('RGBA',(256,256));full.alpha_composite(master,(36,52));contact.paste(full,(1536,row*320+55),full);draw.text((1542,row*320+8),'selected master',fill='white')
  for repeat in range(4 if action=='eat' else 2):
   for i in range(6):
    board=Image.new('RGB',(800,330),'#303b40');draw=ImageDraw.Draw(board);draw.text((8,8),'James '+d+' '+action+' / master / 82px / 54px / 27px',fill='white');full=Image.new('RGBA',(256,256));full.alpha_composite(rows[row*6+i],(36,52));board.paste(full,(0,70),full);reference=Image.new('RGBA',(256,256));reference.alpha_composite(master,(36,52));board.paste(reference,(230,70),reference)
    for h,x in [(82,510),(54,650),(27,740)]:sc=h/148;small=full.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);board.paste(small,(x,294-round(224*sc)),small)
    boards.append(board);times.append(TIMING[action][i])
 contact.save(p/'contact.png');boards[0].save(p/'review.gif',save_all=True,append_images=boards[1:],duration=times,loop=0);(p/'index.html').write_text('<style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>James '+d+' meals</h1><p>Staged independently drawn eating and drinking. Sealed helmet uses inspection substitute.</p><img src="review.gif"><img src="contact.png">');print(d,'12 bare frames,2 equipped inspection substitutions, fixed scale',scale)
if __name__=='__main__':
 import sys
 for d in (sys.argv[1:] or ['east','south','west','north']):build(d)
