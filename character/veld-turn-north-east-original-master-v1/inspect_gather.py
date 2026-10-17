from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parents[1];version=int(sys.argv[1]) if len(sys.argv)>1 else 1;suffix='' if version==1 else f'-v{version}';raw=P/f'raw-gather-v{version}.png';a=np.array(Image.open(raw).convert('RGBA'));lab,n=ndimage.label(a[:,:,3]>200);sizes=np.bincount(lab.ravel());sizes[0]=0;k=int(sizes.argmax());yy,xx=np.where(lab==k)
box=(max(0,int(xx.min())-5),max(0,int(yy.min())-5),min(a.shape[1],int(xx.max())+6),min(a.shape[0],int(yy.max())+6));lo,up,hi,down=box;cell=a[up:down,lo:hi].copy();cell[~ndimage.binary_dilation((lab==k)[up:down,lo:hi],iterations=3)]=0;scales=[]
for adjust in [0,1,-1,2,-2,3,-3]:
    h=round(cell.shape[0]*148/(yy.max()-yy.min()+1))+adjust;s=h/cell.shape[0];im=Image.fromarray(cell).resize((round(cell.shape[1]*s),h),Image.Resampling.LANCZOS);z=np.array(im);ys,xs=np.where(z[:,:,3]>200)
    if ys.max()-ys.min()+1==148:scales.append((s,im))
assert scales;scale,im=scales[0];b=np.array(im);ys,xs=np.where(b[:,:,3]>200);top=int(ys.min());hx=np.where(b[top:top+16,:,3]>128)[1];offset=(round(128-(hx.min()+hx.max())/2),224-int(ys.max()));frame=Image.new('RGBA',(256,256));frame.alpha_composite(im,offset);frame.save(P/('diagnostic-gather'+suffix+'.png'))
held=Image.open(R/'character/veld-cargo-north-original-master-v3/frames/bare/000.png').convert('RGBA');board=Image.new('RGB',(768,285),'#202a30');d=ImageDraw.Draw(board);stats=[]
for i,(label,f) in enumerate([('latest exact held',held),('new gather',frame)]):
    z=np.array(f);ys,xs=np.where(z[:,:,3]>200);head=np.where(z[int(ys.min()):int(ys.min())+16,:,3]>128)[1];upper=np.where(z[100:140,:,3]>200)[1];foot=np.where(z[216:225,:,3]>200)[1]
    neutral=z[142:175,108:149];rgb=neutral[:,:,:3].astype(float);lum=rgb.mean(2);mask=(neutral[:,:,3]>200)&(np.ptp(rgb,axis=2)<15)&(lum>20)&(lum<180)
    stats.append({'source':label,'height':int(ys.max()-ys.min()+1),'headRegionWidth':int(head.max()-head.min()+1),'upperBodyWidth':int(upper.max()-upper.min()+1),'bootRegionWidth':int(foot.max()-foot.min()+1),'bootY':int(ys.max()),'neutralUpperLegQuartiles':np.percentile(lum[mask],[25,50,75]).tolist()});board.paste(f,(i*256,22),f);d.text((i*256+5,4),label,fill='white')
board.save(P/('gather-master-comparison'+suffix+'.png'));(P/('gather-audit'+suffix+'.json')).write_text(json.dumps({'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'scale':float(scale),'sourceBox':box,'offset':offset,'rows':stats,'postGenerationRGBChanged':False,'status':'diagnostic_not_selected; source/stance/material and continuous gather transition remain to review'},indent=2)+'\n');print(json.dumps(stats))
