from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'case-projection-v42';out.mkdir(exist_ok=True)
fs=[r/'character/james-carry-headcaps-v1/frames/004.png',p/'coherent-turn-v40/bare-candidate.png',p/'whole-belt-admission-v35/bare-candidate.png']+[p/'master-head-review-v16'/('bare-%03d.png'%i) for i in [0,1,3,8,20,28]]
labels=['standing case authority','turn9-guided intermediate','V35 profile intermediate']+['walk '+str(i) for i in [0,1,3,8,20,28]]
box=(88,116,152,160);scale=4;w=256;h=176;board=Image.new('RGBA',(w*3,(h+24)*3),(48,59,63,255));draw=ImageDraw.Draw(board)
for i,(f,label) in enumerate(zip(fs,labels)):
    im=Image.open(f).convert('RGBA');x=i%3*w;y=i//3*(h+24);board.alpha_composite(im.crop(box).resize((w,h),Image.Resampling.NEAREST),(x,y+24));draw.text((x+3,y+6),label,fill='white')
board.convert('RGB').save(out/'case-hand-comparison.png')
(out/'inputs.json').write_text(json.dumps(dict(sources=[dict(path=f.relative_to(r).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),role=label) for f,label in zip(fs,labels)],crop=list(box),displayScale=scale,normalChanged=False),indent=2)+'\n')
print('Nine same-coordinate case/hand comparisons prepared, no artwork changed.')
