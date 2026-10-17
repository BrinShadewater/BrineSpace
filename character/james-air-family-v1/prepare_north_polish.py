from pathlib import Path
import json,shutil,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;p=P.parent/'james-air-north-v1'
record=json.loads((p/'recover-v3-origin.json').read_text())
source=p/'recover-source-v3.png'
if not source.exists():shutil.copy2(record['original'],source)
assert source.read_bytes()==Path(record['original']).read_bytes()
(p/'recover-source-v3-prompt.txt').write_text(record['prompt'],encoding='utf-8')
a=np.array(Image.open(source).convert('RGBA'));ls,n=label(a[:,:,3]>180);counts=np.bincount(ls.ravel());counts[0]=0
ids=sorted(np.argsort(counts)[-6:],key=lambda k:np.where(ls==k)[1].mean());records=[];heads=[]
board=Image.new('RGB',(1536,300),'#303b40');draw=ImageDraw.Draw(board)
for j,k in enumerate(ids):
    yy,xx=np.where(ls==k);raw=[int(xx.min())-3,int(yy.min())-3,int(xx.max())+4,int(yy.max())+4];box=[max(0,raw[0]),max(0,raw[1]),min(a.shape[1],raw[2]),min(a.shape[0],raw[3])];x0,y0,x1,y1=box
    cell=a[y0:y1,x0:x1].copy();cell[~binary_dilation(ls[y0:y1,x0:x1]==k,iterations=2)]=0;im=Image.fromarray(cell)
    dest=p/'recovery-crops-v3'/f'{j+6:03d}.png';dest.parent.mkdir(exist_ok=True);im.save(dest)
    rr,gg,bb=cell[:,:,:3].astype(float).transpose(2,0,1);gridy=np.indices(rr.shape)[0]
    warm=(cell[:,:,3]>180)&(gridy<im.height*.14)&(rr-gg>2)&(gg-bb>1)&(rr-bb>6)
    labs,nn=label(warm);cs=np.bincount(labs.ravel());cs[0]=0;hy,hx=np.where(labs==cs.argmax());point=np.array([hx.mean(),hy.mean()]);heads.append(point.tolist())
    records.append(dict(index=j+6,sourceBox=box,width=im.width,height=im.height,clipped=raw!=box,hairBounds=[int(hx.min()),int(hy.min()),int(hx.max()+1),int(hy.max()+1)]))
    zoom=im.crop((*np.rint(point-[80,80]).astype(int),*np.rint(point+[80,80]).astype(int))).resize((210,210),Image.Resampling.NEAREST);at=(j*256+8,50);board.paste(zoom,at,zoom);draw.line((at[0]+105,at[1],at[0]+105,at[1]+210),fill='cyan');draw.line((at[0],at[1]+105,at[0]+210,at[1]+105),fill='cyan');draw.text((at[0],10),str(j+6)+' '+str(np.rint(point).astype(int).tolist()),fill='white')
(p/'recovery-v3-audit.json').write_text(json.dumps(dict(sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),poses=records,heads=heads,method='Warm upper cranium proxy; visual review required'),indent=2)+'\n');board.save(p/'recovery-v3-head-audition.png')
print([(r['width'],r['height'],r['hairBounds'],r['clipped']) for r in records],np.rint(heads).astype(int).tolist())
