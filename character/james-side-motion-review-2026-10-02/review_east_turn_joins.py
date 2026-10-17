from pathlib import Path
from PIL import Image, ImageDraw
import json,re,hashlib
P=Path(__file__).resolve().parent; R=P.parents[1]
text=(R/'scripts/grid_canvas.gd').read_text();start=text.index('elif actor == "branforth":');block=text[start:text.index('\nfunc ',start)]
C=R/'character/chief-engineer-branforth-v2'; catalog=json.loads((C/'catalog.json').read_bytes()); selected={'bare':{},'helmet':{}};inputs={}
def freeze(p): inputs[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
def add(path,mode):
    freeze(path);pack=json.loads(path.read_bytes())
    for state in pack['states']:selected[mode][state['id']]=(path,pack,state)
for field,mode in [('body','bare'),('equipment','helmet')]:
    for rel in catalog[field]:add(C/rel,mode)
for kind,rel in re.findall(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet",\s*)?"res://([^"]+)"',block):add(R/rel,'bare' if kind=='load_manifest' else 'helmet')
prior=json.loads((P/'selected-banks.json').read_bytes())['banks']
assert all(selected[b['gear']][b['key']][0].relative_to(R).as_posix()==b['manifest'] for b in prior)
candidate=json.loads((P/'east-family-v2-bare-manifest.json').read_bytes());candidate_state=next(s for s in candidate['states'] if s['id']=='carry-east')
def load(mode,key,i):
    path,pack,state=selected[mode][key];rel=state['frameFiles'][i];file=R/rel[6:] if rel.startswith('res://') else (path.parent/rel).resolve();freeze(file)
    im=Image.open(file).convert('RGBA');canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,(round(128-pack['pivot'][0]),round(224-pack['pivot'][1])))
    assert pack['standingHeight']==148
    return canvas,file
records=[]
for mode in ['bare','helmet']:
    keys=sorted(k for k in selected[mode] if k.startswith('carry-turn-') and 'east' in k.split('-')[2:])
    for key in keys:
        a,b=key.split('-')[2:];path,pack,state=selected[mode][key];frames=[load(mode,key,i)[0] for i in range(len(state['frameFiles']))]
        masters=[load(mode,'idle-'+d,0)[0] for d in [a,b]]
        carries=[load(mode,'carry-'+d,0)[0] for d in [a,b]]
        revised=Image.open(P/candidate_state['frameFiles'][0]).convert('RGBA') if mode=='bare' else load(mode,'carry-east',0)[0]
        pages=[]
        for page in range((len(frames)+5)//6):
            board=Image.new('RGB',(1536,840),'#303b40');draw=ImageDraw.Draw(board)
            anchors=[masters[0],carries[0],revised,carries[1],masters[1]]
            labels=[a+' master',a+' carry 0','East revised carry 0',b+' carry 0',b+' master']
            for j,(im,label) in enumerate(zip(anchors,labels)):
                board.paste(im,(j*256,24),im);draw.text((j*256+4,4),label,fill='white')
            for j,im in enumerate(frames[page*6:page*6+6]):
                board.paste(im,(j*256,304),im);draw.text((j*256+4,284),key+' '+str(page*6+j),fill='white')
                crop=im.crop((96,56,192,120)).resize((288,192),Image.Resampling.NEAREST)
                board.paste(crop,(j*256,590),crop)
            name=mode+'-'+key+'-joins-'+str(page)+'.png';board.save(P/name);pages.append(name)
        records.append({'gear':mode,'state':key,'manifest':path.relative_to(R).as_posix(),'slots':len(frames),'durationMs':sum(state['frameDurationsMs']),'pages':pages})
for p in [R/'scripts/grid_canvas.gd',R/'character/ACTIVE_ASSETS.json']:freeze(p)
(P/'east-turn-join-inputs.json').write_text(json.dumps(inputs,indent=2))
(P/'east-turn-join-review.json').write_text(json.dumps({'records':records,'slots':sum(r['slots'] for r in records),'priorSideBanksSelectionUnchanged':True,'scope':'Current ordered dry East-connected carrying turns, every source slot beside both directional idle/carry anchors and staged East head; source review only, no runtime admission.'},indent=2))
print(json.dumps({'banks':len(records),'slots':sum(r['slots'] for r in records),'boards':sum(len(r['pages']) for r in records),'priorSideBanksSelectionUnchanged':True}))
