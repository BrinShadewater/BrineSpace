from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];files=[r/'character/james-carry-headcaps-v1/frames/004.png',p/'walk12-original.png',p/'walk12-carry.png'];labels=['standing carry master pose','original selected walk12','local carrying walk12']
board=Image.new('RGBA',(768,282),(48,59,63,255));detail=Image.new('RGBA',(1152,410),(48,59,63,255))
for i,(f,label) in enumerate(zip(files,labels)):
    im=Image.open(f).convert('RGBA');board.alpha_composite(im,(i*256,26));ImageDraw.Draw(board).text((i*256+5,7),label,fill='white');detail.alpha_composite(im.crop((80,88,176,184)).resize((384,384),Image.Resampling.NEAREST),(i*384,26));ImageDraw.Draw(detail).text((i*384+5,7),label,fill='white')
board.convert('RGB').save(p/'carrying-family-comparison.png');detail.convert('RGB').save(p/'carrying-family-upper-comparison.png')
a=Image.open(files[1]).convert('RGBA');b=Image.open(files[2]).convert('RGBA');assert a.crop((0,169,256,256)).tobytes()==b.crop((0,169,256,256)).tobytes();assert a.crop((0,0,256,104)).tobytes()==b.crop((0,0,256,104)).tobytes()
(p/'carrying-family-review.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'headAbove104Exact':True,'legsBelow169Exact':True,'donorBounds':a.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox(),'carryingBounds':b.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox(),'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'One source carrying frame versus master carrying and actual selected walk donor. No complete cycle/limb ownership/timing/native acceptance.'},indent=2)+'\n',encoding='utf-8')
print('Exact donor head/legs confirmed; full and upper carry-family comparison prepared.')
