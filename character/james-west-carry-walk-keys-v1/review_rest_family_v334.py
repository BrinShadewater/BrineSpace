from pathlib import Path
from PIL import Image, ImageDraw
import hashlib,json

p=Path(__file__).resolve().parent
r=p.parents[1]
o=p/'rest-family-review-v334'
o.mkdir(exist_ok=True)
prior=p/'selected-family-audit-v333'
inventory=json.loads((prior/'selected-inventory.json').read_bytes())
provenance=json.loads((prior/'pixel-provenance.json').read_bytes())
changed=[f for f,h in provenance['bindings'].items() if hashlib.sha256((r/f).read_bytes()).hexdigest()!=h]
assert not changed,changed[:10]
families=['sit-down','sit-idle','sit-rise','lie-down','sleep','get-up']
samples=[]
boards=[]
for gear,rows in inventory['gears'].items():
    matches={row['key']:row['sourceMatches'] for row in provenance['gears'][gear]}
    for direction in ['east','south','west','north']:
        board=Image.new('RGB',(1536,900),(48,59,64));draw=ImageDraw.Draw(board)
        for col,family in enumerate(families):
            key=f'{family}-{direction}';row=next(x for x in rows if x['key']==key)
            for stage,slot in enumerate([0,row['frameCount']//2,row['frameCount']-1]):
                source=matches[key][slot][-1];im=Image.open(r/source).convert('RGBA')
                assert hashlib.sha256(im.tobytes()).hexdigest()==row['pixelHashes'][slot]
                m=row['metadata'][slot];scale=148/m['standingHeight']
                size=tuple(round(v*scale) for v in im.size)
                if size!=im.size:im=im.resize(size,Image.Resampling.LANCZOS)
                offset=(round(128-m['pivot'][0]*scale),round(224-m['pivot'][1]*scale))
                tile=Image.new('RGBA',(256,256));tile.alpha_composite(im,offset)
                x=col*256;y=stage*300
                board.paste(tile,(x,y+30),tile)
                draw.text((x+4,y+4),f'{key} [{slot}]',fill='white')
                draw.line((x,y+254,x+255,y+254),fill=(78,98,103))
                samples.append(dict(gear=gear,key=key,slot=slot,source=source,pixelHash=row['pixelHashes'][slot],metadata=m,scale=scale,offset=offset))
        filename=f'{gear}-{direction}.png';board.save(o/filename);boards.append(filename)
report=dict(scope='Selected rest-family first/middle/last source review at declared standing density/pivot. Inventory from v333, all prior source bindings revalidated now. Not a new live loader run or continuous motion/furniture acceptance.',sourceBindingsChecked=len(provenance['bindings']),sourceBindingsChanged=changed,families=families,samples=samples,boards=boards,normalChanged=False,fullGoalComplete=False)
(o/'source-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(boards=len(boards),samples=len(samples),bindingsChecked=report['sourceBindingsChecked'],changed=len(changed))))
