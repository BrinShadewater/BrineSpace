from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'normal_checkpoint_probe-evidence.json').read_bytes())
inputs=json.loads((p/'normal_checkpoint_probe-inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
records=[c for c in data['results'] if 'label' in c]
assert len(records)==30
case=Image.open(p/'floor-case-west-v7.png').convert('RGBA')
for mode in ['bare','helmet']:
    for phase in ['before','after','midpoint','terminal','idle']:
        board=Image.new('RGB',(1020,600),'#303b40');draw=ImageDraw.Draw(board)
        initial=next(c for c in records if c['label']==mode+'-normal-checkpoint-v1-'+phase+'-saved')
        for col,step in enumerate(['saved','restored','completed']):
            c=next(c for c in records if c['label']==mode+'-normal-checkpoint-v1-'+phase+'-'+step)
            assert c['height']==148
            x=col*340;draw.text((x+6,6),mode+' / '+phase+' / '+step,fill='white')
            source=Image.open(r/c['source'].removeprefix('res://')).convert('RGBA')
            if c['enabled']:
                delta=[round((initial['foot'][j]-c['foot'][j])/(65.28/148)) for j in range(2)]
                board.paste(case,(x+42+delta[0],28+delta[1]),case)
            pivot=c['pivot'];board.paste(source,(x+42+round(128-pivot[0]),28+round(224-pivot[1])),source)
            draw.text((x+6,286),'registered source / actual native room below',fill='#b9c2c3')
            world=Image.open(r/c['world'].removeprefix('res://')).convert('RGB')
            world.thumbnail((330,280),Image.Resampling.NEAREST)
            board.paste(world,(x+(340-world.width)//2,310))
        board.save(p/(mode+'-'+phase+'-normal-checkpoint-v1-review.png'))
(p/'normal-checkpoint-v1-review.json').write_text(json.dumps({'selected':False,'visualReviewPending':True,'nativeSourceWorldPairs':30,'targetedInputsUnchanged':len(inputs),'registration':'Native pivots/H148; upper source/prop composites, lower actual native rooms. Immediate restored source whole RGBA exact.','scope':data['scope']},indent=2)+'\n')
print('Ten normal disk/fresh-main boards;30native source-world pairs;'+str(len(inputs))+' targeted inputs unchanged.')
