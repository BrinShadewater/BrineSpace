from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
files=[r/'character/james-west-master-carry-v1/local-v3-carry-pose.png']+[p/f'walk{i:02d}-case-master-v5.png' for i in (0,8,12,20,28,36,44,48)]
for start in (0,3,6):
    board=Image.new('RGBA',(1440,510),(48,59,63,255));d=ImageDraw.Draw(board)
    for col,f in enumerate(files[start:start+3]):
        board.alpha_composite(Image.open(f).convert('RGBA').crop((80,112,160,192)).resize((480,480),Image.Resampling.NEAREST),(col*480,30))
        d.text((col*480+5,8),'standing carry reference (provisional)' if start==0 and col==0 else f.stem,fill='white')
    board.convert('RGB').save(p/f'case-master-v5-result-audit-{start}.png')
(p/'case-master-v5-result-audit-inputs.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'visualReviewPending':True,'referenceAuthority':'Original-selected-idle-based local3 standing carry candidate, not a replacement owner-locked master.'},indent=2)+'\n',encoding='utf-8')
print('Nine same-crop reference/result case views prepared.')
