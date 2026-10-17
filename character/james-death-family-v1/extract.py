from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
def extract(d):
 p=P.parent/('james-death-'+d+'-v1');a=np.array(Image.open(p/'source.png').convert('RGBA'));labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
 ids=sorted(np.argsort(counts)[-12:],key=lambda k:np.where(labs==k)[0].mean());order=[]
 for row in range(2):order+=sorted(ids[row*6:row*6+6],key=lambda k:np.where(labs==k)[1].mean())
 records=[];heads=[];board=Image.new('RGB',(1536,440),'#303b40');draw=ImageDraw.Draw(board)
 for i,k in enumerate(order):
  yy,xx=np.where(labs==k);raw=[int(xx.min())-3,int(yy.min())-3,int(xx.max())+4,int(yy.max())+4];box=[max(0,raw[0]),max(0,raw[1]),min(a.shape[1],raw[2]),min(a.shape[0],raw[3])];x0,y0,x1,y1=box
  cell=a[y0:y1,x0:x1].copy();cell[~binary_dilation(labs[y0:y1,x0:x1]==k,iterations=2)]=0;im=Image.fromarray(cell);dest=p/'source-crops'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);im.save(dest)
  records.append(dict(index=i,sourceBox=box,clipped=box!=raw,width=im.width,height=im.height))
  r,g,b=cell[:,:,:3].astype(float).transpose(2,0,1);warm=(cell[:,:,3]>180)&(r-g>10)&(g-b>7)&(r-b>24)&((r-g)/np.maximum(1,r-b)>.42);ls,ns=label(warm);cs=np.bincount(ls.ravel());cs[0]=0;hy,hx=np.where(ls==cs.argmax())
  offset=np.array({'east':[-5,-8],'west':[5,-8],'south':[0,-10],'north':[0,0]}[d]);point=np.array([hx.mean(),hy.mean()])+offset;heads.append(point.tolist())
  zoom=im.crop((*np.rint(point-[40,40]).astype(int),*np.rint(point+[40,40]).astype(int))).resize((160,160),Image.Resampling.NEAREST);pos=(i%6*256+8,i//6*220+44);board.paste(zoom,pos,zoom);draw.line((pos[0]+80,pos[1],pos[0]+80,pos[1]+160),fill='cyan');draw.line((pos[0],pos[1]+80,pos[0]+160,pos[1]+80),fill='cyan');draw.text((pos[0],pos[1]-25),str(i)+' '+str(np.rint(point).astype(int).tolist()),fill='white')
 (p/'source-audit.json').write_text(json.dumps(dict(sourceSha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),poses=records),indent=2)+'\n');(p/'head-candidates.json').write_text(json.dumps(dict(method='Warm-component proxy requiring visual review; rear manual crown correction required',heads=heads),indent=2)+'\n');board.save(p/'head-audition.png')
 print(d,[(q['width'],q['height'],q['clipped']) for q in records],np.rint(heads).astype(int).tolist())
if __name__=='__main__':
 import sys
 for d in sys.argv[1:] or ['east','south','west','north']:extract(d)

