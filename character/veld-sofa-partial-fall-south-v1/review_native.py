from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-partial-south-staged-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==24
bindings={};boards=[];pairs=0
for record in records:
    names=[record['name']+'-living']+[p['label'] for p in record['presentations']]
    board=Image.new('RGB',(1620,664),'#202a30');d=ImageDraw.Draw(board)
    for index,name in enumerate(names):
        source=O/(name+'-source.png');native=O/(name+'-room.png')
        for path in [source,native]:bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
        image=Image.open(source).convert('RGBA');padded=Image.new('RGBA',(256,272));padded.alpha_composite(image);small=padded.resize((128,136),Image.Resampling.LANCZOS)
        x=index%9*180;y=index//9*320;board.paste(small,(x+26,y+18),small);board.paste(Image.open(native).convert('RGB').crop((490,286,660,424)),(x+5,y+165));d.text((x+5,y+3),'living' if index==0 else str(record['presentations'][index-1]['elapsed'])+'s',fill='white');pairs+=1
    d.text((5,644),record['name']+' / exact live partial source / staged fractional support and finite floor fall',fill='white')
    path=P/(record['name']+'-native-review.png');board.save(path);boards.append(path.name)
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    path=O/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
evidence={'boards':boards,'nativeSourcePairs':pairs,'worldDeaths':24,'actorFileRestores':96,'malformedGuards':168,'bindings':bindings,'visualReview':'pending','scope':'candidate-only injection; normally selected South sit/rise from actual timed reading service, both gear versions and all6partial poses; actual world mortality API/roster, same-clock actor-file restores; prescribed default sofa, paused world; no ordinary disk/fresh-main future or normal partial admission'}
(P/'native-review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
(P/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Veld partial South sofa fall audition</title><style>body{background:#202a30;color:#e0e8ec;font:16px system-ui;margin:24px}img{max-width:100%}p{max-width:85ch}</style><h1>Veld — partial South sit/rise fall audition</h1><p>Six current partial entrances, both gears. Exact whole existing body/helmet source aliases, no grade or scale changes. Early poses use authored ground-collapse interiors; later poses use neutral sofa fall. Staged: ordinary world disk/future continuation and normal admission remain pending.</p><img src="bare-source-review.png"><img src="helmet-source-review.png">'+''.join('<p><img src="'+board+'"></p>' for board in boards),encoding='utf-8')
print(json.dumps({'boards':24,'nativeSourcePairs':pairs}))
