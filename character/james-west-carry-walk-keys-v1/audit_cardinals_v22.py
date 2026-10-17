from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];out=r/'character/james-full-set-review-2026-10-02/cardinals-v22';out.mkdir(exist_ok=True)
inventory=r/'character/james-full-set-review-2026-10-02/source-inventory.json';d=json.loads(inventory.read_bytes());records=[];files=[inventory,Path(__file__)]
for direction in ('south','north','east','west'):
    board=Image.new('RGBA',(1024,1128),(48,59,63,255));draw=ImageDraw.Draw(board)
    master=d['states']['bare']['idle-'+direction]
    for row,family in enumerate(('idle','walk','repair','inspect')):
        state=d['states']['bare'][family+'-'+direction];n=state['frameCount']
        sources=[(master,0,'idle reference')]+[(state,i,f'{family} {i}/{n-1}') for i in (0,n//2,n-1)]
        for col,(s,i,label) in enumerate(sources):
            f=r/s['frameFiles'][i];im=Image.open(f).convert('RGBA');files.append(f)
            assert s['standingHeight']==148
            px,py=s['pivot'];assert px==int(px) and py==int(py)
            tile=Image.new('RGBA',(256,256));tile.paste(im,(128-int(px),224-int(py)))
            board.alpha_composite(tile,(col*256,row*282+26));draw.text((col*256+4,row*282+7),label,fill='white')
            records.append(dict(direction=direction,family=family,column=col,slot=i,source=f.relative_to(r).as_posix(),pivot=s['pivot'],standingHeight=148))
    board.convert('RGB').save(out/f'bare-{direction}.png')
(out/'review.json').write_text(json.dumps(dict(records=records,sourceSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)},
    visualReviewPending=True,sourceAcceptance=False,scope='Primary normal bare source first/middle/last per action and same-direction idle0 at exact pivot148 ruler. Static64 displayed slots,48 distinct phase selections; no full-cycle, gear, rooms or scheduler acceptance.'),indent=2)+'\n')
print('Four normal bare cardinal action boards prepared at fixed pivot/ruler; no artwork changed.')
