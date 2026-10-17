"""Current ordered James selections, registered family comparison (source review)."""
from pathlib import Path
import re,json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];P.mkdir(exist_ok=True)
text=(R/'scripts/grid_canvas.gd').read_text();start=text.index('elif actor == "branforth":');block=text[start:text.index('\nfunc ',start)]
C=R/'character/chief-engineer-branforth-v2';catalog=json.loads((C/'catalog.json').read_bytes());selected={'bare':{},'helmet':{}}
inputs={}
def freeze(p):inputs[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
def add(path,mode):
    freeze(path);pack=json.loads(path.read_bytes())
    for state in pack['states']:selected[mode][state['id']]=(path,pack,state)
for field,mode in [('body','bare'),('equipment','helmet')]:
    for rel in catalog[field]:add(C/rel,mode)
for kind,rel in re.findall(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet",\s*)?"res://([^"]+)"',block):add(R/rel,'bare' if kind=='load_manifest' else 'helmet')
freeze(R/'scripts/grid_canvas.gd');freeze(C/'catalog.json');freeze(R/'character/ACTIVE_ASSETS.json')
(P/'current-selection.json').write_text(json.dumps({m:{k:{'manifest':p.relative_to(R).as_posix(),'slots':len(s['frameFiles']),'standingHeight':d['standingHeight'],'pivot':d['pivot']} for k,(p,d,s) in states.items()} for m,states in selected.items()},indent=2))
groups={'movement':['idle','walk','carry','pickup','unload','interact'], 'work':['inspect','kneel','repair','stand','torch-draw','weld','torch-stow']}
print('Current selected states:',{m:len(v) for m,v in selected.items()})
print('Available cardinal families:',sorted({k.rsplit('-',1)[0] for k in selected['bare'] if k.endswith('-east')}))
records=[]
def load(mode,key,index):
    path,pack,state=selected[mode][key];rel=state['frameFiles'][index]
    file=R/rel.removeprefix('res://') if rel.startswith('res://') else (path.parent/rel).resolve();freeze(file)
    im=Image.open(file).convert('RGBA');factor=148/float(pack['standingHeight'])
    scaled=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS) if factor!=1 else im
    registered=Image.new('RGBA',(256,256));shift=(round(128-pack['pivot'][0]*factor),round(224-pack['pivot'][1]*factor))
    registered.alpha_composite(scaled,shift)
    bounds=im.getchannel('A').getbbox()
    records.append({'gear':mode,'key':key,'index':index,'source':file.relative_to(R).as_posix(),'standingHeight':pack['standingHeight'],'registrationFactor':factor,'sourceBounds':bounds,'visibleHeightAt148':(bounds[3]-bounds[1])*factor if bounds else 0})
    return registered
for direction in ['north','east','south','west']:
 for mode in ['bare','helmet']:
  for group,families in groups.items():
    rows=[a for a in families if a+'-'+direction in selected[mode]]
    board=Image.new('RGB',(4*256,len(rows)*280),'#303b40');draw=ImageDraw.Draw(board)
    for row,action in enumerate(rows):
        key=action+'-'+direction;state=selected[mode][key][2];indices=[0,len(state['frameFiles'])//2,len(state['frameFiles'])-1]
        for col,(k,i) in enumerate([('idle-'+direction,0),*[(key,i) for i in indices]]):
            im=load(mode,k,i);at=(col*256,row*280+24);board.paste(im,at,im)
            draw.text((at[0]+4,at[1]-20),('master' if col==0 else action+' '+str(i))+' / '+direction+' '+mode,fill='white')
    board.save(P/(direction+'-'+mode+'-'+group+'.png'))
(P/'sample-records.json').write_text(json.dumps({'scope':'13 primary dry families, four directions, both selected gears where present; first/middle/last source samples registered by pivot and documented standing ruler at148. Same-scale source presentation only, not runtime/furniture/motion acceptance; posed body/cargo extent is not standing height.','records':records},indent=2))
(P/'inputs-before.json').write_text(json.dumps(inputs,indent=2))
print(len(records),'registered source samples;16 family boards; frozen inputs',len(inputs))
