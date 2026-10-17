from pathlib import Path
from PIL import Image,ImageDraw
import json,os,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/james-cargo-material-joined-v1'
bare=json.loads((P/'east-family-v2-bare-manifest.json').read_bytes());original=json.loads((S/'bare-manifest.json').read_bytes());helmet=json.loads((S/'helmet-manifest.json').read_bytes())
helmet['states']=[s for s in helmet['states'] if s['id'] in ['pickup-east','carry-east','unload-east']]
for state in helmet['states']:state['frameFiles']=[os.path.relpath((S/rel).resolve(),P).replace('\\','/') for rel in state['frameFiles']]
helmet['name']='James East cargo retained shared helmet pair for head family v2';helmet['status']='staged_existing_helmet_pair_turn_review_pending'
(P/'east-family-v2-helmet-manifest.json').write_text(json.dumps(helmet,indent=2))
masters=[]
for mode,path in [('bare',R/'character/crew-runtime-matte-v1/branforth/manifest.json'),('helmet',R/'character/james-shared-helmet-runtime-v1/manifest.json')]:
    pack=json.loads(path.read_bytes());state=next(s for s in pack['states'] if s['id']=='idle-east');im=Image.open((path.parent/state['frameFiles'][0]).resolve()).convert('RGBA');m=Image.new('RGBA',(256,256));m.alpha_composite(im,(round(128-pack['pivot'][0]),round(224-pack['pivot'][1])));masters.append(m)
checks=[];records=[]
for state in bare['states']:
    old=next(s for s in original['states'] if s['id']==state['id']);gear=next(s for s in helmet['states'] if s['id']==state['id'])
    checks.append({'name':state['id']+' clocks/count/loop','pass':all(old[k]==state[k] for k in ['id','frameCount','frameDurationsMs','loop'])})
    board=Image.new('RGB',(1280,1680),'#303b40');draw=ImageDraw.Draw(board);preview=[]
    for i in range(6):
        images=[masters[0],Image.open(S/old['frameFiles'][i]).convert('RGBA'),Image.open(P/state['frameFiles'][i]).convert('RGBA'),masters[1],Image.open(P/gear['frameFiles'][i]).convert('RGBA')]
        for col,im in enumerate(images):
            at=(col*256,i*280+24);board.paste(im,at,im);draw.text((col*256+4,i*280+4),['bare master','selected','bare candidate','helmet master','retained helmet'][col]+' / '+state['id']+' '+str(i),fill='white')
        frame=Image.new('RGB',(1280,280),'#303b40');frame.paste(board.crop((0,i*280,1280,(i+1)*280)));preview.append(frame)
        records.append({'key':state['id'],'index':i,'bare':state['frameFiles'][i],'helmet':gear['frameFiles'][i]})
    board.save(P/('family-v2-'+state['id']+'.png'))
    preview[0].save(P/('family-v2-'+state['id']+'.gif'),save_all=True,append_images=preview[1:],duration=state['frameDurationsMs'],loop=0,optimize=False)
for k in ['frameWidth','frameHeight','pivot','standingHeight','textureFilter','precomposed']:checks.append({'name':k,'pass':bare[k]==original[k]})
(P/'family-v2-package-review.json').write_text(json.dumps({'checks':checks,'failures':[c for c in checks if not c['pass']],'records':records,'selected':False,'scope':'18new bare and18retained helmet refs; old clocks/geometry checked; paired master/current/candidate source boards. No turn/native action acceptance.'},indent=2))
assert all(c['pass'] for c in checks)
print('Paired18+18source references packaged;9metadata/clock checks pass;3full-family boards.')
