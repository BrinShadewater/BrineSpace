from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parents[1];raw=P/'raw-unload-v4.png';a=np.array(Image.open(raw).convert('RGBA'));labels,n=ndimage.label(a[:,:,3]>200);counts=np.bincount(labels.ravel());counts[0]=0;big=sorted(np.argsort(counts)[-6:],key=lambda k:np.where(labels==k)[1].mean());centers=[np.where(labels==k)[1].mean() for k in big]
groups=[[] for _ in big];keep=np.zeros(labels.shape,bool)
for k in range(1,n+1):
 if counts[k]<500:continue
 y,x=np.where(labels==k);i=int(np.argmin(np.abs(np.array(centers)-x.mean())));groups[i].append([int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]);keep|=labels==k
# Complete figure AND any separate deposited case retained. Only tiny detached source speckles removed from alpha.
a[~ndimage.binary_dilation(keep,iterations=3)]=0
boxes=[[min(b[0] for b in g),min(b[1] for b in g),max(b[2] for b in g),max(b[3] for b in g)] for g in groups];first_hi=round((boxes[0][2]+boxes[1][0])/2);first=Image.fromarray(a[:,:first_hi]);initial=round(a.shape[0]*148/(boxes[0][3]-boxes[0][1]))
for adjust in [0,1,-1,2,-2,3,-3]:
 height=initial+adjust;scale=height/a.shape[0];z=np.array(first.resize((round(first.width*scale),height),Image.Resampling.LANCZOS));y,x=np.where(z[:,:,3]>200)
 if int(y.max()-y.min()+1)==148:break
else:raise AssertionError('No common148 standing ruler')
near=[(40,175),(370,518),(720,885),(1090,1260),(1460,1618),(1840,1980)];far=[(175,240),(518,583),(885,945),(1263,1330),(1620,1680),(1980,2036)]
master=np.array(Image.open(R/'character/veld-east-held-original-master-v1/frames/bare/000.png').convert('RGBA'));my,mx=np.where(master[216:225,90:137,3]>200);target_x=float((mx[my>=my.max()-1]+90).mean());target_y=int(my.max()+216)
rows=[];common_y=None;board=Image.new('RGB',(1792,310),'#202a30');d=ImageDraw.Draw(board)
for i in range(6):
 lo=0 if i==0 else round((boxes[i-1][2]+boxes[i][0])/2);hi=a.shape[1] if i==5 else round((boxes[i][2]+boxes[i+1][0])/2);im=Image.fromarray(a[:,lo:hi]).resize((round((hi-lo)*scale),height),Image.Resampling.LANCZOS);z=np.array(im);xscale=im.width/(hi-lo)
 def contact(bounds):
  left,right=bounds;xl=round((left-lo)*xscale);xr=round((right-lo)*xscale);yt=round(640*scale);yb=min(height,round(674*scale));yy,xx=np.where(z[yt:yb,xl:xr,3]>200);bottom=int(yy.max()+yt);sel=yy>=yy.max()-1;return float((xx[sel]+xl).mean()),bottom,int((xx[sel]+xl).max())
 nx,ny,nr=contact(near[i]);fx,fy,fr=contact(far[i]);dx=round(target_x-nx)
 if common_y is None:common_y=target_y-ny
 out=Image.new('RGBA',(256,256));out.alpha_composite(im,(dx,common_y));dest=P/'atlas-contact-frames'/f'{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);ys,xs=np.where(np.array(out)[:,:,3]>200);head=np.where(np.array(out)[int(ys.min()):int(ys.min())+16,:,3]>128)[1]
 rows.append({'pose':i,'heightIncludingCase':int(ys.max()-ys.min()+1),'headWidth':int(head.max()-head.min()+1),'sourceCell':[lo,0,hi,a.shape[0]],'offset':[dx,common_y],'nearContact':[nx+dx,ny+common_y],'farVisibleContact':[fx+dx,fy+common_y],'farToeRight':fr+dx,'sourceScaleX':xscale,'sourceContactWindows':{'near':near[i],'far':far[i]}});board.paste(out,(i*256,25),out);d.text((i*256+4,4),'whole registered '+str(i),fill='white')
master_im=Image.open(R/'character/veld-east-held-original-master-v1/frames/bare/000.png').convert('RGBA');board.paste(master_im,(1536,25),master_im);d.text((1540,4),'exact held master',fill='white');board.save(P/'atlas-contact-master-review.png')
report={'rawSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sourceScale':scale,'commonYOffset':common_y,'originalHeldNearContactTarget':[target_x,target_y],'rows':rows,'nearContactXResidualMax':max(abs(r['nearContact'][0]-target_x) for r in rows),'nearYDrift':max(r['nearContact'][1] for r in rows)-min(r['nearContact'][1] for r in rows),'visibleFarToeXSpan':max(r['farToeRight'] for r in rows)-min(r['farToeRight'] for r in rows),'scope':'Complete column registration to foreground boot, one atlas scale/sharedY. No body/limb/RGB edits. Separate far visible contacts measured, not forced. Source/world foot fidelity and floor case drift remain separate.'};(P/'contact-registration.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
