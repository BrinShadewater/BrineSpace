from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2]
raw=Image.open(P/'raw-source.png').convert('RGBA');pitch=517;origin=6;first=raw.crop((origin,0,origin+pitch,raw.height))
# Calibrate the one whole-source ruler once from first pose; freeze for all cells.
base=round(raw.height*148/684)
for delta in [0,1,-1,2,-2]:
 height=base+delta;size=(round(pitch*height/raw.height),height);one=first.resize(size,Image.Resampling.LANCZOS);y,x=np.where(np.asarray(one)[:,:,3]>200)
 if y.max()-y.min()+1==148:break
else:raise AssertionError('No common standing ruler')
scale=height/raw.height;offset=(128-round(size[0]/2),224-int(y.max()));master=Image.open(P.parent/'clean-idle-master.png').convert('RGBA');imgs=[];rows=[]
for i in range(4):
 cell=raw.crop((origin+i*pitch,0,origin+(i+1)*pitch,raw.height));im=cell.resize(size,Image.Resampling.LANCZOS);plate=Image.new('RGBA',(256,256));plate.alpha_composite(im,offset);imgs.append(plate);a=np.asarray(plate);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];rows.append(dict(frame=i,height=int(y.max()-y.min()+1),floor=int(y.max()),top=top,left=int(x.min()),right=int(x.max()),headWidth=int(hx.max()-hx.min()+1),headAxis=float((hx.min()+hx.max())/2)))
 dest=P/'diagnostic-frames'/f'{i:03}.png';dest.parent.mkdir(exist_ok=True);plate.save(dest)
board=Image.new('RGB',(1280,560),'#202a30');d=ImageDraw.Draw(board)
for j,im in enumerate([master]+imgs):
 board.paste(im,(j*256,24),im);d.text((j*256+4,4),'Prepared master' if j==0 else f'Authored {j-1}',fill='white');crop=im.crop((96,64,160,128)).resize((256,256),Image.Resampling.NEAREST);board.paste(crop,(j*256,288),crop)
board.save(P/'fixed-grid-master-comparison.png');imgs[0].save(P/'fixed-grid-diagnostic.png',save_all=True,append_images=imgs[1:],duration=[375]*4,loop=0,disposal=0,blend=0)
(P/'REGISTRATION_REVIEW.json').write_text(json.dumps(dict(rows=rows,grid=dict(origin=origin,pitch=pitch),scale=scale,offset=list(offset),resize=list(size),sourceAlphaPreserved=True,scope='One global ruler from first pose; uniform grid, unchanged source RGB/alpha except common resampling. Not native/adopted.',sourceSHA256=hashlib.sha256((P/'raw-source.png').read_bytes()).hexdigest()),indent=2)+'\n');print(json.dumps(dict(rows=rows,scale=scale,offset=offset)))
