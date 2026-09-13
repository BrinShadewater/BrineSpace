"""Retain existing side shelf inventories and prepare exact texture turns."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/observation-owner-v2'
records={}
for side in ['west','east']:
    d=json.loads((ROOT/f'rooms/full-wall-v1/registrations/side-observation-shelves-{side}.json').read_text())
    im=Image.open(ROOT/d['source'].removeprefix('res://')).convert('RGBA')
    mask=Image.new('L',im.size);draw=ImageDraw.Draw(mask)
    for piece in d['pieces']:draw.polygon([tuple(p) for p in piece],fill=255)
    im.putalpha(mask);box=mask.getbbox();im=im.crop(box)
    outputs={}
    for q,turn in [(0,None),(1,Image.Transpose.ROTATE_270),(2,Image.Transpose.ROTATE_180),(3,Image.Transpose.ROTATE_90)]:
        out=im if turn is None else im.transpose(turn);p=PACK/f'observation_{side}-q{q}.png';out.save(p)
        outputs[q]={'size':out.size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    records[side]={'original_source':d['source'],'crop':box,'outputs':outputs}
(PACK/'side-turns.json').write_text(json.dumps(records,indent=2)+'\n')
