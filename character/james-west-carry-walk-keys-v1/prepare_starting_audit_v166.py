from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path('character/james-west-carry-walk-keys-v1');r=p.parents[1];o=p/'starting-source-audit-v166';o.mkdir(exist_ok=True);j=json.loads((p/'material-repair-progress.json').read_bytes());inputs={}
for phase in range(4):
    board=Image.new('RGBA',(1024,560),(47,58,63,255));draw=ImageDraw.Draw(board)
    for row,mode in enumerate(['bare','helmet']):
        source=p/f'master-head-review-v16/{mode}-{phase:03d}.png';candidate=r/j['states'][phase]['candidateSources'][mode]['file'];previous=p/f'local-material-phase48-v164/{mode}-head-protected.png'
        master=p/'../james-west-master-carry-v1/registered-original-master.png'
        for col,(label,f) in enumerate([('Original pose '+str(phase),source),('Current candidate '+str(phase),candidate),('Repaired48 neighbour',previous),('Registered master bare',master)]):
            im=Image.open(f).convert('RGBA');board.alpha_composite(im,(col*256,row*280+24));draw.text((col*256+4,row*280+5),label,fill='white');inputs[f.resolve().relative_to(r.resolve()).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
    board.save(o/f'phase-{phase:03d}-review.png')
(o/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
print('Four original/candidate/neighbour/master comparison boards prepared.')
