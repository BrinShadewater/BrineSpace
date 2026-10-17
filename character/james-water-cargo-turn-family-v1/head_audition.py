from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
P=Path(__file__).resolve().parent
OFFSETS={'east':[-5,-8],'south':[0,-10],'west':[5,-8],'north':[0,0]}
for pair in ['east-south','south-west','west-north','north-east']:
 p=P.parent/('james-water-cargo-turn-'+pair+'-v1');a,b=pair.split('-');points=[];rulers=[];board=Image.new('RGB',(1536,360),'#303b40');draw=ImageDraw.Draw(board)
 for i in range(6):
  im=Image.open(p/'source-crops'/f'{i:03d}.png').convert('RGBA');arr=np.array(im);r,g,bb=arr[:,:,:3].astype(float).transpose(2,0,1)
  skin=(arr[:,:,3]>180)&(r-g>10)&(g-bb>7)&(r-bb>24)&((r-g)/np.maximum(1,r-bb)>.42)
  labs,n=label(skin);counts=np.bincount(labs.ravel());counts[0]=0;yy,xx=np.where(labs==counts.argmax());assert len(xx)>30
  point=np.array([xx.mean(),yy.mean()])+np.array(OFFSETS[a])*(1-i/5)+np.array(OFFSETS[b])*i/5;points.append(point.tolist());rulers.append(dict(warmComponentBounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]))
  crop=im.crop((*np.rint(point-[55,55]).astype(int),*np.rint(point+[55,55]).astype(int))).resize((220,220),Image.Resampling.NEAREST);at=(i*256+12,90);board.paste(crop,at,crop);draw.line((at[0]+110,at[1],at[0]+110,at[1]+220),fill='#9cc8d1');draw.line((at[0],at[1]+110,at[0]+220,at[1]+110),fill='#9cc8d1');draw.text((at[0],12),pair+' '+str(i),fill='white');draw.text((at[0],36),str(np.rint(point).astype(int).tolist()),fill='white');draw.text((at[0],58),str(rulers[-1]['warmComponentBounds']),fill='white')
 (p/'head-candidates.json').write_text(json.dumps(dict(method='Warm face/rear-cranium component with interpolated cranial offset; candidate proxy requiring visual review, not measured shoulder',heads=points,rulers=rulers),indent=2)+'\n');board.save(p/'head-audition.png')
 print(pair,'candidate heads',np.rint(points).astype(int).tolist())
