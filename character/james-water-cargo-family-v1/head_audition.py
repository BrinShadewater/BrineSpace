from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
P=Path(__file__).resolve().parent
for d in ['east','south','west','north']:
 p=P.parent/('james-water-cargo-'+d+'-v1');points=[];board=Image.new('RGB',(1536,3*280),'#303b40');draw=ImageDraw.Draw(board)
 for i in range(18):
  im=Image.open(p/'source-crops'/f'{i:03d}.png').convert('RGBA');a=np.array(im);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
  skin=(a[:,:,3]>180)&(r-g>10)&(g-b>7)&(r-b>24)&((r-g)/np.maximum(1,r-b)>.42)
  labs,n=label(skin);counts=np.bincount(labs.ravel());counts[0]=0;yy,xx=np.where(labs==counts.argmax());assert len(xx)>30
  face=np.array([xx.mean(),yy.mean()]);point=face+np.array({'east':[-5,-8],'west':[5,-8],'south':[0,-10],'north':[0,0]}[d]);points.append(point.tolist())
  x0,y0=np.rint(point-[55,55]).astype(int);crop=im.crop((x0,y0,x0+110,y0+110)).resize((220,220),Image.Resampling.NEAREST);at=(i%6*256+12,i//6*280+40);board.paste(crop,at,crop);draw.line((at[0]+110,at[1],at[0]+110,at[1]+220),fill='#a0cfff');draw.line((at[0],at[1]+110,at[0]+220,at[1]+110),fill='#a0cfff');draw.text((at[0],at[1]-25),d+' '+str(i)+' '+str(np.rint(point).astype(int).tolist()),fill='white')
 (p/'head-candidates.json').write_text(json.dumps(dict(method='Warm cranial/face component centroid plus direction-specific cranial offset; candidate proxy requiring visual review, not measured shoulder',heads=points),indent=2)+'\n');board.save(p/'head-audition.png')
print('Four cranial-proxy audits; all18 source poses/facing')
