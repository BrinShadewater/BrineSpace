"""Sample current dry/water joins without changing scale, palette or selection."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
raw=(P/'selected-library.json').read_bytes();d=json.loads(raw)
rows=[];bindings={};boards=[]
for direction in ['east','west','north','south']:
    board=Image.new('RGB',(1280,1184),'#202a30');draw=ImageDraw.Draw(board)
    for gi,gear in enumerate(['bare','helmet']):
        for phase in range(2):
            y=(gi*2+phase)*296
            for x,action in enumerate(['idle','carry','swim','swim-carry','death-water']):
                state=action+'-'+direction;entry=d['resolved'][gear][state]
                assert entry['standingHeight']==148, (state,entry['standingHeight'])
                index=0 if phase==0 else len(entry['frameFiles'])//2
                relative=entry['frameFiles'][index];path=R/relative
                digest=hashlib.sha256(path.read_bytes()).hexdigest()
                assert digest==d['sourceBindings'][relative],relative
                bindings[relative]=digest
                im=Image.open(path).convert('RGBA');px,py=entry['pivot']
                ox=x*256+128-round(px);oy=y+24+224-round(py)
                board.paste(im,(ox,oy),im)
                draw.text((x*256+5,y+4),gear+' '+state+' / '+str(index),fill='white')
                rows.append({'gear':gear,'state':state,'index':index,'source':relative,
                    'manifest':entry['manifest'],'pivot':entry['pivot'],
                    'frameSize':entry['frameSize'],'reviewPaddingOnly':[128-round(px),224-round(py)]})
    filename=direction+'-cross-family-source-review.png';board.save(P/filename);boards.append(filename)
evidence={'boards':boards,'rows':rows,'bindings':bindings,
    'inventorySHA256':hashlib.sha256(raw).hexdigest(),'visualReview':'pending',
    'scope':'80 current selected source presentations: first/middle dry idle/carry and water swim/swim-carry/fall, all cardinals/both gears. Fixed H148, pivot translation only, exact original colour. Sampling can find defects; cannot establish full-frame motion, native appearance, controller handoffs or full-library acceptance.'}
(P/'cross-family-review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
print('4 boards / 80 source presentations; same H148 ruler, no artwork mutation')
