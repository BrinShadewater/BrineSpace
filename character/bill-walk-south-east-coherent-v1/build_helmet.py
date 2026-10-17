"""Reuse the accepted quarter-angle helmet through its frozen source recipe."""
from pathlib import Path
import json,copy,hashlib,shutil
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];D=P.parent/'bill-carry-turn-helmet-east-south-v1';B=P.parent/'bill-carry-turn-east-south-v1'
shutil.copy2(D/'sources/helmet-angle-atlas-v1.png',P/'sources/accepted-helmet-angle-atlas.png');shutil.copy2(D/'helmet-registration.json',P/'sources/accepted-helmet-recipe.json')
reg=json.loads((P/'sources/accepted-helmet-recipe.json').read_text());cell=Image.open(P/'sources/accepted-helmet-angle-atlas.png').convert('RGBA').crop((1024,0,1280,256));a=np.array(cell);yy,xx=np.where(a[:,:,3]>160);box=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];h=cell.crop((box[0]-2,box[1]-2,box[2]+2,box[3]+2));p=np.array(h);rgb=p[:,:,:3].astype(float);y,x=np.indices(p.shape[:2]);weight=np.clip((25-np.ptp(rgb,axis=2))/15,0,1);mapped=np.interp(rgb.mean(2),reg['curveInput'],reg['curveOutput']);weight[(rgb.mean(2)>185)&(y<60)]=0;tone=np.stack([mapped+.7,mapped,mapped-.5],axis=2);p[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+tone*weight[:,:,None],0,255)
skin=(p[:,:,3]>0)&(y>h.height*.2)&(rgb[:,:,0]>rgb[:,:,1]+12)&(rgb[:,:,0]>rgb[:,:,2]+20)&(rgb.mean(2)>50);p[skin,:3]=np.clip(rgb[skin]*reg['skinGain'],0,255)
glass=(p[:,:,3]>0)&(rgb[:,:,2]>rgb[:,:,0]+10)&(rgb[:,:,2]>rgb[:,:,1]+3)&(rgb.mean(2)>55);p[glass,:3]=np.clip(rgb[glass]*reg['visorGain'],0,255)
head=Image.fromarray(p).resize((round(h.width*reg['scale'][0]),round(h.height*reg['scale'][1])),Image.Resampling.LANCZOS);assert head.size==(39,43);head.save(P/'sources/quarter-canonical-helmet.png')
def axis(im):
 a=np.array(im);y,x=np.indices(a.shape[:2]);mask=(a[:,:,3]>180)&(x>=100)&(x<166)&(y>=60)&(y<105);top=int(np.where(mask)[0].min());yy,xx=np.where(mask&(y<top+14));return [float(np.median(xx)),top],[int(xx.min()),int(xx.max()+1)]
authority,_=axis(Image.open(B/'frames/carry-turn-east-south/004.png').convert('RGBA'));base=[107,65]
m=copy.deepcopy(json.loads((P/'manifest.json').read_text()));files=[];records=[]
for i,f in enumerate(m['states'][0]['frameFiles']):
 im=Image.open(R/f[6:]).convert('RGBA');a=np.array(im);anchor,bounds=axis(im);pos=[round(base[0]+anchor[0]-authority[0]),round(base[1]+anchor[1]-authority[1])];erase=[bounds[0]-2,anchor[1],bounds[1]+2,anchor[1]+25];x0,y0,x1,y1=erase;a[y0:y1,x0:x1]=0;out=Image.fromarray(a);out.alpha_composite(head,pos);dest=P/f'frames/helmet/walk-south-east/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);files.append('res://'+dest.relative_to(R).as_posix());records.append({'frame':i,'bareFile':f,'position':pos,'eraseRect':erase,'nativeScale':1,'componentSize':list(head.size),'headAxis':anchor})
m.update(name='Bill southeast native shared-helmet walk candidate',equipment='diving-helmet');m['states'][0]['frameFiles']=files
(P/'helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n');(P/'helmet-registration.json').write_text(json.dumps({'canonicalSha256':hashlib.sha256((P/'sources/quarter-canonical-helmet.png').read_bytes()).hexdigest(),'sourceAuthority':'character/bill-carry-turn-helmet-east-south-v1/frames/carry-turn-east-south/004.png','authorityPosition':base,'idleAxis':authority,'frames':records},indent=2)+'\n')
board=Image.new('RGB',(1792,512),(34,52,62))
for i,f in enumerate([D/'frames/carry-turn-east-south/004.png']+[R/f[6:] for f in files]):
 im=Image.open(f).convert('RGBA');board.paste(im,(i*256,0),im);small=im.resize((142,142),Image.Resampling.LANCZOS);board.paste(small,(i*256+57,320),small)
board.save(P/'helmet-master-review.png');print('Six candidate quarter helmets fitted at native39x43')
