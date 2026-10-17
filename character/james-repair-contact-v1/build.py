"""Measure selected flame pixels using the actual physical-foot rendering transform."""
import hashlib, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SCALE = 384 * .17 / 148
# Main subtracts .038 cells and the renderer adds it back. Physical actor.foot
# already denotes the rendered pivot, so no second deck lift belongs here.
LIFT = 0.0
OLD = {'north': [16,-127], 'east': [37,-75], 'south': [0,-59], 'west': [-35,-75]}
rows = []
bare_masks = {}
for gear in ['bare', 'helmet']:
    manifest_path = ROOT / f'character/james-torch-material-residue-v2/{gear}-manifest.json'
    manifest = json.loads(manifest_path.read_bytes())
    for state in manifest['states']:
        if not state['id'].startswith('weld-'): continue
        direction = state['id'].removeprefix('weld-')
        for index, reference in enumerate(state['frameFiles']):
            p = ROOT / reference.removeprefix('res://')
            a = np.array(Image.open(p).convert('RGBA')).astype(int)
            mask = (a[:,:,3]>150)&(a[:,:,2]>140)&(a[:,:,2]>a[:,:,0]+40)&(a[:,:,1]>100)
            if gear == 'bare':
                bare_masks[direction,index] = mask
            else:
                # The fitted visor is also cyan. Bound the flame to its paired
                # bare-source mask, never average helmet glass into contact.
                paired = bare_masks[direction,index]
                assert np.all(mask[paired])
                mask = paired
            y,x = np.nonzero(mask)
            assert len(x) > 0
            xy = [float(x.mean()),float(y.mean())]
            rows.append(dict(gear=gear, direction=direction,index=index, path=reference,
                             sha256=hashlib.sha256(p.read_bytes()).hexdigest(), cyanPixels=len(x), sourcePoint=xy))
offsets = {}
for direction in OLD:
    selected = [r for r in rows if r['direction']==direction and r['gear']=='bare']
    mean = np.mean([r['sourcePoint'] for r in selected],axis=0)
    offsets[direction] = [round(float((mean[0]-92)*SCALE),6),round(float((mean[1]-172)*SCALE+LIFT),6)]
for r in rows:
    r['worldPoint'] = [(r['sourcePoint'][0]-92)*SCALE,(r['sourcePoint'][1]-172)*SCALE+LIFT]
    r['errorWorld'] = math.dist(r['worldPoint'],offsets[r['direction']])
    r['oldErrorWorld'] = math.dist(r['worldPoint'],OLD[r['direction']])
    assert r['errorWorld'] < .8
(OUT/'torch-tip-offsets.json').write_text(json.dumps(offsets,indent=2)+'\n')
(OUT/'source-evidence.json').write_text(json.dumps(dict(references=len(rows),newDrawings=0,
    scale=SCALE,deckLift=LIFT,maximumWorldError=max(r['errorWorld'] for r in rows),
    minimumOldWorldError=min(r['oldErrorWorld'] for r in rows),rows=rows),indent=2)+'\n')
for page in range(math.ceil(len(rows)/60)):
    subset=rows[page*60:(page+1)*60]
    board=Image.new('RGB',(1840,1230),(45,55,60)); d=ImageDraw.Draw(board)
    d.text((8,8),'James selected held torch / fixed source scale / green=corrected flame / old generic anchor often outside source canvas',fill='white')
    for n,r in enumerate(subset):
        x=n%10*184;y=30+n//10*200
        im=Image.open(ROOT/r['path'].removeprefix('res://')).convert('RGBA');board.paste(im,(x,y),im)
        tip=offsets[r['direction']];px=x+92+tip[0]/SCALE;py=y+172+(tip[1]-LIFT)/SCALE
        d.ellipse((px-3,py-3,px+3,py+3),outline='#80ff80')
        d.text((x+4,y+182),f"{r['gear']} {r['direction']} #{r['index']}",fill='white')
    board.save(OUT/f'source-page{page}.png')
print(json.dumps({'references':len(rows),'offsets':offsets,'maxWorldError':max(r['errorWorld'] for r in rows),'minOldWorldError':min(r['oldErrorWorld'] for r in rows),'boards':math.ceil(len(rows)/60)}))
