"""Same-ruler current South transition, ground and sofa reference comparison."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];A=R/'character/veld-sofa-partial-south-audit-v1';A.mkdir(exist_ok=True)
bindings={};identities={}
for gear in ['bare','helmet']:
    seating=json.loads((R/f'character/veld-seated-south-selected-v1/{gear}-manifest.json').read_text())
    sit=next(s for s in seating['states'] if s['id']=='sit-down-south')['frameFiles']
    neutral=json.loads((P/f'{gear}-manifest.json').read_text())['states'][1]['frameFiles']
    ground=[f'res://character/veld-death-ground-south-coherent-v1/frames/{gear}/death-ground-south/{i:03}.png' for i in range(6)]
    board=Image.new('RGB',(1536,884),'#202a30');d=ImageDraw.Draw(board)
    sets=[('Selected sit-down (rise reverses)',sit),('Retained ground candidate',ground),('Normally selected neutral sofa fall',neutral)]
    padded=[]
    for row,(label,files) in enumerate(sets):
        group=[]
        for col,path in enumerate(files):
            file=R/path.removeprefix('res://');im=Image.open(file).convert('RGBA');canvas=Image.new('RGBA',(256,272));canvas.alpha_composite(im)
            board.paste(canvas,(col*256,row*294+20),canvas);d.text((col*256+5,row*294+3),label+' '+str(col),fill='white')
            bindings[file.relative_to(R).as_posix()]=hashlib.sha256(file.read_bytes()).hexdigest();group.append(canvas)
        padded.append(group)
    identities[gear]={'selectedSit5EqualsNeutralFall0':padded[0][5].tobytes()==padded[2][0].tobytes(),'selectedSit0EqualsGround0':padded[0][0].tobytes()==padded[1][0].tobytes()}
    board.save(A/(gear+'-source-audit.png'))
(A/'source-bindings.json').write_text(json.dumps({'bindings':bindings,'identities':identities,'scope':'same canvas/pivot/ruler current sources; no current world death proof or new fall admission'},indent=2)+'\n',encoding='utf-8')
print(json.dumps(identities))
