"""Extract four independent authored poses without changing anatomy."""
from pathlib import Path
import json,sys
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent
source=H/(sys.argv[1] if len(sys.argv)>1 else 'body-source-v1.png')
a=np.array(Image.open(source).convert('RGBA'));l,n=label(a[:,:,3]>160);z=np.bincount(l.ravel());ids=sorted(range(1,n+1),key=lambda k:z[k],reverse=True)[:4]
assert len(ids)==4
ids.sort(key=lambda k:(int(np.where(l==k)[0].mean()//(a.shape[0]/2)),np.where(l==k)[1].mean()))
records=[];board=Image.new('RGBA',(1400,1400),'#202a30');draw=ImageDraw.Draw(board)
for i,k in enumerate(ids):
 y,x=np.where(l==k);b=[int(x.min())-2,int(y.min())-2,int(x.max())+3,int(y.max())+3];assert min(b[:2])>=0 and b[2]<=a.shape[1] and b[3]<=a.shape[0]
 cut=a.copy();cut[~binary_dilation(l==k,iterations=2)]=0;im=Image.fromarray(cut).crop(b);(H/'source-crops').mkdir(exist_ok=True);im.save(H/f'source-crops/{i:03}.png');records.append(dict(slot=i+1,sourceBox=b,sourceFile=source.name))
 board.alpha_composite(im,(i%2*700,i//2*700+30));draw.text((i%2*700,i//2*700),f'cell{i} crop{im.size}',fill='white')
(H/'crop-records.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8');board.save(H/'source-crop-board-v1.png')
print('Four full-body crops retained; semantic head landmarks require visual selection.')
