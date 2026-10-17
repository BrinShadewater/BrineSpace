"""Source-authored water helmet pitch; unchanged body pixels outside owned head."""
from pathlib import Path
import json,copy,os,hashlib
import numpy as np
from PIL import Image,ImageDraw
from extract_sources import extract
P=Path(__file__).resolve().parent;R=P.parents[1];combined=None;reviews=[]
for d in ['east','south','west','north']:
 p=P.parent/('james-water-'+d+'-v1');bare=json.loads((p/'bare-manifest.json').read_text());reg=json.loads((p/'registration.json').read_text());donors=extract(p/'source-helmet.png',6,6);master=Image.open(P.parent/('james-lying-'+d+'-v1')/'selected-helmet-master.png').convert('RGBA');ma=np.array(master);yy,xx=np.indices(ma.shape[:2]);mask=ma[:,:,3]>180;top=int(np.where(mask)[0].min());y,x=np.where(mask&(yy<top+28));master_width=int(x.max()-x.min()+1)
 first=np.array(donors[0][0]);yy0,xx0=np.indices(first.shape[:2]);ym,xm=np.where((first[:,:,3]>180)&(yy0<round(first.shape[0]*.72)));source_width=int(xm.max()-xm.min()+1);scale=master_width/source_width
 oldreg=json.loads((P.parent/('james-lying-'+d+'-v1')/'helmet-registration.json').read_text());offset=np.array(oldreg['centerOffset'])+[0,5 if d=='south' else (3 if d in ['east','west'] else 0)]
 rows={};records={};patches=[]
 for cell,box in donors:
  a=np.array(cell);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);neutral=(a[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);rgb[neutral]*=.9;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');cell=Image.fromarray(a);patches.append(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS))
 for i in sorted(set(j for s in bare['states'] for j in s['provenance']['sourcePoses'])):
  owner=next(s for s in bare['states'] if i in s['provenance']['sourcePoses']);j=owner['provenance']['sourcePoses'].index(i);body=Image.open(p/owner['frameFiles'][j]).convert('RGBA');a=np.array(body);yy,xx=np.indices(a.shape[:2]);point=np.array(reg['tracking'][i]['headAnchor'])
  if i<6:di=0
  elif i<12:di=5 if i in [7,8,9] else 4
  elif i<18:di=i-12
  else:di=i-17
  if d=='north' and di in [2,3]:di=1 if di==2 else 4 # Reject sideways-tilted donor heads; source preserved.
  patch=patches[di];target=point+offset;pos=np.rint(target-[patch.width/2,patch.height/2]).astype(int);erase=((xx-point[0])/14)**2+((yy-(point[1]-1))/14)**2<=1;a[erase]=0;out=Image.fromarray(a);out.alpha_composite(patch,tuple(pos))
  # North overhead reach: restore original gloves above the cranium, never bare hair.
  foreground=np.zeros(a.shape[:2],bool)
  if d=='north' and (i in [6,20,21]):foreground=(yy<point[1]-12)&(np.array(body)[:,:,3]>0);b=np.array(out);b[foreground]=np.array(body)[foreground];out=Image.fromarray(b)
  region=[min(int(point[0]-14),int(pos[0])),min(int(point[1]-15),int(pos[1])),max(int(point[0]+15),int(pos[0])+patch.width),max(int(point[1]+14),int(pos[1])+patch.height)]
  rows[i]=out;records[str(i)]=dict(sourceHead=di,sourceHeadBox=donors[di][1],fixedHeadScale=scale,position=pos.tolist(),editRegion=region,neutralShellGain=.9,foreground='Original north gloves above cranial ownership' if foreground.any() else None)
 eq=copy.deepcopy(bare);eq['name']='James '+d+' water shared helmet staged';hashes={}
 for s in eq['states']:
  files=[]
  for j,i in enumerate(s['provenance']['sourcePoses']):
   f=p/'frames/helmet'/s['id'].rsplit('-',1)[0]/f'{j:03d}.png';f.parent.mkdir(parents=True,exist_ok=True);rows[i].save(f);rel=f.relative_to(p).as_posix();files.append(rel);hashes[rel]=hashlib.sha256(f.read_bytes()).hexdigest()
  s['frameFiles']=files;s['provenance'].update(helmetSource='source-helmet.png',helmetDerivation='Independent water pitch donors, fixed master-shell scale, owned cranial erase, source body retained outside head edit region')
 (p/'helmet-manifest.json').write_text(json.dumps(eq,indent=2)+'\n');(p/'helmet-registration.json').write_text(json.dumps(dict(masterShellWidth=master_width,sourceShellWidth=source_width,fixedHeadScale=scale,centerOffset=offset.tolist(),sourceSha256=hashlib.sha256((p/'source-helmet.png').read_bytes()).hexdigest(),tracking=records,status='staged_fit_review'),indent=2)+'\n');(p/'helmet-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
 board=Image.new('RGB',(1792,1280),'#303b40');dr=ImageDraw.Draw(board)
 for row,s in enumerate(eq['states']):
  for j,i in enumerate(s['provenance']['sourcePoses']):at=(j*256,38+row*312);board.paste(rows[i],at,rows[i]);dr.text((at[0]+8,at[1]-27),s['id']+' '+str(j),fill='white')
 full=Image.new('RGBA',(256,276));full.alpha_composite(master,(36,66));board.paste(full,(1536,38),full);dr.text((1544,10),'selected helmet master',fill='white');board.save(p/'helmet-contact.png')
 if combined is None:combined={k:copy.deepcopy(v) for k,v in eq.items() if k!='states'};combined.update(name='James directional water shared helmets staged',states=[])
 for s in eq['states']:s=copy.deepcopy(s);s['frameFiles']=[Path(os.path.relpath(p/f,P)).as_posix() for f in s['frameFiles']];combined['states'].append(s)
 reviews.append((d,rows,{s['id'].rsplit('-',1)[0]:s['provenance']['sourcePoses'] for s in eq['states']}));print(d,'24 helmet refs, shell ruler',master_width,source_width,'scale',round(scale,5))
(P/'helmet-manifest.json').write_text(json.dumps(combined,indent=2)+'\n')
seq=[('tread',j,160) for j in range(6)]+[('swim-start',j,t) for j,t in enumerate([70,90,100,100,90,70])]+[('swim',j,160) for _ in range(2) for j in range(6)]+[('swim-stop',j,t) for j,t in enumerate([70,90,100,100,90,70])]
gif=[];dur=[]
for action,j,t in seq:
 im=Image.new('RGB',(1024,640),'#303b40');dr=ImageDraw.Draw(im)
 for k,(d,rows,ids) in enumerate(reviews):
  folder=P.parent/('james-water-'+d+'-v1');b=Image.open(folder/'frames'/action/f'{j:03d}.png').convert('RGBA');e=rows[ids[action][j]]
  for row,sprite in enumerate([b,e]):im.paste(sprite,(k*256,40+row*312),sprite);dr.text((k*256+8,8+row*312),d+' '+action+' '+('bare' if row==0 else 'helmet'),fill='white')
 gif.append(im);dur.append(t)
gif[0].save(P/'paired-review.gif',save_all=True,append_images=gif[1:],duration=dur,loop=0,disposal=2,optimize=False)
