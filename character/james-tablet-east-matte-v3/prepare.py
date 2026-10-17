from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];P.mkdir(exist_ok=True)
S=R/'character/james-tablet-east-belt-fixed-source-v2';inputs={};refs=[]
def freeze(p):inputs[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
for mode in ['bare','helmet']:
    p=S/(mode+'-manifest.json');freeze(p);d=json.loads(p.read_bytes());s=next(s for s in d['states'] if s['id']=='inspect-east')
    for rel in s['frameFiles']:freeze((p.parent/rel).resolve())
    refs.append((mode,p,d,s))
masters={}
for mode,rel in [('bare','character/crew-runtime-matte-v1/branforth/manifest.json'),('helmet','character/james-shared-helmet-runtime-v1/manifest.json')]:
    p=R/rel;freeze(p);d=json.loads(p.read_bytes());s=next(s for s in d['states'] if s['id']=='idle-east');f=(p.parent/s['frameFiles'][0]).resolve();freeze(f);masters[mode]=Image.open(f).convert('RGBA')
target=Image.new('RGBA',(4*184,2*184));idx=[0,20,40,60,80,100,120,140]
path,pack,state=refs[0][1:]
for n,i in enumerate(idx):target.alpha_composite(Image.open((path.parent/state['frameFiles'][i]).resolve()).convert('RGBA'),((n%4)*184,(n//4)*184))
target.save(P/'material-edit-target.png')
master=Image.new('RGBA',(368,184));master.alpha_composite(masters['bare'],(0,0));master.alpha_composite(masters['helmet'],(184,0));master.save(P/'master-material-reference.png')
for rel in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json']:freeze(R/rel)
(P/'inputs-before.json').write_text(json.dumps(inputs,indent=2))
(P/'edit-layout.json').write_text(json.dumps({'target':'Eight sampled current bare poses, row-major184cells, transparent target atlas. Complete current141poses remain authoritative; sample edit is a material reference study only.','indices':idx,'masterReference':'Exact selected bare/helmet East idle0, no rescale.','wholeCycleFramesPerGear':141},indent=2))
print(len(inputs),'current inputs frozen; eight-pose material target and masters prepared.')
