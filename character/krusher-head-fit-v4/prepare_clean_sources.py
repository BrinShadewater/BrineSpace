from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2]; P=Path(__file__).resolve().parent
raw=Image.open(P/'generated-clean-heads.png').convert('RGBA')
regions={}; heads={}
for i,d in enumerate(['south','east','north','west']):
    part=raw.crop((i*raw.width//4,0,(i+1)*raw.width//4,raw.height))
    box=Image.fromarray((np.array(part)[:,:,3]>128).astype('uint8')*255).getbbox(); part=part.crop(box)
    # Shared uniform physical scale; preserve longer profile width and neck.
    scale=29/float(480)
    size=tuple(round(v*scale) for v in part.size)
    head=part.resize(size,Image.Resampling.NEAREST)
    path=P/'sources'/f'clean-bare-{d}-native.png'; head.save(path); heads[d]=head
    regions[d]={'quarter':i,'alphaBox':box,'sourceSize':part.size,'uniformScale':scale,'nativeSize':size,'output':path.relative_to(P).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(P/'clean-extraction.json').write_text(json.dumps({'source':'generated-clean-heads.png','method':'Generated alpha retained, four quarter crops and a shared uniform nearest-neighbour scale. No separate width/height fitting or invented RGB.','regions':regions},indent=2)+'\n')
board=Image.new('RGBA',(1200,600),'#252b2e'); draw=ImageDraw.Draw(board); font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22)
fits=json.loads((R/'character/krusher-james-motion-fit-v2/verification.json').read_text())['records']
for col,d in enumerate(['south','east','north','west']):
    q=next(q for q in fits if q['state']=='idle-'+d and q['frame']==0)
    original=Image.open(R/q['source']).convert('RGBA')
    head=heads[d]
    board.alpha_composite(original.resize((368,368),Image.Resampling.NEAREST),(col*300-35,45))
    board.alpha_composite(head.resize((head.width*5,head.height*5),Image.Resampling.NEAREST),(col*300+60,410))
    draw.text((col*300+12,12),d+' / Original James + new source',font=font,fill='white')
board.save(P/'original-fit-reference.png')
print(json.dumps({d:regions[d]['nativeSize'] for d in regions}))
