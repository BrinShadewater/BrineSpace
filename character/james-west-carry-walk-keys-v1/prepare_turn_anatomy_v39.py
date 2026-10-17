from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'turn-anatomy-v39';out.mkdir(exist_ok=True)
files=[r/'character/james-carry-headcaps-v1/frames/004.png']+[r/('character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/%03d.png'%i) for i in [8,9,10]]+[r/('character/james-cargo-return-bridges-v1/frames-v9/bare/%03d.png'%i) for i in range(4)]+[p/'master-head-review-v16/bare-000.png']
labels=['standing authority','turn8','turn9','turn10','return0','return1','return2','return3','walk0 authority']
board=Image.new('RGBA',(9*192,312),(48,59,63,255));draw=ImageDraw.Draw(board)
for i,(f,label) in enumerate(zip(files,labels)):
    im=Image.open(f).convert('RGBA');assert im.size==(256,256)
    crop=im.crop((80,96,176,240)).resize((192,288),Image.Resampling.NEAREST)
    board.alpha_composite(crop,(i*192,24));draw.text((i*192+3,5),label,fill='white')
board.convert('RGB').save(out/'actual-source-comparison.png')
(out/'inputs.json').write_text(json.dumps(dict(sources=[dict(role=label,path=f.relative_to(r).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f,label in zip(files,labels)],normalChanged=False),indent=2)+'\n')
print('Nine actual chronological/master source poses prepared for anatomy comparison.')
