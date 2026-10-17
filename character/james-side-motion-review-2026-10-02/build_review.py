from pathlib import Path
from PIL import Image,ImageDraw
import json,re,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];P.mkdir(exist_ok=True)
text=(R/'scripts/grid_canvas.gd').read_text();start=text.index('elif actor == "branforth":');block=text[start:text.index('\nfunc ',start)]
C=R/'character/chief-engineer-branforth-v2';catalog=json.loads((C/'catalog.json').read_bytes());selected={'bare':{},'helmet':{}};inputs={}
def freeze(p):inputs[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
def add(path,mode):
    freeze(path);pack=json.loads(path.read_bytes())
    for state in pack['states']:selected[mode][state['id']]=(path,pack,state)
for field,mode in [('body','bare'),('equipment','helmet')]:
    for rel in catalog[field]:add(C/rel,mode)
for kind,rel in re.findall(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet",\s*)?"res://([^"]+)"',block):add(R/rel,'bare' if kind=='load_manifest' else 'helmet')
for p in [R/'scripts/grid_canvas.gd',R/'character/ACTIVE_ASSETS.json',C/'catalog.json']:freeze(p)
records=[];banks=[]
def load(mode,key,i):
    path,pack,state=selected[mode][key];rel=state['frameFiles'][i]
    file=R/rel.removeprefix('res://') if rel.startswith('res://') else (path.parent/rel).resolve();freeze(file)
    im=Image.open(file).convert('RGBA');assert float(pack['standingHeight'])==148, (key,pack['standingHeight'])
    canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,(round(128-pack['pivot'][0]),round(224-pack['pivot'][1])))
    return canvas,file
for mode in ['bare','helmet']:
    for key in ['carry-east','carry-west','pickup-east','pickup-west','unload-east','unload-west','inspect-west']:
        path,pack,state=selected[mode][key];direction=key.rsplit('-',1)[1];master,_=load(mode,'idle-'+direction,0)
        frames=[load(mode,key,i)[0] for i in range(len(state['frameFiles']))]
        pages=[]
        for page in range((len(frames)+15)//16):
            board=Image.new('RGB',(1280,1120),'#303b40');draw=ImageDraw.Draw(board)
            for row in range(4):
                at=(0,row*280+24);board.paste(master,at,master);draw.text((4,at[1]-20),mode+' '+direction+' master',fill='white')
                for col in range(4):
                    i=page*16+row*4+col
                    if i>=len(frames):continue
                    at=((col+1)*256,row*280+24);board.paste(frames[i],at,frames[i]);draw.text((at[0]+4,at[1]-20),key+' '+str(i),fill='white')
            name=mode+'-'+key+'-'+str(page)+'.png';board.save(P/name);pages.append(name)
        # Clock preview contains each source slot, with master beside it.
        preview=[]
        for frame in frames:
            board=Image.new('RGB',(512,280),'#303b40');board.paste(master,(0,24),master);board.paste(frame,(256,24),frame)
            ImageDraw.Draw(board).text((4,4),mode+' '+key+' / master | action',fill='white');preview.append(board)
        durations=state.get('frameDurationsMs',[100]*len(frames))
        preview[0].save(P/(mode+'-'+key+'.gif'),save_all=True,append_images=preview[1:],duration=durations,loop=0,optimize=False)
        banks.append({'gear':mode,'key':key,'manifest':path.relative_to(R).as_posix(),'slots':len(frames),'pages':pages,'durationMs':sum(durations),'loop':state['loop']})
(P/'selected-banks.json').write_text(json.dumps({'banks':banks,'scope':'Complete selected source slots for side carry/pickup/unload and West inspection, both gears. Exact148 ruler with pivot registration; no source rescale or edits. Constructed source-clock previews, not runtime task-chain proof.'},indent=2))
(P/'inputs-before.json').write_text(json.dumps(inputs,indent=2))
print(json.dumps({'banks':len(banks),'slots':sum(b['slots'] for b in banks),'boards':sum(len(b['pages']) for b in banks),'frozenInputs':len(inputs)}))
