"""Extract independently authored bodies and helmet heads, preserving source pixels."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation
P=Path(__file__).resolve().parent
PAIRS=['east-south','south-west','west-north','north-east']
def extract(p):
 a=np.array(Image.open(p/'source.png').convert('RGBA')); labs,n=label(a[:,:,3]>180)
 counts=np.bincount(labs.ravel()); counts[0]=0
 ids=sorted(np.argsort(counts)[-12:],key=lambda k:np.where(labs==k)[0].mean())
 ordered=[]
 for row in range(2):
  ordered+=sorted(ids[row*6:row*6+6],key=lambda k:np.where(labs==k)[1].mean())
 records=[]; board=Image.new('RGB',(1800,900),'#303b40'); d=ImageDraw.Draw(board)
 for i,k in enumerate(ordered):
  yy,xx=np.where(labs==k); raw=[int(xx.min())-3,int(yy.min())-3,int(xx.max())+4,int(yy.max())+4]
  box=[max(0,raw[0]),max(0,raw[1]),min(a.shape[1],raw[2]),min(a.shape[0],raw[3])]
  x0,y0,x1,y1=box; cell=a[y0:y1,x0:x1].copy(); cell[~binary_dilation(labs[y0:y1,x0:x1]==k,iterations=2)]=0
  clipped=raw!=box
  if clipped and i%6 not in [0,5]:raise ValueError('Required interior clipped: '+str(i))
  im=Image.fromarray(cell); dest=p/'source-crops'/f'{i:03d}.png'; dest.parent.mkdir(exist_ok=True); im.save(dest)
  records.append(dict(index=i,kind='body' if i<6 else 'helmet',sourceBox=box,clipped=clipped,opaqueWidth=int(xx.max()-xx.min()+1),opaqueHeight=int(yy.max()-yy.min()+1)))
  sc=min(280/im.width,360/im.height); small=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.LANCZOS)
  at=(i%6*300+8,i//6*450+48); board.paste(small,at,small); d.text((at[0],at[1]-30),str(i)+' '+records[-1]['kind'],fill='white')
 board.save(p/'source-contact.png'); (p/'source-audit.json').write_text(json.dumps(dict(sourceSha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),poses=records),indent=2)+'\n')
 print(p.name,[(q['opaqueWidth'],q['opaqueHeight'],q['clipped']) for q in records])
if __name__=='__main__':
 import sys
 for pair in sys.argv[1:] or PAIRS:extract(P.parent/('james-water-turn-'+pair+'-v1'))
