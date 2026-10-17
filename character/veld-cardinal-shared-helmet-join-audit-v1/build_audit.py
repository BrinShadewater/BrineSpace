from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
R=P.parents[1]
Q=R/'character/veld-helmet-original-turntable-west-v1'
turns={'north':'north-east','east':'east-south','south':'south-west','west':'west-north'}
rows=[]; bindings={}; checks=0
def load(folder,gear):
    path=R/'character'/folder/f'{gear}-manifest.json'
    bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    states=json.loads(path.read_text())['states']
    for state in states:
        state['frameFiles']=[ref if ref.startswith('res://') else 'res://'+(path.parent/ref).relative_to(R).as_posix() for ref in state['frameFiles']]
    return {s['id']:s for s in states}
for direction in turns:
    board=Image.new('RGB',(1280,1000),'#202a30'); draw=ImageDraw.Draw(board)
    for gi,gear in enumerate(['bare','helmet']):
        cargo=load('veld-cargo-'+direction+'-master-family-v1',gear)
        start=load('veld-carry-'+direction+'-start-master-v1',gear)
        gait=load('veld-carry-'+direction+'-master-proportions-v1'+('/paired-package-v1' if direction=='east' else ''),gear)
        turn=load(Q.name,gear)
        if direction=='south':
            original=load('veld-idle-south-original-master-v1',gear)
            cargo=original; start=original
            # The South material package has separate gait manifests.
            gpath=R/'character/veld-south-material-master-v2'/f'gait-{gear}-manifest.json'
            bindings[gpath.relative_to(R).as_posix()]=hashlib.sha256(gpath.read_bytes()).hexdigest()
            gait={s['id']:s for s in json.loads(gpath.read_text())['states']}
        sources=[('Standing',cargo['unload-'+direction]['frameFiles'][-1]),
                 ('Held case',cargo['pickup-'+direction]['frameFiles'][-1]),
                 ('Start pose',start['carry-start-'+direction]['frameFiles'][0]),
                 ('Gait contact',gait['carry-'+direction]['frameFiles'][0]),
                 ('Shared turn',turn['carry-turn-'+turns[direction]]['frameFiles'][0])]
        images=[]
        for col,(name,ref) in enumerate(sources):
            path=R/ref[6:]; im=Image.open(path).convert('RGBA'); assert im.size==(256,256); checks+=1
            bindings[ref]=hashlib.sha256(path.read_bytes()).hexdigest(); images.append(im)
            x=col*256;y=gi*500
            draw.text((x+5,y+5),direction+' / '+gear+' / '+name,fill='white')
            board.paste(im,(x,y+25),im)
            detail=im.crop((96,60,160,120)).resize((192,180),Image.Resampling.NEAREST)
            board.paste(detail,(x+32,y+300),detail)
            a=np.asarray(im);ys,xs=np.where(a[:,:,3]>200)
            hy,hx=np.where(a[60:120,96:160,3]>200)
            rows.append({'direction':direction,'gear':gear,'role':name,'source':ref,
                         'opaqueBodyBox':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
                         'headRegionBox':[int(hx.min()+96),int(hy.min()+60),int(hx.max()+97),int(hy.max()+61)],
                         'headRegionScope':'Includes collar; not a helmet-only topology measurement.'})
        for i,name in [(2,'start-held'),(3,'gait-held'),(4,'turn-held')]:
            a=np.asarray(images[1]); b=np.asarray(images[i]); mask=np.any(a!=b,axis=2)
            head=mask[60:120,96:160]
            rows.append({'direction':direction,'gear':gear,'join':name,'wholeDifferentPixels':int(mask.sum()),
                         'headRegionDifferentPixels':int(head.sum()),'exact':not bool(mask.any()),
                         'scope':'Different body poses may be intended; values flag a comparison, not an art failure.'})
    board.save(P/f'{direction}-cardinal-joins.png')
(P/'audit.json').write_text(json.dumps({'scope':'Source-only cardinal endpoint comparison. No art edits, grade transforms, native integration or owner acceptance.', 'checks':checks,'rows':rows,'bindings':bindings},indent=2)+'\n')
print(f'{checks} source size checks; four paired boards and source bindings saved.')
