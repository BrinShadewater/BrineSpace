from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
audit=json.loads((R/'character/bill-selected-source-audit-2026-10-01/source-inventory.json').read_text())['selectedStateSources']
board=Image.new('RGB',(1400,1680),(34,52,62));draw=ImageDraw.Draw(board);records=[]
for g,gear in enumerate(['bare','helmet']):
    for d,di in enumerate(['east','west','south','north']):
        y=(g*4+d)*210;s=audit[gear]['run-'+di]
        master=R/f'character/bill-seated-{"helmet-" if g else ""}{di}-coherent-v1/frames/sit-down-{di}/000.png'
        im=Image.open(master).convert('RGBA');board.paste(im,(100-128,y+190-224),im)
        draw.text((4,y+195),gear+' '+di,fill='white')
        for i,f in enumerate(s['sourceFiles']):
            a=Image.open(R/f[6:]).convert('RGBA');px,py=s['pivot'];board.paste(a,(300+i*200-px,y+190-py),a)
        records.append(dict(gear=gear,direction=di,source=s,master=master.relative_to(R).as_posix(),masterSha256=hashlib.sha256(master.read_bytes()).hexdigest(),sourceSha256={f:hashlib.sha256((R/f[6:]).read_bytes()).hexdigest() for f in s['sourceFiles']}))
board.save(P/'run-review.png')
(P/'source-review.json').write_text(json.dumps({'scale':'1:1 native pixels, shared declared148 anatomical density and foot baseline; no per-pose fit','rows':records},indent=2)+'\n')
print('8 fixed-density run/master rows')
