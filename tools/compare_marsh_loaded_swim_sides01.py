"""Whole East/West figures and own masters; no mirrors or normal selection."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1';O=B/'side01-cross-review';O.mkdir(exist_ok=True)
board=Image.new('RGB',(1344,476),'#293b40');d=ImageDraw.Draw(board);states=[];parity=[]
for row,(f,rev) in enumerate([('east','02'),('west','01')]):
    folder=B/f'{f}-loop-{rev}-unselected'
    paths=[folder/f'{i:03}.png' for i in range(4)]+[folder/'ruler.png',ROOT/f'character/marsh-v2/frames/bare/idle-{f}/000.png']
    for col,p in enumerate(paths):
        im=Image.open(p).convert('RGBA');board.paste(im,(col*224,row*238+25),im)
        d.text((col*224+4,row*238+5),f+' / '+('whole '+str(col) if col<4 else 'neutral' if col==4 else 'own master'),fill='white')
        parity.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    states.extend(json.loads((folder/'manifest.json').read_text())['states'])
board.save(O/'whole-side-comparison.png')
(O/'family-manifest.json').write_text(json.dumps({'revision':'marsh-loaded-swim-side01-staged','frameWidth':224,'frameHeight':208,'pivot':[112,172],'standingHeight':148,'textureFilter':'nearest','states':states},indent=2)+'\n')
(O/'verification.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholeFigures':12,'states':2,'slots':12,'authoredSwimmingFigures':8,'sourceParity':parity,'scope':'Whole-source/cardinal neutral-master comparison. No linked water-family or normal admission acceptance.'},indent=2)+'\n')
print('12 complete figures, two staged side loops / 12 timing slots / 8 drawings; no normal admission.')
