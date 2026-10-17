from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
sources=[r/'character/james-carry-headcaps-v1/frames/004.png',p/'walk00-case-v2-fleck.png',p/'walk08-carry.png',r/'character/james-west-carry-depth-v1/walk12-carry.png',p/'walk20-carry.png',p/'walk28-tool-fix.png',p/'walk36-tool-fix.png']
labels=['master','0','8','12','20','28','36'];crop=(80,120,152,168)
for start in (0,4):
    batch=list(zip(sources,labels))[start:start+4];board=Image.new('RGBA',(576*len(batch),410),(48,59,63,255));d=ImageDraw.Draw(board)
    for col,(f,label) in enumerate(batch):
        im=Image.open(f).convert('RGBA').crop(crop).resize((576,384),Image.Resampling.NEAREST)
        board.alpha_composite(im,(576*col,26));d.text((576*col+5,7),'case '+label,fill='white')
    board.convert('RGB').save(p/f'case-geometry-{start}.png')
(p/'case-geometry-inputs.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sources},'crop':list(crop),'visualReviewPending':True,'scope':'Aligned crop only, no isolated case mask/dimension metric or artwork change.'},indent=2)+'\n',encoding='utf-8')
print('Seven aligned case/grip/tool crops prepared.')
