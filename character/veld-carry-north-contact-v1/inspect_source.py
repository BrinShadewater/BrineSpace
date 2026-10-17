from pathlib import Path
import json, hashlib,sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent; R=P.parents[1]
version=int(sys.argv[1]) if len(sys.argv)>1 else 1
count=12 if version==1 else 2
suffix='' if version==1 else f'-v{version}'
raw=P/f'raw-contact-v{version}.png'; a=np.array(Image.open(raw).convert('RGBA'))
lab,n=ndimage.label(a[:,:,3]>200); cells=[]
for k in range(1,n+1):
    yy,xx=np.where(lab==k)
    if len(xx)>10000: cells.append((int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1),k))
assert len(cells)==count, f'Expected {count} whole source figures, found {len(cells)}'
cells=sorted(cells,key=lambda c:c[1])
cells=sorted(cells[:6],key=lambda c:c[0])+sorted(cells[6:],key=lambda c:c[0])
head_widths=[]
for x0,y0,x1,y1,k in cells:
    width=np.where((lab==k)[y0:y0+round((y1-y0)*16/148)])[1]
    head_widths.append(int(width.max()-width.min()+1))
# One common head ruler; moving silhouette heights are measured, not forced148.
scale=22/float(np.median(head_widths)); rows=[]
board=Image.new('RGB',(7*256,2*285),'#202a30'); d=ImageDraw.Draw(board)
master=Image.open(R/'character/veld-idle-north-original-master-v1/clean-idle-master.png').convert('RGBA')
for rr in range(2): board.paste(master,(1536,rr*285+20),master);d.text((1540,rr*285+4),'original standing ruler',fill='white')
for i,(x0,y0,x1,y1,k) in enumerate(cells):
    pad=8; lo=max(0,x0-pad);hi=min(a.shape[1],x1+pad);up=max(0,y0-pad);down=min(a.shape[0],y1+pad)
    cell=a[up:down,lo:hi].copy(); keep=ndimage.binary_dilation((lab==k)[up:down,lo:hi],iterations=3);cell[~keep]=0
    im=Image.fromarray(cell).resize((round(cell.shape[1]*scale),round(cell.shape[0]*scale)),Image.Resampling.LANCZOS)
    b=np.array(im);yy,xx=np.where(b[:,:,3]>200);top=int(yy.min());hx=np.where(b[top:top+16,:,3]>128)[1]
    offset=(round(128-(hx.min()+hx.max())/2),77-top)
    f=Image.new('RGBA',(256,256)); f.alpha_composite(im,offset)
    dest=P/('diagnostic-frames'+suffix)/f'{i:03}.png';dest.parent.mkdir(exist_ok=True);f.save(dest)
    z=np.array(f);ys,xs=np.where(z[:,:,3]>200); toe={}
    for side,(l,r) in {'left':(95,128),'right':(128,166)}.items():
        by,bx=np.where(z[180:251,l:r,3]>200);toe[side]=int(180+by.max()) if len(by) else None
    widths={}
    for part,(t,bottom) in {'upperBody':(100,140),'hips':(140,160)}.items():
        px=np.where(z[t:bottom,:,3]>200)[1];widths[part]=int(px.max()-px.min()+1)
    neutral=z[142:175,108:149];rgb=neutral[:,:,:3].astype(float);luma=rgb.mean(axis=2);mask=(neutral[:,:,3]>200)&(np.ptp(rgb,axis=2)<15)&(luma>20)&(luma<180)
    quartiles=np.percentile(luma[mask],[25,50,75]).tolist() if mask.any() else []
    rows.append({'phase':i,'height':int(ys.max()-ys.min()+1),'width':int(xs.max()-xs.min()+1),'headRegionWidth':int(hx.max()-hx.min()+1),'partWidths':widths,'neutralUpperLegQuartiles':quartiles,'toeProxyY':toe,'sourceBox':[lo,up,hi,down],'offset':offset})
    col=i%6;rr=i//6;board.paste(f,(col*256,rr*285+20),f);d.text((col*256+5,rr*285+3),f'phase{i} toes{toe}',fill='white')
board.save(P/('source-master-comparison'+suffix+'.png'))
(P/('source-audit'+suffix+'.json')).write_text(json.dumps({'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'scale':scale,'registration':'one head ruler and skull registration; no per-pose limb edits or RGB changes','rows':rows,'status':'candidate_not_selected; ground contact and source fidelity require review'},indent=2)+'\n')
print(json.dumps({'scale':scale,'rows':rows}))
