from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
from source_registration import capture_registration
p=Path(__file__).resolve().parent;r=p.parents[1]
capture_registration('delta-evidence.json','delta-registration-evidence.json')
data=json.loads((p/'delta-evidence.json').read_bytes())
inputs=json.loads((p/'delta-inputs.json').read_bytes())
registration=json.loads((p/'delta-registration-evidence.json').read_bytes())['matches']
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
case=Image.open(p/'floor-case-west.png').convert('RGBA')
for mode in ['bare','helmet']:
    records=[c for c in data['results'] if c.get('label','').startswith(mode+'-')]
    assert len(records)==4
    board=Image.new('RGB',(1280,600),'#303b40');draw=ImageDraw.Draw(board)
    for i,c in enumerate(records):
        x=i*320;draw.text((x+6,6),c['label'],fill='white')
        meta=registration[c['label']];assert meta['standingHeight']==148
        source=Image.open(r/c['source'].removeprefix('res://')).convert('RGBA')
        authority=Image.open(r/meta['source']).convert('RGBA')
        assert source.size==authority.size and source.tobytes()==authority.tobytes()
        if c['enabled']:board.paste(case,(x+32,28),case)
        pivot=meta['pivot'];board.paste(source,(x+32+round(128-pivot[0]),28+round(224-pivot[1])),source)
        draw.text((x+6,286),'registered sources / native room below',fill='#b9c2c3')
        world=Image.open(r/c['world'].removeprefix('res://')).convert('RGB')
        world.thumbnail((310,280),Image.Resampling.NEAREST)
        board.paste(world,(x+(320-world.width)//2,310))
    board.save(p/(mode+'-delta-review.png'))
(p/'delta-review.json').write_text(json.dumps({'selected':False,'visualReviewPending':True,'nativeSourceWorldPairs':8,'targetedInputsUnchanged':len(inputs),'crossings':[c for c in data['results'] if c.get('crossing')],'scope':data['scope']},indent=2)+'\n')
print('Eight source/room presentations packaged;12 targeted hashes unchanged.')
