"""Actual staged sofa submissions beside exact source and master references."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-fall-south-staged-v1'
records=json.loads((O/'records.json').read_text(encoding='utf-8'));boards=[];bindings={}
for gear in ['bare','helmet']:
    for elapsed in ['0.05','0.1','0.25','0.4','2.4','4.2']:
        prefix=gear+'-'+elapsed
        names=[prefix+'-living']+[r['name'] for r in records if r['name'].startswith(prefix+'-')]
        board=Image.new('RGB',(len(names)*180,364),'#202a30');d=ImageDraw.Draw(board)
        for col,name in enumerate(names):
            source=O/(name+'-source.png');native=O/(name+'-room.png')
            for p in [source,native]:bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
            im=Image.open(source).convert('RGBA');padded=Image.new('RGBA',(256,272));padded.alpha_composite(im);small=padded.resize((128,136),Image.Resampling.LANCZOS)
            board.paste(small,(col*180+26,20),small)
            board.paste(Image.open(native).convert('RGB').crop((490,286,660,424)),(col*180+5,190))
            d.text((col*180+5,3),name,fill='white')
        d.text((5,342),'Exact current reader entrance; staged authored fall; actual sofa/native captures; H74 sources',fill='white')
        path=P/(prefix+'-native-review.png');board.save(path);boards.append(path.name)
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    p=O/name;bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(P/'native-review-evidence.json').write_text(json.dumps({'boards':boards,'nativeSourcePairs':(len(bindings)-7)//2,'scope':'candidate manifests injected only in fixture; normally selected reader; prescribed default South sofa contact, actor mortality APIs and actor-file restores; not normal fall admission, world roster/hazard or ordinary RunSave future Continue','bindings':bindings,'visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
(P/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Veld South sofa fall candidate</title><style>body{background:#202a30;color:#e0e8ec;font:16px system-ui;margin:24px}img{max-width:100%}p{max-width:85ch}</style><h1>Veld — South sofa fall candidate</h1><p>Exact current reading entrance, supported slump, floor brace and relaxed rest. Staged candidate: normal admission, actual world mortality and ordinary save/future Continue remain open. All sources use one H148 standing ruler, matte master palette and selected shared shell.</p><img src="paired-source-review.png">'+''.join('<p><img src="'+b+'"></p>' for b in boards),encoding='utf-8')
print(json.dumps({'boards':len(boards),'nativeSourcePairs':(len(bindings)-7)//2}))
