from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
out=p/'normal-integration-review';out.mkdir(exist_ok=True)
case=Image.open(p/'floor-case-west-v7.png').convert('RGBA')
normal=json.loads((p/'normal_checkpoint_probe-evidence.json').read_bytes())
title=json.loads((p/'normal-title-validation.json').read_bytes())
assert len(title['results'])==10 and all(x['exitCode']==0 and x['realProfileUnchanged'] for x in title['results'])
counts={'title':0,'legacy':0,'ordinary':0}
def panel(record,label):
    board=Image.new('RGB',(340,590),'#303b40');draw=ImageDraw.Draw(board);draw.text((6,6),label,fill='white')
    source=Image.open(r/record['source'].removeprefix('res://')).convert('RGBA')
    if record['enabled']:board.paste(case,(42,28),case)
    pivot=record['pivot'];board.paste(source,(42+round(128-pivot[0]),28+round(224-pivot[1])),source)
    world=Image.open(r/record['world'].removeprefix('res://')).convert('RGB');world.thumbnail((330,280),Image.Resampling.NEAREST)
    board.paste(world,((340-world.width)//2,300))
    return board
for mode in ['bare','helmet']:
    board=Image.new('RGB',(5*340,590),'#303b40')
    for i,phase in enumerate(['before','after','midpoint','terminal','idle']):
        label=mode+'-normal-checkpoint-v1-'+phase
        saved=next(x for x in normal['results'] if x.get('label')==label+'-saved')
        record=dict(saved,source='res://character/james-floor-case-west-v1/arrival-captures/'+label+'-title-source.png',world='res://character/james-floor-case-west-v1/arrival-captures/'+label+'-title.png')
        a=Image.open(r/saved['source'].removeprefix('res://')).convert('RGBA');b=Image.open(r/record['source'].removeprefix('res://')).convert('RGBA')
        assert a.size==b.size and a.tobytes()==b.tobytes()
        evidence=json.loads((p/(label+'-title-evidence.json')).read_bytes());assert evidence['failures']==0
        board.paste(panel(record,mode+' title Continue / '+phase),(i*340,0));counts['title']+=1
    board.save(out/(mode+'-title.png'))
for family,file in [('legacy','legacy-normal-evidence.json'),('ordinary','ordinary-normal-evidence.json')]:
    data=json.loads((p/file).read_bytes());assert data['failures']==0
    for mode in ['bare','helmet']:
        rows=[x for x in data['results'] if x.get('label','').startswith(mode+'-')]
        board=Image.new('RGB',(340*len(rows),590),'#303b40')
        for i,c in enumerate(rows):board.paste(panel(c,c['label']),(i*340,0));counts[family]+=1
        board.save(out/(mode+'-'+family+'.png'))
(out/'review.json').write_text(json.dumps({'visualReviewPending':True,'pairs':counts,'normalSavedRestoredCompletedPairsPreviouslyReviewed':30,'sourceRegistration':'Original pivots/H148 and fixed case prop; native actual room pixels beneath. Title source equality asserted to exact normal saved source.','scope':'Additional ten title/two legacy/eight ordinary source/native room pairs. Not all master/cardinal/natural scheduling or continuously watched playback acceptance.'},indent=2)+'\n')
print(json.dumps(counts))
