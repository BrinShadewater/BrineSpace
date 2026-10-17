from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
board=Image.new('RGB',(1536,768),(34,52,62));draw=ImageDraw.Draw(board);results=[]
for row,version in enumerate(['current','bare-v6','bare-v7']):
 raw=np.array(Image.open(P/f'sources/{version}.png')) if version!='current' else None
 ruler=None;records=[]
 for i in range(4):
  if raw is None:im=Image.open(P/f'frames/bare/carry-turn-east-south/{i+1:03}.png')
  else:
   a=raw[:,i*384:(i+1)*384].copy();labs,_=label(a[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0;body=labs==n.argmax();y,x=np.where(body);height=int(y.max()-y.min()+1)
   if ruler is None:ruler=148/height
   mask=binary_dilation(body,iterations=1)&(a[:,:,3]>80);a[~mask]=0;y,x=np.where(mask);box=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));piece=Image.fromarray(a).crop(box);piece=piece.resize((round(piece.width*ruler),round(piece.height*ruler)),Image.Resampling.LANCZOS)
   pa=np.array(piece);py,px=np.where(pa[:,:,3]>180);axis=(px.min()+px.max())/2;im=Image.new('RGBA',(256,256));im.alpha_composite(piece,(round(128-axis),224-int(py.max())))
   records.append({'phase':i+1,'sourceHeight':height,'fixedSheetScale':ruler,'nativeHeight':height*ruler})
  a=np.array(im);widths={}
  for name,y0,y1 in [('shoulder',102,126),('waist_and_case',126,162)]:
   y,x=np.where(a[y0:y1,:,3]>180);widths[name]=int(x.max()-x.min()+1)
  if raw is None:records.append({'phase':i+1})
  records[-1].update(widths);board.paste(im,(i*384,row*256),im);draw.text((i*384+6,row*256+8),version+' '+str(widths),fill='white')
 results.append({'source':version,'frames':records})
board.save(P/'build-source-comparison.png');(P/'build-source-comparison.json').write_text(json.dumps({'scope':'Diagnostic independent fixed per-sheet ruler;not adopted or visual acceptance;axis centers whole silhouette here,unlike final foot fitting','sources':results},indent=2)+'\n');print(json.dumps(results))
