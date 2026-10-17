from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
pack=json.loads((HERE/'bare-manifest.json').read_text());reg=json.loads((HERE/'registration.json').read_text());source=Image.open(HERE/'source-helmet.png').convert('RGBA');scale=reg['fixedScale']
head_boxes=[[149,106,260,205],[579,181,690,291],[867,209,984,313],[1209,272,1326,370],[67,683,181,784],[436,751,554,858],[851,793,959,898]]
selected=Image.open(HERE/'selected-helmet-master.png').convert('RGBA');standing=Image.new('RGBA',(256,256));standing.alpha_composite(selected,(36,52));rows=[];tracking=[]
for i,box in enumerate(head_boxes):
 crop=source.crop(box);a=np.array(crop);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);neutral=(a[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);rgb[neutral]*=.9;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');crop=Image.fromarray(a)
 info=reg['tracking'][i];sb=info['sourceBox'];at=info['translation'];pos=[round(at[0]+(box[0]-sb[0])*scale),round(at[1]+(box[1]-sb[1])*scale)];patch=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
 body=Image.open(HERE/'frames/bare/bunk-enter'/f'{i:03d}.png').convert('RGBA');base=np.array(body);x0,y0,x1,y1=info['protectedHeadBox'];base[y0:y1,x0:x1]=0;out=Image.fromarray(base);out.alpha_composite(patch,tuple(pos));region=[min(x0,pos[0]),min(y0,pos[1]),max(x1,pos[0]+patch.width),max(y1,pos[1]+patch.height)]
 if i==0:out=standing.copy()
 rows.append(out);tracking.append(dict(sourceHeadBox=box,position=pos,editRegion=region,fixedHeadScale=scale,neutralHeadGain=.9,exactStandingMaster=i==0))
eq=copy.deepcopy(pack);eq['name']='James master-matched east bunk shared helmet';hashes={}
for st in eq['states']:
 files=[]
 for j,i in enumerate(st['provenance']['sourcePoses']):
  p=HERE/'frames/helmet'/st['id'].rsplit('-',1)[0]/f'{j:03d}.png';p.parent.mkdir(parents=True,exist_ok=True);rows[i].save(p);f=p.relative_to(HERE).as_posix();files.append(f);hashes[f]=hashlib.sha256(p.read_bytes()).hexdigest()
 st['frameFiles']=files;st['provenance']['helmetSource']='source-helmet.png';st['provenance']['helmetPrompt']='helmet-prompt.txt';st['provenance']['helmetDerivation']='New coherent head angles at one fixed source scale, body outside recorded head region unchanged, exact selected standing shell arrival'
(HERE/'helmet-manifest.json').write_text(json.dumps(eq,indent=2)+'\n');(HERE/'helmet-registration.json').write_text(json.dumps(dict(tracking=tracking,sourceSha256=hashlib.sha256((HERE/'source-helmet.png').read_bytes()).hexdigest()),indent=2)+'\n');(HERE/'helmet-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
contact=Image.new('RGB',(1792,640),'#303b40');draw=ImageDraw.Draw(contact)
for i,im in enumerate(rows):contact.paste(im,(i*256,50),im);draw.text((i*256+8,8),'helmet '+str(i),fill='white');b=Image.open(HERE/'frames/bare/bunk-enter'/f'{i:03d}.png');contact.paste(b,(i*256,370),b);draw.text((i*256+8,328),'bare '+str(i),fill='white')
contact.save(HERE/'paired-contact.png');print('15 helmet references; fixed source scale',scale)
