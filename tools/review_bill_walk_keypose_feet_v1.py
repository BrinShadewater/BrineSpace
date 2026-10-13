"""Keep Y-depth and horizontal support diagnostics distinct from planted-foot acceptance."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1/keypose-review-v1';board=Image.new('RGB',(1620,450),'#17252d');draw=ImageDraw.Draw(board);records=[]
for col,slot in enumerate([0,12,24,36]):
 pair=[]
 for row,(label,path) in enumerate([('Selected',R/f'character/bill-walk-east-material-v1/frames/bare/walk-east/{slot:03}.png'),('New',P/f'frames/{slot:03}.png')]):
  im=Image.open(path).convert('RGBA');a=np.asarray(im)[:,:,3]>127;y,x=np.where(a);bottom=y.max();xs=np.where(a[bottom])[0];band=np.where(a[max(0,bottom-3):bottom+1])[1]
  pair.append(dict(label=label,soleEdge=int(bottom+1),lowestRowXMean=float(xs.mean()),lowestRowXRange=[int(xs.min()),int(xs.max()+1)],bottom4RowsXRange=[int(band.min()),int(band.max()+1)]))
  view=im.crop((60,170,195,232)).resize((405,186),Image.Resampling.NEAREST);board.paste(view,(col*405,row*225+30),view);draw.text((col*405+8,row*225+10),f'{label} {slot} - fixed source crop',fill='white');draw.line((col*405,row*225+30+(224-170)*3,col*405+404,row*225+30+(224-170)*3),fill='#819b98')
 records.append(dict(slot=slot,measurements=pair,soleYDelta=pair[1]['soleEdge']-pair[0]['soleEdge'],lowestRowXMeanDelta=pair[1]['lowestRowXMean']-pair[0]['lowestRowXMean']))
board.save(P/'foot-comparison.png');(P/'foot-diagnostics.json').write_text(json.dumps(dict(scope='Opaque>127 source raster diagnostics. Lowest-row centroid is not a physical support point and may change with sole shape/rasterization. Fixed contact guide224; phase24 retains original sole223. Does not certify2Dplanted feet or native movement.',records=records),indent=2)+'\n',encoding='utf-8');print(json.dumps(records))
