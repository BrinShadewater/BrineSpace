from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'priority-evidence.json').read_bytes())
inputs=json.loads((p/'priority-inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
case=Image.open(p/'floor-case-west.png').convert('RGBA')
records=[c for c in data['results'] if 'label' in c]
assert len(records)==48
for mode in ['bare','helmet']:
    for phase in ['before','after']:
        board=Image.new('RGB',(2040,1200),'#303b40');draw=ImageDraw.Draw(board)
        for col,hazard in enumerate(['gear','death','fire','water','floor','service']):
            initial=next(c for c in records if c['label']==mode+'-floor-priority-'+phase+'-'+hazard+'-initial')
            for row,step in enumerate(['initial','replaced']):
                label=mode+'-floor-priority-'+phase+'-'+hazard+'-'+step
                c=next(c for c in records if c['label']==label)
                assert c['height']==148 and len(c['pivot'])==2
                x=col*340;y=row*600;draw.text((x+6,y+6),hazard+' / '+step+' / '+c['gear'],fill='white')
                source=Image.open(r/c['source'].removeprefix('res://')).convert('RGBA')
                if c['enabled']:
                    delta=[round((initial['foot'][j]-c['foot'][j])/(65.28/148)) for j in range(2)]
                    board.paste(case,(x+42+delta[0],y+28+delta[1]),case)
                pivot=c['pivot'];board.paste(source,(x+42+round(128-pivot[0]),y+28+round(224-pivot[1])),source)
                draw.text((x+6,y+286),'registered source / actual native room below',fill='#b9c2c3')
                world=Image.open(r/c['world'].removeprefix('res://')).convert('RGB')
                world.thumbnail((330,280),Image.Resampling.NEAREST)
                board.paste(world,(x+(340-world.width)//2,y+310))
        board.save(p/(mode+'-'+phase+'-priority-review.png'))
out={'selected':False,'visualReviewPending':True,'nativeSourceWorldPairs':48,'targetedInputsUnchanged':len(inputs),'registration':'Native captured texture pivot and standingHeight148. Upper source/prop composite; lower native room pixels. No whole-source/master identity or continuous motion claim.','scope':data['scope']}
(p/'priority-review.json').write_text(json.dumps(out,indent=2)+'\n')
print('Four before/after priority boards;48 source/room pairs;13 targeted hashes unchanged.')
