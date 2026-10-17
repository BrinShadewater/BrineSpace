from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
from source_registration import capture_registration
capture_registration()
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'world-evidence.json').read_bytes())
data['results']=[c for c in data['results'] if not c.get('depthDiagnostic')]
inputs=json.loads((p/'world-inputs.json').read_bytes())
registration=json.loads((p/'source-registration-evidence.json').read_bytes())['matches']
case=Image.open(p/'floor-case-west.png').convert('RGBA')
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
for mode in ['bare','helmet']:
    records=[c for c in data['results'] if c['label'].startswith(mode+'-')]
    board=Image.new('RGB',(1920,600),'#303b40');draw=ImageDraw.Draw(board)
    for i,c in enumerate(records):
        x=i*320
        draw.text((x+6,6),c['label'],fill='white')
        source=Image.open(r/c['source'].removeprefix('res://')).convert('RGBA')
        meta=registration[c['label']]
        authority=Image.open(r/meta['source']).convert('RGBA')
        assert source.size==authority.size and source.tobytes()==authority.tobytes()
        assert meta['standingHeight']==148
        # Upper pane is a registered source/prop presentation, not another native
        # capture. Lower pane is the actual room capture from the guarded run.
        if c['enabled']:
            terminal=next(t for t in records if t['label']==mode+'-terminal')
            delta=[round((terminal['foot'][i]-c['foot'][i])/(65.28/148)) for i in range(2)]
            board.paste(case,(x+32+delta[0],28+delta[1]),case)
        pivot=meta['pivot']
        board.paste(source,(x+32+round(128-pivot[0]),28+round(224-pivot[1])),source)
        draw.text((x+6,286),'registered sources / native room below',fill='#b9c2c3')
        world=Image.open(r/c['world'].removeprefix('res://')).convert('RGB')
        world.thumbnail((310,280),Image.Resampling.NEAREST)
        board.paste(world,(x+(320-world.width)//2,310))
    board.save(p/(mode+'-world-review.png'))
(p/'world-review.json').write_text(json.dumps({'selected':False,'visualReviewPending':True,'nativeSourceWorldPairs':len(data['results']),'targetedInputsUnchanged':len(inputs),'scope':data['scope']},indent=2)+'\n')
print('Two native source/room boards;',len(data['results']),'presentations;',len(inputs),'targeted hashes unchanged.')
