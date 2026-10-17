from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'material-quarter-review-v54';out.mkdir(exist_ok=True)
sources=[(0,p/'master-material-v49'),(12,p/'master-material-phase12-v51'),(24,p/'master-material-phase24-v52'),(36,p/'master-material-phase36-v53')]
board=Image.new('RGBA',(1280,560),(47,58,63,255));draw=ImageDraw.Draw(board);records=[]
for row,mode in enumerate(['bare','helmet']):
    for col,(phase,folder) in enumerate(sources):
        f=folder/(mode+'-head-protected.png');before=p/'master-head-review-v16'/(mode+'-%03d.png'%phase)
        im=Image.open(f).convert('RGBA');a=np.asarray(im);b=np.asarray(Image.open(before).convert('RGBA'))
        mask=a[110:,:,3]>=128;old=b[110:,:,3]>=128
        union=int(np.count_nonzero(mask|old));intersection=int(np.count_nonzero(mask&old))
        board.alpha_composite(im,(col*256,row*280+24));draw.text((col*256+5,row*280+5),mode+' phase'+str(phase),fill='white')
        records.append(dict(phase=phase,mode=mode,file=f.relative_to(r).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bodyAlpha128IoU=intersection/union,bodyAlpha128SymmetricDifference=int(np.count_nonzero(mask^old))))
    master=Image.open(r/'character/james-west-master-carry-v1/registered-original-master.png').convert('RGBA');board.alpha_composite(master,(1024,row*280+24));draw.text((1029,row*280+5),'original bare master',fill='white')
board.save(out/'paired-material-quarter-review.png')
(out/'inputs.json').write_text(json.dumps(dict(sourceRecords=records,scope='Four sparse key poses per gear, no interpolation/continuous motion/runtime acceptance.',normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
print(json.dumps(records))
