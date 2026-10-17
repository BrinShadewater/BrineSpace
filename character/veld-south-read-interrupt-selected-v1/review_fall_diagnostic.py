from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];P=R/'character/veld-south-sofa-fall-diagnostic-v1';P.mkdir(exist_ok=True)
O=R/'output/veld-south-sofa-fall-diagnostic-v1'
rows=json.loads((O/'records.json').read_text(encoding='utf-8'));bindings={};boards=[]
for gear in ['bare','helmet']:
    names=[gear+'-living']+[r['name'] for r in rows if r['name'].startswith(gear)]
    board=Image.new('RGB',(len(names)*180,340),'#202a30');d=ImageDraw.Draw(board)
    for col,name in enumerate(names):
        source=O/(name+'-source.png');native=O/(name+'-room.png')
        for p in [source,native]:bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
        im=Image.open(source).convert('RGBA')
        if im.size==(184,184):
            padded=Image.new('RGBA',(256,256));padded.alpha_composite(im,(36,52));im=padded
        assert im.size==(256,256)
        im=im.resize((128,128),Image.Resampling.LANCZOS);board.paste(im,(col*180+26,20),im)
        board.paste(Image.open(native).convert('RGB').crop((490,286,660,391)),(col*180+5,190))
        d.text((col*180+5,3),name,fill='white')
    d.text((5,317),'Actual actor mortality API; normal loader; visual diagnosis, not accepted fall motion',fill='white')
    file=P/(gear+'-diagnostic.png');board.save(file);boards.append(file.name)
(P/'review-evidence.json').write_text(json.dumps({'scope':'two prescribed actor-level deaths at actual default South sofa contact; normal loader; no world roster kill, hazard cadence or Continue proof','boards':boards,'records':rows,'bindings':bindings,'visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'boards':len(boards),'nativeSourcePairs':len(bindings)//2,'specialisedRecipes':sum(bool(r['recipe']) for r in rows)}))
