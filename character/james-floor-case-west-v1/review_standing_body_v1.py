from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
refs=json.loads((p/'rise-reference-evidence.json').read_bytes())
assert all(hashlib.sha256((r/c['source']).read_bytes()).hexdigest()==c['sha256'] for c in refs['sources'])
data=json.loads((p/'motion_rise_v4-evidence.json').read_bytes());case=Image.open(p/'floor-case-west-v6.png').convert('RGBA');metrics=[]
for gear in ['bare','helmet']:
    original=Image.open(r/next(c['source'] for c in refs['sources'] if c['gear']==gear and c['index']==5)).convert('RGBA')
    body=Image.open(p/f'standing-body-v1/{gear}/000.png').convert('RGBA')
    assert body.crop((0,0,256,194)).tobytes()==original.crop((0,0,256,194)).tobytes()
    record=next(x for x in data['results'] if x.get('label')==gear+'-motion-rise-v4-017')
    idle=Image.open(r/record['source'].removeprefix('res://')).convert('RGBA');pivot=record['pivot'];assert record['height']==148
    registered=Image.new('RGBA',(256,256));registered.alpha_composite(idle,(round(128-pivot[0]),round(224-pivot[1])))
    composite=case.copy();composite.alpha_composite(body);idle_case=case.copy();idle_case.alpha_composite(registered)
    board=Image.new('RGB',(2048,810),'#303b40');draw=ImageDraw.Draw(board)
    for n,(label,image) in enumerate([('original standing+embedded case',original),('body-only standing draft',body),('draft+separate V6 case',composite),('actual next source+V6 case',idle_case)]):
        scaled=image.resize((512,512),Image.Resampling.NEAREST);board.paste(scaled,(n*512,25),scaled);draw.text((n*512+4,5),label,fill='white')
        roi=image.crop((100,185,166,230)).resize((396,270),Image.Resampling.NEAREST);board.paste(roi,(n*512+40,540),roi)
    board.save(p/(gear+'-standing-body-v1-review.png'))
    bounds=body.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox();metrics.append({'gear':gear,'bodyAlpha128Bounds':bounds,'protectedUpperPixelChecks':256*194,'bodySha256':hashlib.sha256((p/f'standing-body-v1/{gear}/000.png').read_bytes()).hexdigest(),'nextSource':record['source'],'nextSourcePivot':pivot})
assert Image.open(p/'standing-body-v1/bare/000.png').crop((0,194,256,256)).tobytes()==Image.open(p/'standing-body-v1/helmet/000.png').crop((0,194,256,256)).tobytes()
(p/'standing-body-v1-review-evidence.json').write_text(json.dumps({'selected':False,'visualReviewPending':True,'metrics':metrics,'scope':'Shared original canvas/p128224/H148, next actually captured source registered by its original pivot; no individual pose height normalization. Static source/prop composites and6xboot detail only; no new runtime motion acceptance.'},indent=2)+'\n')
print(json.dumps(metrics))
