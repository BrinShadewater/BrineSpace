from pathlib import Path
import json,hashlib,sys
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];v=int(sys.argv[1]) if len(sys.argv)>1 else 1
raw=P/f'raw-interiors-v{v}.png';a=np.array(Image.open(raw).convert('RGBA'));lab,n=ndimage.label(a[:,:,3]>200);cells=[]
for k in range(1,n+1):
    y,x=np.where(lab==k)
    if len(x)>10000:cells.append((int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1),k))
cells.sort();assert len(cells)==4;cellwidth=a.shape[1]//4;assert cellwidth*4==a.shape[1]
sources=[]
for i,(*box,k) in enumerate(cells):
    c=a[:,i*cellwidth:(i+1)*cellwidth].copy();local=(lab==k)[:,i*cellwidth:(i+1)*cellwidth];c[~ndimage.binary_dilation(local,iterations=3)]=0;sources.append(Image.fromarray(c))
scale=None
for adjust in [0,1,-1,2,-2]:
    h=round(a.shape[0]*148/(cells[0][3]-cells[0][1]))+adjust;s=h/a.shape[0];im=sources[0].resize((round(cellwidth*s),h),Image.Resampling.LANCZOS);ys,xs=np.where(np.array(im)[:,:,3]>200)
    if ys.max()-ys.min()+1==148:scale=s;first=im;floor=int(ys.max());break
assert scale
offset=(round(128-cellwidth*scale/2),224-floor);frames=[]
for i,im in enumerate(sources):
    z=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);f=Image.new('RGBA',(256,256));f.alpha_composite(z,offset);dest=P/f'diagnostic-interiors-v{v}/{i:03}.png';dest.parent.mkdir(exist_ok=True);f.save(dest);frames.append((f'new interior{i+1}',f))
old=[('exact original held',Image.open(R/'character/veld-cargo-north-original-master-v3/frames/bare/000.png').convert('RGBA')),('old gathered target',Image.open(R/'character/veld-turn-north-east-original-master-v1/gather-frames/bare/000.png').convert('RGBA'))]
allframes=[old[0]]+frames+[old[1]];stats=[];board=Image.new('RGB',(1536,570),'#202a30');d=ImageDraw.Draw(board)
for i,(label,im) in enumerate(allframes):
    z=np.array(im);ys,xs=np.where(z[:,:,3]>200);head=np.where(z[int(ys.min()):int(ys.min())+16,:,3]>128)[1];upper=np.where(z[100:140,:,3]>200)[1]
    foot=[]
    for side,lo,hi in [('left',90,128),('right',128,166)]:
        sy,sx=np.where(z[198:225,lo:hi,3]>128);sx+=lo;sy+=198
        foot.append({'side':side,'bounds':[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)],'regionWidth':int(sx.max()-sx.min()+1),'regionCenterX':float((sx.min()+sx.max())/2),'bottom':int(sy.max())})
    neutral=z[142:175,108:149];rgb=neutral[:,:,:3].astype(float);lum=rgb.mean(2);mask=(neutral[:,:,3]>200)&(np.ptp(rgb,axis=2)<15)&(lum>20)&(lum<180)
    stats.append({'source':label,'height':int(ys.max()-ys.min()+1),'headWidth':int(head.max()-head.min()+1),'upperBodyWidth':int(upper.max()-upper.min()+1),'feet':foot,'neutralUpperLegQuartiles':np.percentile(lum[mask],[25,50,75]).tolist()})
    board.paste(im,(i*256,20),im);d.text((i*256+4,4),label,fill='white');crop=im.crop((96,186,160,228));crop=crop.resize((256,168),Image.Resampling.NEAREST);board.paste(crop,(i*256,335),crop)
board.save(P/f'interiors-master-review-v{v}.png');report={'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sourceBoxes':[list(c[:4]) for c in cells],'commonScale':scale,'commonOffset':offset,'registration':'Whole constant-width source cells, one scale and shared nominal horizontal cell axis / first actual resampled floor. No per-pose head/floor fitting.','rows':stats,'postGenerationRGBChanged':False,'status':'diagnostic pending contact/material/master review, not selected'}
(P/f'interiors-audit-v{v}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'scale':scale,'offset':offset,'rows':stats}))
