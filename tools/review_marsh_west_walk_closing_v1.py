"""Show a fixed-pivot closing sequence at native and station display density."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-west-walk-family-contact-v1/motion-review'
INV=ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-east-walk/inventory.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inv=json.loads(INV.read_text());reg=json.loads((OUT.parent/'registration.json').read_text())
for e in inv['states']['walk-west']['frames']:assert sha(ROOT/e['path'])==e['sha256']
for e in reg['records']:assert sha(ROOT/e['path'])==e['sha256']
seq=[5,0,1,2,3,4,5,0]
board=Image.new('RGB',(8*184,3*214),'#293b40');d=ImageDraw.Draw(board)
for row,label in enumerate(['Original','Revision','Station density / revision']):
    for col,slot in enumerate(seq):
        p=ROOT/inv['states']['walk-west']['frames'][slot]['path'] if row==0 else OUT.parent/f'{slot:03}.png'
        im=Image.open(p).convert('RGBA')
        if row==2:
            z=65.28/148;im=im.resize((round(184*z),round(184*z)),Image.Resampling.LANCZOS)
            xy=(col*184+round(92-92*z),row*214+25+round(172-172*z))
        else:xy=(col*184,row*214+25)
        board.paste(im,xy,im);d.text((col*184+3,row*214+3),f'{label} /{slot}',fill='white')
p=OUT/'closing-join-board.png';board.save(p)
(OUT/'closing-review.json').write_text(json.dumps({'sequence':seq,'boardSha256':sha(p),'sourceRegistrationSha256':sha(OUT.parent/'registration.json'),'inventorySha256':sha(INV),'scale':65.28/148,'method':'Whole original square canvas, common92/172pivot, no pose bound fitting; fixed station density65.28/148. Held ordered sequence, not continuous watched animation.','reviewed':False},indent=2)+'\n')
print('Closing5/0and half-cycle complete ordered source/station board prepared with exact input hashes.')
