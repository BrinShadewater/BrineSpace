from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
d=json.loads((P/'selected-library.json').read_text(encoding='utf-8'));bindings={};rows=[]
for gear in ['bare','helmet']:
    board=Image.new('RGB',(1536,1168),'#202a30');draw=ImageDraw.Draw(board)
    for y,direction in enumerate(['east','west','north','south']):
        specs=[('idle-'+direction,0),('sit-down-'+direction,0),('sit-down-'+direction,'mid'),('sit-down-'+direction,-1),('sit-idle-'+direction,0),('read-seated-'+direction,'mid')]
        for x,(state,index) in enumerate(specs):
            entry=d['resolved'][gear][state];files=entry['frameFiles'];idx=len(files)//2 if index=='mid' else index%len(files)
            path=R/files[idx];raw=path.read_bytes();bindings[files[idx]]=hashlib.sha256(raw).hexdigest()
            im=Image.open(path).convert('RGBA');scale=148/entry['standingHeight']
            assert scale==1,'Current inspected rows share H148; avoid invented per-pose scale'
            px,py=entry['pivot'];ox=x*256+128-round(px);oy=y*292+28+224-round(py)
            board.paste(im,(ox,oy),im)
            draw.text((x*256+5,y*292+4),state+' / '+str(idx),fill='white')
            rows.append({'gear':gear,'state':state,'index':idx,'manifest':entry['manifest'],'source':files[idx],'reviewPaddingOnly':[128-round(px),224-round(py)]})
    board.save(P/(gear+'-selected-furniture-review.png'))
(P/'furniture-review-evidence.json').write_text(json.dumps({'scope':'48 current selected source presentations at same H148/p128224 review padding; no artwork mutation, native room/material acceptance or continuous playback inferred','rows':rows,'bindings':bindings,'visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
print('48exact selected source presentations, unchanged shared standing-height ruler')
