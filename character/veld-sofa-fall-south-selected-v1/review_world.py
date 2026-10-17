"""All real world/death checkpoint captures, source and continued room positions."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-selected-continue-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text(encoding='utf-8'));assert len(records)==20
bindings={};boards=[];pair_count=0
master=Image.open(R/'character/crew-runtime-matte-v1/veld/frames/idle-south-breathing-v1/000.png').convert('RGBA')
def read_capture(name):
    global pair_count
    source=O/(name+'-source.png');native=O/(name+'-room.png')
    for p in [source,native]:bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    pair_count+=1
    padded=Image.new('RGBA',(256,272));padded.alpha_composite(Image.open(source).convert('RGBA'))
    return padded.resize((128,136),Image.Resampling.LANCZOS),Image.open(native).convert('RGB').crop((490,286,660,424))
for record in records:
    name=record['name'];changes=[sample['tick'] for sample in record['reference'] if 'rendered' in sample]
    width=max(3,len(changes))*180;board=Image.new('RGB',(width,970),'#202a30');d=ImageDraw.Draw(board)
    for col,suffix in enumerate(['living','before','after']):
        image,room=read_capture(name+'-'+suffix);board.paste(image,(col*180+26,25),image);board.paste(room,(col*180+5,167));d.text((col*180+5,8),suffix,fill='white')
    for row,branch in enumerate(['reference','resumed']):
        for col,tick in enumerate(changes):
            image,room=read_capture(name+'-'+branch+'-tick-%02d'%tick)
            y=320+row*300;board.paste(image,(col*180+26,y),image)
            board.paste(room,(col*180+5,y+145))
            d.text((col*180+5,y-15),branch+' tick '+str(tick),fill='white')
    d.text((5,945),name+' / '+record['recipe']['clip']+' / save '+str(record['saveElapsed'])+'s',fill='white')
    path=P/(name+'-world-review.png');board.save(path);boards.append(path.name)
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    p=O/name;bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
evidence={'boards':boards,'nativeSourcePairs':pair_count,'worldDeathCases':20,'freshDiskRestores':20,'futureActorSteps':6000,'bindings':bindings,'visualReview':'pending','scope':'normally selected paired fall, actual world mortality APIs/roster; prescribed default South sofa; ordinary disk/fresh-main Continue and 150 reference/resumed 20ms actor updates per case; world scheduler paused, not title/new-process or natural hazard/chooser coverage'}
(P/'world-review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
(P/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Veld sofa fall — normal world Continue</title><style>body{background:#202a30;color:#e0e8ec;font:16px system-ui;margin:24px}img{max-width:100%}p{max-width:85ch}</style><h1>Veld — South sofa fall and Continue</h1><p>Normally selected tablet and empty-handed falls. Actual world death, normal disk checkpoint and fresh-scene continuation across 20 contexts. Prescribed sofa and paused-world actor stepping; continuous motion, natural hazards and title/new-process Continue remain separate.</p><img src="../veld-sofa-fall-south-v1/neutral-source-review.png"><img src="../veld-sofa-fall-south-v1/paired-source-review.png">'+''.join('<p><img src="'+b+'"></p>' for b in boards),encoding='utf-8')
print(json.dumps({'boards':len(boards),'nativeSourcePairs':pair_count}))
