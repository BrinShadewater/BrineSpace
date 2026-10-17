from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
sources=[r/'character/james-carry-headcaps-v1/frames/004.png',p/'walk00-case-v2-fleck.png',r/'character/james-west-carry-depth-v1/walk12-carry.png',p/'walk28-tool-fix.png',p/'walk36-tool-fix.png']
labels=['standing master','corrected0','phase12','phase28','phase36']
board=Image.new('RGBA',(1920,410),(48,59,63,255));d=ImageDraw.Draw(board)
full=Image.new('RGBA',(1280,282),(48,59,63,255));fd=ImageDraw.Draw(full)
for i,(f,label) in enumerate(zip(sources,labels)):
    im=Image.open(f).convert('RGBA');board.alpha_composite(im.crop((80,88,176,184)).resize((384,384),Image.Resampling.NEAREST),(384*i,26));d.text((384*i+5,7),label,fill='white')
    full.alpha_composite(im,(256*i,26));fd.text((256*i+5,7),label,fill='white')
board.convert('RGB').save(p/'case-v2-family-upper.png');full.convert('RGB').save(p/'case-v2-family-full.png')
(p/'case-v2-family-review.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sources},'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Static same-ruler case/grip comparisons; no full cycle/native acceptance.'},indent=2)+'\n',encoding='utf-8')
print('Corrected phase0 cross-key comparison prepared.')
