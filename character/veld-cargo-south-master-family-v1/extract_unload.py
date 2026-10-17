from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
raw=Image.open(P/'raw-unload-v4.png').convert('RGBA');a=np.array(raw);labels,n=label(a[:,:,3]>200);areas=np.bincount(labels.ravel());areas[0]=0;boxes=[]
for identity in np.argsort(areas)[-7:]:
 yy,xx=np.where(labels==identity);assert len(yy)>10000;boxes.append((int(xx.min()),int(xx.max())))
boxes.sort();bounds=[0]+[(boxes[i][1]+boxes[i+1][0])//2 for i in range(6)]+[raw.width]
cells=[a[:,bounds[i]:bounds[i+1]].copy() for i in range(7)]
for cell in cells:assert not np.any(cell[:,[0,-1],3]>20),'Whole-figure alpha gutters required'
yy,xx=np.where(cells[0][:,:,3]>200);scale=148/(yy.max()-yy.min()+1);rows=[];board=Image.new('RGB',(1792,600),'#202a30');draw=ImageDraw.Draw(board)
(P/'ungraded-unload').mkdir(exist_ok=True)
for i,cell in enumerate(cells):
 lab,n=label(cell[:,:,3]>200);areas=np.bincount(lab.ravel());areas[0]=0;mask=lab==int(areas.argmax());y,x=np.where(mask);floor=int(y.max());_,bx=np.where(mask[floor-7:floor+1]);center=(bx.min()+bx.max())/2
 clean=cell.copy();clean[~binary_dilation(mask,iterations=2)]=0;offset=(round(128-center*scale),round(224-floor*scale));frame=Image.new('RGBA',(256,256));frame.alpha_composite(Image.fromarray(clean).resize((round(cell.shape[1]*scale),round(cell.shape[0]*scale)),Image.Resampling.LANCZOS),offset);frame.save(P/f'ungraded-unload/{i:03}.png')
 fa=np.array(frame);rgb=fa[:,:,:3].astype(float);fy,fx=np.where(fa[:,:,3]>200);top=int(fy.min());warm=(fa[:,:,3]>128)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[:top]=False;warm[top+16:]=False;hy,hx=np.where(warm)
 rows.append({'phase':i,'sourceBootFloor':floor,'sourceBootCenter':float(center),'offset':offset,'nativeHeight':int(fy.max()-fy.min()+1),'headTop':top,'warmTop16Width':int(hx.max()-hx.min()+1),'gutterEdgeOpaque':int((cell[:,-1,3]>200).sum())})
 board.paste(frame,(i*256,25),frame);draw.text((i*256+3,4),'New source '+str(i),fill='white');old=Image.open(R/f'character/veld-unload-south-consistent-v1/frames/bare/{min(i,5):03}.png').convert('RGBA');board.paste(old,(i*256,325),old);draw.text((i*256+3,304),'Earlier source '+str(min(i,5)),fill='white')
board.save(P/'unload-source-comparison.png');(P/'extraction.json').write_text(json.dumps({'scale':scale,'gutters':bounds,'rows':rows,'sourceSHA256':hashlib.sha256((P/'raw-unload-v4.png').read_bytes()).hexdigest(),'ruler':'One firststanding148 source ruler, whole-body boot-center/ground registration; no per-pose scaling'},indent=2)+'\n',encoding='utf-8');print(json.dumps({'scale':scale,'rows':rows}))
