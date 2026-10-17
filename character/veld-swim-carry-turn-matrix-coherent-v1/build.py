"""Consolidate cargo quarters and derive original twelve-slot half turns."""
from pathlib import Path
import copy,json,hashlib,shutil
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1]
FAMILIES=['east-south','south-west','west-north','north-east']
ROUTES=[('east','south','west'),('west','south','east'),('north','east','south'),('south','east','north')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
provenance={};bindings={};count=0
for gear in ['bare','helmet']:
 lookup={};base=None
 for family in FAMILIES:
  folder=R/f'character/veld-swim-carry-turn-{family}-coherent-v1';m=json.loads((folder/f'{gear}-manifest.json').read_text());base=base or copy.deepcopy(m);proof=json.loads((folder/'packaging-checks.json').read_text());assert proof['failures']==0
  for s in m['states']:
   for f in s['frameFiles']:assert sha(folder/f)==proof['frameHashes'][f]
   lookup[s['id']]=(folder,s)
  bindings[family+'/'+gear]={f:sha(folder/f) for f in [f'{gear}-manifest.json','bare-fit-v1.json','helmet-fit-v1.json','source-provenance.json','packaging-checks.json','native-candidate-v1-checks.json','native-candidate-v1.log']}
 old=json.loads((R/f'character/dr-veld-v2/packs/{gear}-256x256-p128.0-128.0/manifest.json').read_text());original={s['id']:s for s in old['states']};out=copy.deepcopy(base);out.update(name='Veld coherent cargo swimming turn matrix '+gear,status=('installed_locally_pending_full_set_polish' if json.loads((R/'character/ACTIVE_ASSETS.json').read_text(encoding='utf-8'))['actionOverrides'].get('veld-water-cargo-turns')=='character/veld-swim-carry-turn-matrix-coherent-v1/bare-manifest.json' else 'staged_pending_full_motion_controller_world_review'),states=[])
 plans=[(key,[(folder,f) for f in s['frameFiles']],None) for key,(folder,s) in lookup.items()]
 for a,b,c in ROUTES:
  lf,left=lookup[f'swim-carry-turn-{a}-{b}'];rf,right=lookup[f'swim-carry-turn-{b}-{c}'];assert Image.open(lf/left['frameFiles'][-1]).tobytes()==Image.open(rf/right['frameFiles'][0]).tobytes()
  plans.append((f'swim-carry-turn-{a}-{c}',[(lf,f) for f in left['frameFiles']]+[(rf,f) for f in right['frameFiles']],[a,b,c]))
 for key,sources,route in plans:
  s=copy.deepcopy(original[key]);assert len(sources)==len(s['frameFiles']);s['frameFiles']=[];records=[]
  for i,(folder,p) in enumerate(sources):
   f=f'frames/{gear}/{key}/{i:03}.png';target=H/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(folder/p,target);s['frameFiles'].append(f);records.append(dict(file=f,source=(folder/p).relative_to(R).as_posix(),sha256=sha(target)))
  out['states'].append(s);provenance[gear+'/'+key]=dict(kind='derived paired quarter with original duplicate middle slots' if route else 'unchanged selected staged quarter',route=route,totalMs=sum(s['frameDurationsMs']),frames=records);count+=len(sources)
 (H/f'{gear}-manifest.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGBA',(12*256,4*280),'#202a30');draw=ImageDraw.Draw(board)
 for row,s in enumerate(out['states'][8:]):
  draw.text((4,row*280+4),s['id']+' original680ms / exact middle repeated slots5,6',fill='white')
  for i,f in enumerate(s['frameFiles']):board.alpha_composite(Image.open(H/f).convert('RGBA'),(i*256,row*280+24))
 board.save(H/f'{gear}-half-contact-v1.png')
(H/'provenance.json').write_text(json.dumps(dict(installed=out['status'].startswith('installed'),sourceFamilies=FAMILIES,sourceBindings=bindings,states=provenance),indent=2)+'\n',encoding='utf-8');print(f'24gearstates/{count}refs; original quarter800ms/half680ms contracts retained.')
