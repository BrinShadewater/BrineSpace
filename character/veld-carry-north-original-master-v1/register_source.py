from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parents[1]
raw=P/'raw-gait-v3.png';a=np.array(Image.open(raw).convert('RGBA'))
labels,count=ndimage.label(a[:,:,3]>200)
cells=[]
for k in range(1,count+1):
    yy,xx=np.where(labels==k)
    if len(xx)>10000:cells.append((int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1),k))
cells.sort();assert len(cells)==6,len(cells)
firstheight=cells[0][3]-cells[0][1]
master=Image.open(R/'character/veld-idle-north-original-master-v1/clean-idle-master.png').convert('RGBA')
# A single atlas standing ruler; never enlarge a squat into a standing figure.
candidate=[]
first=a[:,:(cells[0][2]+cells[1][0])//2].copy()
fl,_=ndimage.label(first[:,:,3]>200);fs=np.bincount(fl.ravel());fs[0]=0
first[~ndimage.binary_dilation(fl==int(fs.argmax()),iterations=3)]=0
for adjust in [0,1,-1,2,-2,3,-3]:
    resizeheight=round(a.shape[0]*148/firstheight)+adjust
    scale=resizeheight/a.shape[0]
    resized=Image.fromarray(first).resize((round(first.shape[1]*scale),resizeheight),Image.Resampling.LANCZOS)
    fy,fx=np.where(np.array(resized)[:,:,3]>200)
    if fy.max()-fy.min()+1==148:candidate.append(scale)
assert candidate,'No common first-pose ruler produces148'
scale=candidate[0];rows=[];bindings={};board=Image.new('RGB',(7*256,310),'#202a30');draw=ImageDraw.Draw(board)
board.paste(master,(6*256,25),master);draw.text((6*256+6,5),'prepared original rest',fill='white')
for i,(x0,y0,x1,y1,k) in enumerate(cells):
    # Broad gutters include complete alpha fringes; retain whole component only.
    lo=0 if i==0 else (cells[i-1][2]+x0)//2
    hi=a.shape[1] if i==5 else (x1+cells[i+1][0])//2
    cell=a[:,lo:hi].copy();celllabels,_=ndimage.label(cell[:,:,3]>200)
    sizes=np.bincount(celllabels.ravel());sizes[0]=0;main=int(sizes.argmax())
    keep=ndimage.binary_dilation(celllabels==main,iterations=3);cell[~keep]=0
    im=Image.fromarray(cell).resize((round(cell.shape[1]*scale),round(cell.shape[0]*scale)),Image.Resampling.LANCZOS)
    aa=np.array(im);yy,xx=np.where(aa[:,:,3]>200);top=int(yy.min());bottom=int(yy.max())
    hx=np.where(aa[top:top+16,:,3]>128)[1];axis=(hx.min()+hx.max())/2
    offset=(round(128-axis),224-round((max(c[3] for c in cells)-1)*scale));frame=Image.new('RGBA',(256,256));frame.alpha_composite(im,offset)
    dest=P/'diagnostic-frames'/f'{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);frame.save(dest)
    native=np.array(frame);ys,xs=np.where(native[:,:,3]>200)
    head=np.where(native[int(ys.min()):int(ys.min())+16,:,3]>128)[1]
    lower=np.where(native[170:225,:,3]>200)[1]
    rows.append({'pose':i,'height':int(ys.max()-ys.min()+1),'width':int(xs.max()-xs.min()+1),'headRegionWidth':int(head.max()-head.min()+1),'lowerBodyWidth':int(lower.max()-lower.min()+1),'offset':offset,'sourceBox':[lo,0,hi,a.shape[0]]})
    assert 222<=ys.max()<=225
    board.paste(frame,(i*256,25),frame);draw.text((i*256+6,5),'whole source '+str(i),fill='white')
    bindings[dest.relative_to(R).as_posix()]=hashlib.sha256(dest.read_bytes()).hexdigest()
board.save(P/'source-master-comparison.png')
(P/'source-registration.json').write_text(json.dumps({'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sourceScale':scale,'standingRuler':148,'rows':rows,'bindings':bindings,'status':'diagnostic_pending_review','postGenerationColourChanged':False},indent=2)+'\n')
print(json.dumps({'scale':scale,'rows':rows}))
