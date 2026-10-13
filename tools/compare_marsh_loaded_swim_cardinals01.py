"""Four staged cardinal loops with own current masters; no linked-state admission."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1';O=B/'cardinal01-cross-review';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
for n in json.loads(cat.read_text())['body']:
    p=resolve(cat,n)
    for state in json.loads(p.read_text())['states']:selected[state['id']]=(p,state)
parity={};states=[];masters={}
for pair in [[('north','04'),('south','01')],[('east','02'),('west','01')]]:
    board=Image.new('RGB',(1344,476),'#293b40');d=ImageDraw.Draw(board)
    for row,(f,r) in enumerate(pair):
        folder=B/f'{f}-loop-{r}-unselected';p,state=selected[f'idle-{f}'];master=resolve(p,state['frameFiles'][0])
        masters[f]=master.relative_to(ROOT).as_posix()
        paths=[folder/f'{i:03}.png' for i in range(4)]+[folder/'ruler.png',master]
        for col,p in enumerate(paths):
            im=Image.open(p).convert('RGBA');board.paste(im,(col*224,row*238+25),im)
            d.text((col*224+4,row*238+5),f+' '+r+' / '+('whole '+str(col) if col<4 else 'neutral' if col==4 else 'current master'),fill='white')
            parity[p.relative_to(ROOT).as_posix()]=sha(p)
        states.extend(json.loads((folder/'manifest.json').read_text())['states'])
    board.save(O/f'{pair[0][0]}-{pair[1][0]}-comparison.png')
manifest={'revision':'marsh-loaded-swim-cardinal01-staged','normalAdmission':False,'frameWidth':224,'frameHeight':208,'pivot':[112,172],'standingHeight':148,'textureFilter':'nearest','states':states}
(O/'family-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(O/'verification.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'uniqueWholeFigures':24,'states':4,'timingSlots':24,'authoredSwimmingFigures':16,'boards':2,'selectedMasters':masters,'sourceParity':parity,'scope':'Four staged loaded loops only. Linked water turns/pickup/drain, normal admission/world/persistence/contact remain pending.'},indent=2)+'\n')
print('Four staged loops,16drawings/24slots,24whole figures; linked water family remains pending.')
