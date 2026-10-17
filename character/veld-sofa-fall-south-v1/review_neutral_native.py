"""Retain separate native empty-hand evidence without replacing earlier review."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-fall-south-neutral-staged-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text(encoding='utf-8'));boards=[];bindings={}
for gear in ['bare','helmet']:
    for elapsed in ['0.05','0.1','0.25','0.4','2.4','4.2','11.95']:
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
        d.text((5,342),'Exact live entrance / empty-hand or tablet branch / native supported fall',fill='white')
        path=P/('neutral-'+prefix+'-native-review.png');board.save(path);boards.append(path.name)
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    p=O/name;bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
evidence={'boards':boards,'nativeSourcePairs':(len(bindings)-7)//2,'scope':'two neutral entrances plus five tablet/draw poses per gear, paused-world actor death and actor-file restore; no ordinary RunSave/world mortality proof','bindings':bindings,'visualReview':'pending'}
(P/'neutral-native-review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
(P/'neutral-review.html').write_text('<!doctype html><meta charset="utf-8"><title>Veld South sofa empty-hand fall</title><style>body{background:#202a30;color:#e0e8ec;font:16px system-ui;margin:24px}img{max-width:100%}</style><h1>Veld — empty-handed sofa fall</h1><p>Authored forearm and waist patches only. Reviewed head, helmet and remaining body retained exactly. Both branches staged; world mortality and ordinary Continue remain pending.</p><img src="neutral-source-review.png"><p>Original tablet family and master:</p><img src="paired-source-review.png">'+''.join('<p><img src="'+b+'"></p>' for b in boards),encoding='utf-8')
print(json.dumps({'boards':len(boards),'nativeSourcePairs':evidence['nativeSourcePairs']}))
