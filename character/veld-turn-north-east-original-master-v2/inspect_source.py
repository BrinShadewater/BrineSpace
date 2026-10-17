from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parents[1];version=int(sys.argv[1]) if len(sys.argv)>1 else 1;suffix='' if version==1 else f'-v{version}';raw=P/f'raw-turn-v{version}.png';a=np.array(Image.open(raw).convert('RGBA'))
lab,n=ndimage.label(a[:,:,3]>200);cells=[]
for k in range(1,n+1):
    yy,xx=np.where(lab==k)
    if len(xx)>10000:cells.append((int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1),k))
cells.sort();assert len(cells)==6,len(cells)
first=a[:,:((cells[0][2]+cells[1][0])//2)].copy();labels,count=ndimage.label(first[:,:,3]>200);sizes=np.bincount(labels.ravel());sizes[0]=0;first[~ndimage.binary_dilation(labels==int(sizes.argmax()),iterations=3)]=0
scales=[];ruler_floor=None
for adjust in [0,1,-1,2,-2,3,-3]:
    h=round(a.shape[0]*148/(cells[0][3]-cells[0][1]))+adjust;scale=h/a.shape[0];test=np.array(Image.fromarray(first).resize((round(first.shape[1]*scale),h),Image.Resampling.LANCZOS));yy,xx=np.where(test[:,:,3]>200)
    if yy.max()-yy.min()+1==148:
        scales.append(scale)
        if ruler_floor is None:ruler_floor=int(yy.max())
assert scales;scale=scales[0];rows=[];board=Image.new('RGB',(7*256,580),'#202a30');d=ImageDraw.Draw(board)
held=Image.open(R/'character/veld-cargo-north-original-master-v3/frames/bare/000.png').convert('RGBA')
for i,(x0,y0,x1,y1,k) in enumerate(cells):
    lo=0 if i==0 else(cells[i-1][2]+x0)//2;hi=a.shape[1] if i==5 else(x1+cells[i+1][0])//2
    cell=a[:,lo:hi].copy();local,_=ndimage.label(cell[:,:,3]>200);sz=np.bincount(local.ravel());sz[0]=0;cell[~ndimage.binary_dilation(local==int(sz.argmax()),iterations=3)]=0
    im=Image.fromarray(cell).resize((round(cell.shape[1]*scale),round(cell.shape[0]*scale)),Image.Resampling.LANCZOS);b=np.array(im);yy,xx=np.where(b[:,:,3]>200);top=int(yy.min());hx=np.where(b[top:top+16,:,3]>128)[1]
    floorx=np.where(b[max(int(yy.max())-3,0):int(yy.max())+1,:,3]>128)[1]
    offset=(round(128-(floorx.min()+floorx.max())/2),224-ruler_floor);f=Image.new('RGBA',(256,256));f.alpha_composite(im,offset)
    dest=P/('diagnostic-frames'+suffix)/f'{i:03}.png';dest.parent.mkdir(exist_ok=True);f.save(dest);z=np.array(f);ys,xs=np.where(z[:,:,3]>200)
    neutral=z[142:175,108:149];rgb=neutral[:,:,:3].astype(float);lum=rgb.mean(2);mask=(neutral[:,:,3]>200)&(np.ptp(rgb,axis=2)<15)&(lum>20)&(lum<180)
    bodyx=np.where(z[100:140,:,3]>200)[1]
    row={'phase':i,'height':int(ys.max()-ys.min()+1),'width':int(xs.max()-xs.min()+1),'headRegionWidth':int(hx.max()-hx.min()+1),'upperBodyWidth':int(bodyx.max()-bodyx.min()+1),'bootY':int(ys.max()),'neutralUpperLegQuartiles':np.percentile(lum[mask],[25,50,75]).tolist(),'sourceBox':[lo,0,hi,a.shape[0]],'offset':offset};rows.append(row)
    board.paste(f,(i*256,22),f);d.text((i*256+5,4),f'new{i} H{row["height"]} head{row["headRegionWidth"]}',fill='white')
    old=Image.open(R/f'character/veld-cargo-turns-master-family-v1/north-east-candidate-v5/frames/bare/{i:03}.png').convert('RGBA');board.paste(old,(i*256,310),old);d.text((i*256+5,290),'older processed turn',fill='white')
board.paste(held,(1536,22),held);d.text((1540,4),'latest North held',fill='white');board.save(P/('source-master-comparison'+suffix+'.png'))
(P/('source-audit'+suffix+'.json')).write_text(json.dumps({'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'scale':scale,'standingRuler':148,'rows':rows,'postGenerationRGBChanged':False,'status':'diagnostic_not_selected; source fidelity/angles/held-stance joins require review'},indent=2)+'\n')
print(json.dumps({'scale':scale,'rows':rows}))
