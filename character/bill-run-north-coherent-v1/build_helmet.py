from pathlib import Path
import json,copy,hashlib,shutil
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];D=P.parent/'bill-seated-helmet-north-coherent-v1';B=P.parent/'bill-seated-north-coherent-v1'
canon=D/'sources/canonical-head.png';shutil.copy2(canon,P/'sources/north-canonical-helmet.png');head=Image.open(canon).convert('RGBA')
def axis(im):
 a=np.array(im);y,x=np.indices(a.shape[:2]);mask=(a[:,:,3]>180)&(x>=100)&(x<166)&(y>=60)&(y<105);top=int(np.where(mask)[0].min());yy,xx=np.where(mask&(y<top+14));return [float(np.median(xx)),top],[int(xx.min()),int(xx.max()+1)]
authority,_=axis(Image.open(B/'frames/sit-down-north/000.png').convert('RGBA'));reg=json.loads((D/'helmet-registration.json').read_text());bx,by=reg['sourceBox'][:2];base=[bx+36,by+52]
m=copy.deepcopy(json.loads((P/'manifest.json').read_text()));records=[];files=[]
for i,f in enumerate(m['states'][0]['frameFiles']):
 im=Image.open(R/f[6:]).convert('RGBA');a=np.array(im);anchor,bounds=axis(im);pos=[round(base[0]+anchor[0]-authority[0]),round(base[1]+anchor[1]-authority[1])];erase=[bounds[0]-2,anchor[1],bounds[1]+2,anchor[1]+25];x0,y0,x1,y1=erase;a[y0:y1,x0:x1]=0
 out=Image.fromarray(a);out.alpha_composite(head,pos);dest=P/f'frames/helmet/run-north/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);files.append('res://'+dest.relative_to(R).as_posix());records.append({'frame':i,'bareFile':f,'position':pos,'eraseRect':erase,'nativeScale':1,'componentSize':list(head.size),'headAxis':anchor})
m.update(name='Bill native shared-helmet North run candidate',equipment='diving-helmet');m['states'][0]['frameFiles']=files
(P/'helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n');(P/'helmet-registration.json').write_text(json.dumps({'canonicalSha256':hashlib.sha256(canon.read_bytes()).hexdigest(),'idleAxis':authority,'frames':records},indent=2)+'\n')
board=Image.new('RGB',(1792,512),(34,52,62))
for i,f in enumerate([D/'frames/sit-down-north/000.png']+[R/f[6:] for f in files]):
 im=Image.open(f).convert('RGBA');board.paste(im,(i*256,0),im);small=im.resize((142,142),Image.Resampling.LANCZOS);board.paste(small,(i*256+57,320),small)
board.save(P/'helmet-master-review.png');print('Fitted6 native shared helmets; body preserved outside bounded head region')
