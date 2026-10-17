from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
def extract(path,count=18,columns=6):
 a=np.array(Image.open(path).convert('RGBA'));labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;ids=sorted(np.argsort(counts)[-count:],key=lambda k:np.where(labs==k)[0].mean());out=[]
 for row in range((count+columns-1)//columns):
  for k in sorted(ids[row*columns:row*columns+columns],key=lambda k:np.where(labs==k)[1].mean()):
   y,x=np.where(labs==k);box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4];x0,y0,x1,y1=box
   if min(x0,y0)<0 or x1>a.shape[1] or y1>a.shape[0]:raise ValueError('Source body clipped: '+str(box))
   cell=a[y0:y1,x0:x1].copy();cell[~binary_dilation(labs[y0:y1,x0:x1]==k,iterations=2)]=0;out.append((Image.fromarray(cell),box))
 return out
if __name__=='__main__':
 import sys
 for d in sys.argv[1:] or ['east','south','west','north']:
  p=P.parent/('james-water-'+d+'-v1');cells=extract(p/'source.png');records=[];board=Image.new('RGB',(1536,936),'#303b40');draw=ImageDraw.Draw(board)
  for i,(im,box) in enumerate(cells):
   dest=p/'source-crops'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);im.save(dest);a=np.array(im);y,x=np.where(a[:,:,3]>180);records.append(dict(index=i,sourceBox=box,opaqueWidth=int(x.max()-x.min()+1),opaqueHeight=int(y.max()-y.min()+1)))
   # A review thumbnail only: packaging later uses one anatomical scale, not this fit.
   sc=min(236/im.width,270/im.height);small=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.LANCZOS);at=(i%6*256+10,i//6*312+35);board.paste(small,at,small);draw.text((at[0],at[1]-25),d+' raw '+str(i),fill='white')
  (p/'source-audit.json').write_text(json.dumps(dict(sourceSha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),poses=records),indent=2)+'\n');board.save(p/'source-contact.png');print(d,'18 complete source bodies',[(q['opaqueWidth'],q['opaqueHeight']) for q in records])
