"""Six complete stop poses; globally resample entire atlas once using first standing."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2];raw=P/'raw-first-lift-v2.png'
original=Image.open(raw).convert('RGBA');a=np.array(original);a[a[:,:,3]==0,:3]=0;original=Image.fromarray(a)
labels,n=ndimage.label(a[:,:,3]>200);sizes=np.bincount(labels.ravel());sizes[0]=0;figures=[]
for k in np.argsort(sizes)[-6:]:
    y,x=np.where(labels==k);figures.append([int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)])
figures.sort(key=lambda b:b[0])
gutters=[0]+[round((figures[i-1][2]+figures[i][0])/2) for i in range(1,6)]+[original.width]
estimate=round(original.height*148/(figures[0][3]-figures[0][1]))
for delta in [0,1,-1,2,-2,3,-3]:
    h=estimate+delta;scale=h/original.height
    atlas=original.resize((round(original.width*scale),h),Image.Resampling.LANCZOS)
    last=atlas.crop((0,0,round(gutters[1]*scale),atlas.height));y,x=np.where(np.array(last)[:,:,3]>200)
    if int(y.max()-y.min()+1)==148:break
else:raise AssertionError('No original148 first standing global atlas ruler')
common_y=223-int(y.max());rows=[];board=Image.new('RGB',(2048,330),'#202a30');d=ImageDraw.Draw(board)
for i in range(6):
    cell=atlas.crop((round(gutters[i]*scale),0,round(gutters[i+1]*scale),atlas.height))
    a=np.array(cell);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1]
    offset=(round(123.5-(hx.min()+hx.max())/2),common_y)
    out=Image.new('RGBA',(256,256));out.alpha_composite(cell,offset)
    path=P/f'diagnostic-frames/{i:03d}.png';path.parent.mkdir(exist_ok=True);out.save(path)
    z=np.array(out);yy,xx=np.where(z[:,:,3]>200);item={'pose':i,'height':int(yy.max()-yy.min()+1),'headWidth':int(hx.max()-hx.min()+1),'floor':int(yy.max()),'top':int(yy.min()),'offset':list(offset),'rawFigureBounds':figures[i],'clipped':bool(np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20))};rows.append(item)
    xy=(i*256,28);board.paste(out,xy,out);d.text((xy[0]+3,8),f"{i} H{item['height']} head{item['headWidth']} floor{item['floor']}",fill='white')
for col,(name,path) in enumerate([('Original held',R/'character/veld-east-held-original-master-v1/frames/bare/000.png'),('Current stride',P.parent/'continuous-video-v3-white/clip-frames/bare/018.png')]):
    im=Image.open(path).convert('RGBA');xy=((6+col)*256,28);board.paste(im,xy,im);d.text((xy[0]+3,8),name,fill='white')
board.save(P/'source-master-review.png')
report={'rawSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sourceSize':list(original.size),'globalScale':scale,'commonYOffset':common_y,'standingRulerPose':0,'rows':rows,'scope':'ONE entire atlas global resample matched actual first standing reference148; component-derived clear gutters, whole X head-axis registration and shared Y only. No per-cell width resampling/per-pose density, floor correction, anatomy or RGB edits. New whole-source first-lift preparation keys, no final animation/native/production acceptance.'}
(P/'source-registration.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'headWidths':[r['headWidth'] for r in rows],'heights':[r['height'] for r in rows],'floors':[r['floor'] for r in rows],'clipped':sum(r['clipped'] for r in rows),'globalScale':scale}))
