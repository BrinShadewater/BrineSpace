from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;R=P.parents[1];audit=json.loads((P/'east-turn-join-review.json').read_bytes());pack=json.loads((P/'east-turn-v3-bare-manifest.json').read_bytes());master_path=R/'character/crew-runtime-matte-v1/branforth/manifest.json';masters=json.loads(master_path.read_bytes());checks=0;pages=[]
def master(direction):
    state=next(s for s in masters['states'] if s['id']=='idle-'+direction);im=Image.open(master_path.parent/state['frameFiles'][0]).convert('RGBA');out=Image.new('RGBA',(256,256));out.alpha_composite(im,(round(128-masters['pivot'][0]),round(224-masters['pivot'][1])));return out
for state in pack['states']:
    bank=next(r for r in audit['records'] if r['gear']=='bare' and r['state']==state['id']);op=R/bank['manifest'];original_pack=json.loads(op.read_bytes());old=next(s for s in original_pack['states'] if s['id']==state['id'])
    for k in old:
        if k not in ['frameFiles','provenance']:assert old[k]==state[k];checks+=1
    a,b=state['id'].split('-')[2:];m=[master(a),master(b)];east=Image.open(P/'east-family-v2/carry-east-000.png').convert('RGBA');preview=[]
    for page in range((len(state['frameFiles'])+5)//6):
        board=Image.new('RGB',(1280,1680),'#303b40');draw=ImageDraw.Draw(board)
        for row in range(6):
            i=page*6+row
            if i>=len(state['frameFiles']):break
            images=[m[0],Image.open(op.parent/old['frameFiles'][i]).convert('RGBA'),Image.open(P/state['frameFiles'][i]).convert('RGBA'),m[1],east]
            for col,im in enumerate(images):
                board.paste(im,(col*256,row*280+24),im);draw.text((col*256+4,row*280+4),[a+' master','original','candidate',b+' master','revised East carry'][col]+' / '+str(i),fill='white')
            preview.append(board.crop((0,row*280,1280,(row+1)*280)))
        name='turn-v3-'+state['id']+'-'+str(page)+'.png';board.save(P/name);pages.append(name)
    preview[0].save(P/('turn-v3-'+state['id']+'.gif'),save_all=True,append_images=preview[1:],duration=state['frameDurationsMs'],loop=0,optimize=False)
(P/'turn-v3-source-review.json').write_text(json.dumps({'metadataChecks':checks,'failures':0,'pages':pages,'slots':46,'scope':'All bare turn slots beside both directional masters, original turn and staged East carry. Constructed source-clock GIFs; no native actor/task motion claim.'},indent=2))
print(json.dumps({'metadataChecks':checks,'sourceSlots':46,'boards':len(pages)}))
