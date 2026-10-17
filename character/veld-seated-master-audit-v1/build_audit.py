"""Selected seated rows at a common anatomical scale, no independent thumbnails."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
coverage=json.loads((R/'character/veld-consistency-audit-v2/coverage.json').read_text())
records=[];bindings={}
for gear in ['bare','helmet']:
    board=Image.new('RGBA',(1920,1080),'#202a30');draw=ImageDraw.Draw(board)
    for row,direction in enumerate(['east','south','west','north']):
        keys=['idle-'+direction,'sit-down-'+direction,'sit-idle-'+direction,'sit-rise-'+direction]
        samples=[]
        for key in keys:
            state=coverage['selected'][gear][key]
            slots=[0] if key.startswith('idle-') else ([0,2,5] if key.startswith('sit-idle-') else [0,1,2,3,4,5])
            records.append({'gear':gear,'state':key,'manifest':state['manifest'],'pivot':state['pivot'],'standingHeight':state['standingHeight'],'slots':slots,'files':[state['files'][i] for i in slots]})
            for slot in slots:samples.append((key,slot,state))
        draw.text((5,row*270+5),gear+' / '+direction+' (common H148 ruler)',fill='white')
        for col,(key,slot,state) in enumerate(samples):
            path=R/state['files'][slot];bindings[state['files'][slot]]=hashlib.sha256(path.read_bytes()).hexdigest()
            image=Image.open(path).convert('RGBA');scale=148/state['standingHeight']
            if scale!=1:image=image.resize((round(image.width*scale),round(image.height*scale)),Image.Resampling.LANCZOS)
            at=(col*120+60-round(state['pivot'][0]*scale),row*270+252-round(state['pivot'][1]*scale))
            board.alpha_composite(image,at)
            draw.text((col*120+4,row*270+26),key.removesuffix('-'+direction)+' '+str(slot),fill='#a3b7c2')
    board.convert('RGB').save(P/f'{gear}-selected.png')
result={'scope':'selected catalog/literal loader mapping; static seated source/master comparison at common H148, not live world or full-motion acceptance','coverageSha256':hashlib.sha256((R/'character/veld-consistency-audit-v2/coverage.json').read_bytes()).hexdigest(),'rows':records,'bindings':bindings}
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'rows':len(records),'boundFrames':len(bindings),'boards':2}))
