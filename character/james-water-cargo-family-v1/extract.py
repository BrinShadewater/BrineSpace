"""Component-aware cells preserve disconnected floating cargo and cutting flames."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
def extract(d):
 p=P.parent/('james-water-cargo-'+d+'-v1');a=np.array(Image.open(p/'source.png').convert('RGBA'));labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
 ids=sorted(np.argsort(counts)[-18:],key=lambda k:np.where(labs==k)[0].mean());groups=[sorted(ids[i*6:i*6+6],key=lambda k:np.where(labs==k)[1].mean()) for i in range(3)]
 means=[[np.array(np.where(labs==k)).mean(1) for k in group] for group in groups];ys=[float(np.mean([v[0] for v in row])) for row in means]
 vertical=(a[:,:,3]>180).any(1);yb=[0]
 for row in range(2):
  midpoint=round((ys[row]+ys[row+1])/2);radius=round((ys[row+1]-ys[row])*.3);runs=[];start=None
  for y in range(max(0,midpoint-radius),min(a.shape[0],midpoint+radius)):
   if not vertical[y] and start is None:start=y
   if vertical[y] and start is not None:runs.append((start,y));start=None
  if start is not None:runs.append((start,min(a.shape[0],midpoint+radius)))
  if not runs:raise ValueError('No complete row gutter '+d+str(row))
  gap=max(runs,key=lambda q:q[1]-q[0]);yb.append(round(sum(gap)/2))
 yb.append(a.shape[0])
 records=[];board=Image.new('RGB',(1800,1350),'#303b40');dr=ImageDraw.Draw(board)
 for row in range(3):
  xs=[v[1] for v in means[row]];xb=[0]
  occupied=(a[yb[row]:yb[row+1],:,3]>180).any(0)
  for col in range(5):
   midpoint=round((xs[col]+xs[col+1])/2);radius=round((xs[col+1]-xs[col])*.25);lo=max(xb[-1]+1,midpoint-radius);hi=min(a.shape[1],midpoint+radius)
   intervals=[];run=None
   for x in range(lo,hi):
    if not occupied[x] and run is None:run=x
    if occupied[x] and run is not None:intervals.append((run,x));run=None
   if run is not None:intervals.append((run,hi))
   if not intervals:raise ValueError('No source gutter '+d+str(row)+str(col))
   gap=max(intervals,key=lambda q:q[1]-q[0]);xb.append(round(sum(gap)/2))
  xb.append(a.shape[1])
  for col in range(6):
   i=row*6+col;x0,x1=xb[col],xb[col+1];y0,y1=yb[row],yb[row+1];area=a[y0:y1,x0:x1];yy,xx=np.where(area[:,:,3]>180);box=[x0+int(xx.min())-3,y0+int(yy.min())-3,x0+int(xx.max())+4,y0+int(yy.max())+4]
   if box[0]<x0 or box[1]<y0 or box[2]>x1 or box[3]>y1:raise ValueError('Component reaches cell boundary '+d+str(i)+str(box))
   cut=a[box[1]:box[3],box[0]:box[2]].copy();core=cut[:,:,3]>180;owned=binary_dilation(core,iterations=2);cut[~owned]=0;cut[core,3]=255
   im=Image.fromarray(cut);dest=p/'source-crops'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);im.save(dest)
   cl,cn=label(np.array(im)[:,:,3]>180);ct=np.bincount(cl.ravel());records.append(dict(index=i,sourceBox=box,opaqueWidth=int(xx.max()-xx.min()+1),opaqueHeight=int(yy.max()-yy.min()+1),components=sorted([int(v) for v in ct[1:] if v>20],reverse=True)))
   sc=min(280/im.width,360/im.height);small=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.LANCZOS);at=(col*300+8,row*450+45);board.paste(small,at,small);dr.text((at[0],at[1]-28),d+' '+str(i)+' '+['salvage','pickup','carry'][row],fill='white')
 board.save(p/'source-contact.png');(p/'source-audit.json').write_text(json.dumps(dict(sourceSha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),method='18 primary body components define row/cell ownership; retain all deliberate foreground components inside cell, including floating case and flame; alpha>180 becomes opaque, two-pixel original-alpha edge retained, distant faint halo discarded',poses=records),indent=2)+'\n');print(d,'18 component-aware source cells',[(q['opaqueWidth'],q['opaqueHeight'],len(q['components'])) for q in records])
if __name__=='__main__':
 import sys
 for d in sys.argv[1:] or ['east','south','west','north']:extract(d)
