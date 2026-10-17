from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1];case=Image.open(p/'floor-case-west-v7.png').convert('RGBA');metrics=[]
for gear in ['bare','helmet']:
    original=Image.open(r/f'character/james-cargo-material-joined-v1/frames/{gear}/unload-west/004.png').convert('RGBA');mid=Image.open(p/f'midpoint-body-v1/{gear}/000.png').convert('RGBA');prior=Image.open(p/f'rise-v4/{gear}/000.png').convert('RGBA');standing=Image.open(p/f'standing-body-v2/{gear}/000.png').convert('RGBA')
    assert case.crop((74,192,117,224)).tobytes()==original.crop((74,192,117,224)).tobytes()
    protected=sum(mid.getpixel((x,y))==prior.getpixel((x,y)) for y in range(256) for x in range(256) if not (x<120 and 192<=y<225));assert protected==61576
    rows=[original,case.copy(),case.copy()];rows[1].alpha_composite(mid);rows[2].alpha_composite(standing)
    board=Image.new('RGB',(1536,800),'#303b40');draw=ImageDraw.Draw(board)
    for n,image in enumerate(rows):
        scaled=image.resize((512,512),Image.Resampling.NEAREST);board.paste(scaled,(n*512,25),scaled)
        draw.text((n*512+4,5),['original release4','body-only midpoint+original case','canonical standing+same case'][n],fill='white')
        roi=image.crop((70,190,170,230)).resize((500,200),Image.Resampling.NEAREST);board.paste(roi,(n*512+4,570),roi)
    board.save(p/(gear+'-shared-case-source-review.png'))
    metrics.append({'gear':gear,'protectedPixels':protected,'midBodyBounds':mid.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox(),'midSourceSha256':hashlib.sha256((p/f'midpoint-body-v1/{gear}/000.png').read_bytes()).hexdigest()})
(p/'shared-case-source-review.json').write_text(json.dumps({'selected':False,'visualReviewPending':True,'caseAlpha128Bounds':case.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox(),'metrics':metrics,'scope':'Registered original release/midpoint/standing common256canvas/p128224/H148, same exact-cropped original case. Explicit crop trims rightmost low-alpha outline to exclude adjacent toe; no invented case pixels or whole-unoccluded case claim. Five-times foot/case details; no motion acceptance.'},indent=2)+'\n')
print(json.dumps(metrics))
