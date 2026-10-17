from pathlib import Path
import hashlib,json,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parents[1];v=int(sys.argv[1]) if len(sys.argv)>1 else 1
raw=P/f'raw-corrected-gather-v{v}.png';a=np.array(Image.open(raw).convert('RGBA'));labels,n=ndimage.label(a[:,:,3]>200);counts=np.bincount(labels.ravel());counts[0]=0;k=int(counts.argmax());ys,xs=np.where(labels==k)
box=(max(0,int(xs.min())-5),max(0,int(ys.min())-5),min(a.shape[1],int(xs.max())+6),min(a.shape[0],int(ys.max())+6));x0,y0,x1,y1=box;c=a[y0:y1,x0:x1].copy();c[~ndimage.binary_dilation((labels==k)[y0:y1,x0:x1],iterations=3)]=0
for adjust in [0,1,-1,2,-2,3,-3]:
    h=round(c.shape[0]*148/(ys.max()-ys.min()+1))+adjust;scale=h/c.shape[0];im=Image.fromarray(c).resize((round(c.shape[1]*scale),h),Image.Resampling.LANCZOS);z=np.array(im);yy,xx=np.where(z[:,:,3]>200)
    if yy.max()-yy.min()+1==148:break
else:raise AssertionError('No exact whole standing ruler')
top=int(yy.min());hx=np.where(z[top:top+16,:,3]>128)[1];offset=(round(128-(hx.min()+hx.max())/2),224-int(yy.max()));frame=Image.new('RGBA',(256,256));frame.alpha_composite(im,offset);frame.save(P/f'diagnostic-corrected-gather-v{v}.png')
sources=[('original held',Image.open(R/'character/veld-cargo-north-original-master-v3/frames/bare/000.png').convert('RGBA')),('old gathered',Image.open(R/'character/veld-turn-north-east-original-master-v1/gather-frames/bare/000.png').convert('RGBA')),('corrected gathered',frame)]
stats=[];board=Image.new('RGB',(768,580),'#202a30');d=ImageDraw.Draw(board)
for i,(label,f) in enumerate(sources):
    z=np.array(f);yy,xx=np.where(z[:,:,3]>200);head=np.where(z[int(yy.min()):int(yy.min())+16,:,3]>128)[1];upper=np.where(z[100:140,:,3]>200)[1]
    feet=[]
    for lo,hi in [(90,128),(128,166)]:
        fy,fx=np.where(z[214:225,lo:hi,3]>128);feet.append({'width':int(fx.max()-fx.min()+1),'centerX':float(lo+(fx.min()+fx.max())/2),'bottom':int(fy.max()+214)})
    neutral=z[142:175,108:149];rgb=neutral[:,:,:3].astype(float);lum=rgb.mean(2);mask=(neutral[:,:,3]>200)&(np.ptp(rgb,axis=2)<15)&(lum>20)&(lum<180)
    stats.append({'source':label,'height':int(yy.max()-yy.min()+1),'headWidth':int(head.max()-head.min()+1),'upperBodyWidth':int(upper.max()-upper.min()+1),'feet':feet,'neutralUpperLegQuartiles':np.percentile(lum[mask],[25,50,75]).tolist()})
    board.paste(f,(i*256,25),f);d.text((i*256+4,4),label,fill='white');crop=f.crop((96,186,160,228)).resize((256,168),Image.Resampling.NEAREST);board.paste(crop,(i*256,330),crop)
board.save(P/f'corrected-gather-master-review-v{v}.png');report={'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sourceBox':list(box),'commonScale':scale,'offset':list(offset),'rows':stats,'postGenerationRGBChanged':False,'status':'diagnostic source/master review pending, not selected'}
(P/f'corrected-gather-audit-v{v}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(stats))
