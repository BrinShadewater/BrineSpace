from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'full-gait-review-v280';j=json.loads((p/'material-repair-progress.json').read_bytes())
def source(i,mode='bare'):
 manifest=json.loads((o/f'{mode}-manifest.json').read_bytes())
 return Image.open(r/manifest['states'][0]['frameFiles'][i].removeprefix('res://')).convert('RGBA')
master=Image.open(p/'../james-west-master-carry-v1/registered-original-master.png').convert('RGBA')
indices=[47,48,0,1,2,3,4]
board=Image.new('RGBA',(256*8,560),(47,58,63,255));draw=ImageDraw.Draw(board)
for row,mode in enumerate(['bare','helmet']):
 board.alpha_composite(master,(0,row*280+24));draw.text((4,row*280+4),'Bare standing master',fill='white')
 for col,i in enumerate(indices,1):board.alpha_composite(source(i,mode),(256*col,row*280+24));draw.text((256*col+4,row*280+4),f'{mode} phase{i}',fill='white')
board.save(o/'seam-master-review.png')
board=Image.new('RGBA',(7*192,7*212),(47,58,63,255));draw=ImageDraw.Draw(board)
for i in range(49):
 x=(i%7)*192;y=(i//7)*212;board.alpha_composite(source(i).crop((80,160,176,256)).resize((192,192),Image.Resampling.NEAREST),(x,y+20));draw.text((x+4,y+4),f'phase{i}',fill='white')
board.save(o/'all-lower-review.png')
rows=[]
for i in range(49):
 a=np.asarray(source(i));mask=a[181:236,:,3]>=250;luma=a[181:236,:,:3]@np.array([.2126,.7152,.0722]);rows.append(dict(phase=i,opaqueCount=int(mask.sum()),median=float(np.percentile(luma[mask],50)),p95=float(np.percentile(luma[mask],95))))
(o/'lower-tone-diagnostics.json').write_text(json.dumps(dict(rows=rows,scope='Pose-dependent visible lower-body masks; comparisons do not isolate equal anatomical/material samples or certify flash-free motion.'),indent=2)+'\n',encoding='utf-8')
print('Seam/master board and all49 lower crops prepared.')
