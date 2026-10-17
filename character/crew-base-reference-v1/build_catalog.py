from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;R=P.parent.parent;P.mkdir(exist_ok=True)
BG='#272b2e';families=[('Bill','bill','character/crew-runtime-matte-v1/bill/manifest.json'),('Veld','veld','character/crew-runtime-matte-v1/veld/manifest.json'),('James (Branforth)','branforth','character/crew-runtime-matte-v1/branforth/manifest.json'),('Marsh','marsh',None)]
directions=['south','east','north','west'];hashes={};records=[];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read_json(p):
    hashes[p.relative_to(R).as_posix()]=sha(p);return json.loads(p.read_text())
active=read_json(R/'character/ACTIVE_ASSETS.json')
families=[(name,key,active['locomotionOverrides'][key] if key!='marsh' else None) for name,key,_ in families]
regular=R/'assets/fonts/BarlowSemiCondensed-Regular.ttf';bold=R/'assets/fonts/BarlowSemiCondensed-SemiBold.ttf';font=lambda n,b=False:ImageFont.truetype(str(bold if b else regular),n)
sheet=Image.new('RGBA',(1640,1770),BG);draw=ImageDraw.Draw(sheet);draw.text((30,18),'BRINESPACE / REUSABLE CREW BODY FAMILIES',font=font(38,True),fill='white');draw.text((30,66),'Bill / Veld / James / Marsh  |  original source appearance  |  common physical registration',font=font(25),fill='#bdcdd0')
for row,(name,key,path) in enumerate(families):
    candidates={}
    if path:
        mp=R/path;m=read_json(mp)
        candidates={s['id']:(mp,m,s) for s in m['states'] if s['id'].startswith(('idle-','walk-'))}
    else:
        root=R/'character/marsh-v2';catalog=read_json(root/'catalog.json')
        for relative in catalog['body']:
            mp=(root/relative).resolve();m=read_json(mp)
            for state in m['states']:
                if state['id'].startswith(('idle-','walk-')):candidates[state['id']]=(mp,m,state)
    y=115+row*390;draw.text((30,y),name.upper()+(' / ANDROID BODY' if key=='marsh' else ''),font=font(29,True),fill='white')
    for col,direction in enumerate(directions):
        state_id='idle-'+direction;mp,m,state=candidates[state_id];source=(mp.parent/state['frameFiles'][0]).resolve();hashes[source.relative_to(R).as_posix()]=sha(source);art=Image.open(source).convert('RGBA');assert art.size==(184,184),'Unexpected standing canvas'
        pivot=state.get('pivot',m['pivot']);standing=m.get('standingHeight',148);assert pivot==[92,172] and standing==148,'Unexpected standing registration'
        xy=(col*400+24,y+35);large=art.resize((368,368),Image.Resampling.NEAREST);sheet.alpha_composite(large,xy)
        draw.text((col*400+40,y+360),direction.upper(),font=font(23),fill='white')
        pixels=np.array(art);mask=pixels[:,:,3]>180;ys,xs=np.where(mask);body=mask.copy();body[:60]=False;by,bx=np.where(body)
        walk=candidates.get('walk-'+direction);walk_info=None if walk is None else {'manifest':walk[0].relative_to(R).as_posix(),'frames':len(walk[2]['frameFiles']),'cycleMs':sum(walk[2]['frameDurationsMs'])}
        records.append({'family':key,'displayName':name,'direction':direction,'manifest':mp.relative_to(R).as_posix(),'source':source.relative_to(R).as_posix(),'canvas':list(art.size),'pivot':pivot,'standingHeight':standing,'idleFrames':len(state['frameFiles']),'idleCycleMs':sum(state['frameDurationsMs']),'walk':walk_info,'opaqueBounds':[int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1],'bodyBoundsBelowRow60':[int(bx.min()),int(by.min()),int(bx.max())+1,int(by.max())+1],'tileXY':list(xy),'tileSize':[368,368]})
draw.text((30,1690),'Each tile uses the same 2x nearest enlargement. Source canvas 184 x 184 / foot (92,172) / standing ruler 148 px.',font=font(23),fill='#bdcdd0')
draw.text((30,1728),'Human rows: declared matte locomotion sources. Marsh: final idle entries from ordered selected catalog. No art modified.',font=font(22),fill='#bdcdd0')
sheet.convert('RGB').save(P/'base-family-comparison.png')
metadata={'scope':'Source model reference catalog, not new derivatives or proof of cross-family head/action compatibility.','humanSelection':'ACTIVE_ASSETS locomotionOverrides (declared base locomotion; later action overrides remain separate)','marshSelection':'Last matching state in selected marsh-v2 catalog.body order','records':records,'sourceHashes':hashes,'reusePolicy':['Bill reuse demonstrated by Krusher candidate','Veld is owner-suggested default for female characters, with actual likeness/build governing selection','James and Marsh remain independent proposed families requiring their own head/tint/equipment checks','Preserve each selected source clock and state count; do not force uniform animation counts','Keep original heads and department colours in the reference sheet; no runtime selections changed']}
(P/'catalog.json').write_text(json.dumps(metadata,indent=2)+'\n');print(json.dumps({'families':4,'views':len(records),'inputs':len(hashes)}))
