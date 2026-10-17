"""Exact-root shared cardinal/source audit before half-turn reconstruction."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
def carry_frame(direction):
    p=R/f'character/veld-carry-{direction}-consistent-v1/bare-manifest.json';data=json.loads(p.read_text(encoding='utf-8'))
    state=next(s for s in data['states'] if s['id']=='carry-'+direction);ref=state['frameFiles'][0]
    return R/ref[6:] if ref.startswith('res://') else p.parent/ref
rows=[('North','north',[
 ('New NW start',P/'north-west-candidate-v4/frames/bare/000.png'),
 ('Selected NE start',R/'character/veld-carry-turn-north-east-consistent-v1/frames/bare/carry-turn-north-east/000.png'),
 ('Selected carry0',carry_frame('north'))]),
 ('East','east',[
 ('Selected NE end',R/'character/veld-carry-turn-north-east-consistent-v1/frames/bare/carry-turn-north-east/005.png'),
 ('Selected ES start',R/'character/veld-carry-turn-east-south-consistent-v1/frames/bare/carry-turn-east-south/000.png'),
 ('Selected carry0',carry_frame('east'))]),
 ('South','south',[
 ('New SW start',P/'candidate-v7/frames/bare/000.png'),
 ('Selected ES end',R/'character/veld-carry-turn-east-south-consistent-v1/frames/bare/carry-turn-east-south/005.png'),
 ('Selected carry0',carry_frame('south'))])]
board=Image.new('RGB',(1280,1296),'#202a30');draw=ImageDraw.Draw(board);records=[]
for ri,(name,direction,items) in enumerate(rows):
    for ci,(label,path) in enumerate(items):
        im=Image.open(path).convert('RGBA');assert im.size==(256,256)
        a=np.array(im);yy,xx=np.where(a[:,:,3]>128);top=int(yy.min());_,hx=np.where(a[top:top+20,:,3]>128)
        record={'direction':direction,'label':label,'path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'headTop20Width':int(hx.max()-hx.min()+1),'alphaHeight':int(yy.max()-yy.min()+1)};records.append(record)
        x=ci*320;y=ri*432;draw.text((x+4,y+4),name+' / '+label,fill='white');board.paste(im,(x,y+24),im)
        crop=im.crop((90,68,170,128)).resize((240,180),Image.Resampling.NEAREST);board.paste(crop,(x+40,y+250),crop)
    # Original living master ruler; this is source density normalization for
    # comparison only, never an endpoint made by altering body anatomy.
    mp=R/f'character/veld-side-foundation-v1/{direction}-standing.png' if direction=='east' else None
    if mp is not None:
        im=Image.open(mp).convert('RGBA');out=Image.new('RGBA',(256,256));out.alpha_composite(im,(36,52))
        board.paste(out,(960,ri*432+24),out);draw.text((964,ri*432+4),'Original East master',fill='white')
        crop=out.crop((90,68,170,128)).resize((240,180),Image.Resampling.NEAREST);board.paste(crop,(1000,ri*432+250),crop)
board.save(P/'cardinal-join-audit.png')
(P/'cardinal-join-audit.json').write_text(json.dumps({'presentations':9,'rows':records,'visualReview':'pending','scope':'same256canvas/p128224 whole cardinal held endpoints and enlarged head/collar/case, not runtime join acceptance'},indent=2)+'\n',encoding='utf-8')
print(json.dumps([(r['label'],r['direction'],r['headTop20Width']) for r in records]))
