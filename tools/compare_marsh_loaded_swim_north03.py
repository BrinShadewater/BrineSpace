"""Compare whole North03 against each staged side and their own masters."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1';O=B/'north-loop-03-cross-review';O.mkdir(exist_ok=True)
parity={}
for side,rev in [('east','02'),('west','01')]:
    board=Image.new('RGB',(1344,476),'#293b40');d=ImageDraw.Draw(board)
    for row,(f,r) in enumerate([('north','03'),(side,rev)]):
        folder=B/f'{f}-loop-{r}-unselected'
        paths=[folder/f'{i:03}.png' for i in range(4)]+[folder/'ruler.png',ROOT/f'character/marsh-v2/frames/bare/idle-{f}/000.png']
        for col,p in enumerate(paths):
            im=Image.open(p).convert('RGBA');board.paste(im,(col*224,row*238+25),im)
            d.text((col*224+4,row*238+5),f+' / '+('whole '+str(col) if col<4 else 'neutral' if col==4 else 'own master'),fill='white')
            parity[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    board.save(O/f'north-{side}-comparison.png')
(O/'verification.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'uniqueWholeFigures':18,'boards':2,'sourceParity':parity,'scope':'Four whole swimmers per direction and three own neutrals/masters. Not a joined water family or world acceptance.'},indent=2)+'\n')
print('Two whole-source boards / 18 unique figures prepared.')
