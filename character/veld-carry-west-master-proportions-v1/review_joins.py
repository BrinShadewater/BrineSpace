from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
d=json.loads((R/'character/veld-animation-coverage-audit-v1/selected-library.json').read_text(encoding='utf-8'))
board=Image.new('RGB',(1536,584),'#202a30');draw=ImageDraw.Draw(board);rows=[];bindings={}
specs=[('idle-west',0),('pickup-west',-1),('unload-west',0),('candidate-carry',1),('carry-turn-north-west',-1),('carry-turn-south-west',-1)]
for y,gear in enumerate(['bare','helmet']):
    for x,(state,index) in enumerate(specs):
        if state=='candidate-carry':
            relative=f'character/veld-carry-west-master-proportions-v1/frames/{gear}/{index:03}.png';pivot=[128,224]
        else:
            entry=d['resolved'][gear][state];relative=entry['frameFiles'][index];pivot=entry['pivot'];assert entry['standingHeight']==148
            assert hashlib.sha256((R/relative).read_bytes()).hexdigest()==d['sourceBindings'][relative]
        path=R/relative;bindings[relative]=hashlib.sha256(path.read_bytes()).hexdigest()
        im=Image.open(path).convert('RGBA');board.paste(im,(x*256+128-round(pivot[0]),y*292+24+224-round(pivot[1])),im)
        draw.text((x*256+4,y*292+4),gear+' '+state+' '+str(index),fill='white')
        rows.append({'gear':gear,'state':state,'index':index,'source':relative,'pivot':pivot})
board.save(P/'cargo-join-review.png')
(P/'join-review-evidence.json').write_text(json.dumps({'rows':rows,'bindings':bindings,'visualReview':'pending','scope':'12 source comparisons atH148/p128224review padding only; actual normal selected idle/pickup/unload/turn endpoints vs candidate carry near contact. Different gait/contact poses are intentional. Not actual controller joins/world acceptance.'},indent=2)+'\n',encoding='utf-8')
print('12pivot-registered selected/candidate cargo presentations')
