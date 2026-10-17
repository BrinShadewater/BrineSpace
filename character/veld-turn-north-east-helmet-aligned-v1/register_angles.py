from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parents[1];raw=P/'raw-angles-v1.png';a=np.array(Image.open(raw).convert('RGBA'));labels,n=ndimage.label(a[:,:,3]>160);cells=[]
for k in range(1,n+1):
    y,x=np.where(labels==k)
    if len(x)>4000:cells.append((int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1),k))
cells.sort();assert len(cells)==2,len(cells);source=[]
for x0,y0,x1,y1,k in cells:
    pad=4;lo=max(0,x0-pad);hi=min(a.shape[1],x1+pad);up=max(0,y0-pad);down=min(a.shape[0],y1+pad);c=a[up:down,lo:hi].copy();c[~ndimage.binary_dilation((labels==k)[up:down,lo:hi],iterations=3)]=0;source.append(Image.fromarray(c))
scale=38/source[1].height;rows=[];board=Image.new('RGB',(4*290,330),'#202a30');d=ImageDraw.Draw(board)
for i,im in enumerate(source):
    shell=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);dest=P/'shells'/f'{i:03}.png';dest.parent.mkdir(exist_ok=True);shell.save(dest);assert 35<=shell.height<=40,shell.size
    rows.append({'angleFromRear':[60,78][i],'nativeSize':list(shell.size),'sourceCoreBox':list(cells[i][:4]),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()});big=shell.resize((shell.width*7,shell.height*7),Image.Resampling.NEAREST);board.paste(big,(i*290+15,30),big);d.text((i*290+10,5),f'new {[60,78][i]}deg {shell.size}',fill='white')
for i,index in enumerate([4,5]):
    shell=Image.open(R/f'character/veld-helmet-original-turntable-v1/v3-study/shells/{index:03}.png').convert('RGBA');big=shell.resize((shell.width*7,shell.height*7),Image.Resampling.NEAREST);board.paste(big,((i+2)*290+15,30),big);d.text(((i+2)*290+10,5),f'old whole shell{index} {shell.size}',fill='white')
board.save(P/'angular-source-comparison.png');(P/'source-registration.json').write_text(json.dumps({'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'commonScale':scale,'nearProfileWholeHeight':38,'rows':rows,'postGenerationRGBChanged':False,'status':'source_only_pending_angle/material/design_review'},indent=2)+'\n');print(json.dumps({'scale':scale,'rows':rows}))
