from pathlib import Path
import json,hashlib,re
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=0;hashes={}
for gear in ['bare','helmet']:
 m=json.loads((H/f'{gear}-manifest.json').read_text(encoding='utf-8'));old=json.loads((R/f'character/dr-veld-v2/packs/{gear}-256x256-p128.0-128.0/manifest.json').read_text());by={s['id']:s for s in m['states']}
 for s in m['states']:
  original=next(x for x in old['states'] if x['id']==s['id']);assert {k:v for k,v in s.items() if k!='frameFiles'}=={k:v for k,v in original.items() if k!='frameFiles'};checks+=1
  for f in s['frameFiles']:
   im=Image.open(H/f);assert im.mode=='RGBA' and im.size==(256,256);hashes[f]=sha(H/f);checks+=1
  start,end=s['id'].split('-')[3:]
  for i,d in [(0,start),(-1,end)]:
   assert Image.open(H/s['frameFiles'][i]).tobytes()==Image.open(R/f'character/veld-swim-carry-{d}-coherent-v1/frames/{gear}/swim-carry-{d}/000.png').tobytes();checks+=1
 assert all(Image.open(H/a).tobytes()==Image.open(H/b).tobytes() for a,b in zip(by['swim-carry-turn-east-south']['frameFiles'],reversed(by['swim-carry-turn-south-east']['frameFiles'])));checks+=1
 frames=[]
 for f in by['swim-carry-turn-east-south']['frameFiles']:
  bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(Image.open(H/f).convert('RGBA'));frames.append(bg.convert('RGB'))
 frames[0].save(H/f'{gear}-preview-v1.gif',save_all=True,append_images=frames[1:],duration=by['swim-carry-turn-east-south']['frameDurationsMs'],loop=0,disposal=2)
n=json.loads((H/'native-candidate-v1-checks.json').read_text());log=(H/'native-candidate-v1.log').read_text(encoding='utf-8');assert n['exit_code']==0 and n['engine_errors']==[] and n['real_profile_changed_files']==[] and '195 checks, 0 failures' in log;checks+=1
(H/'packaging-checks.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=False,frameHashes=hashes,nativeChecks=195,fixtureSha256=sha(R/'tools/review_veld_swim_carry_turn_east_south_v1.gd'),nativeLogSha256=sha(H/'native-candidate-v1.log'),sourceProvenanceSha256=sha(H/'source-provenance.json'),scope='Original800ms contracts/exact cargo endpoints/reverse/RGBA/current native candidate pixels; full motion and world acceptance separate'),indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Veld cargo east/south turn</title><style>body{background:#202a30;color:#e5ebed;font:16px sans-serif;margin:24px}img{max-width:100%}a{color:#8cc6e7}</style><h1>Veld — cargo east/south turn</h1><p>Staged800ms paired turn with exact cargo endpoints and corrected middle yaw. Forward preview; reverse uses the same authored poses in reverse order. Runtime unchanged; motion/world review remains.</p><img src="bare-preview-v1.gif" width="256"><img src="helmet-preview-v1.gif" width="256"><h2>Body and master endpoints</h2><img src="bare-contact-v1.png"><h2>Shared helmet and protected grip</h2><img src="helmet-fit-contact-v1.png"><p><a href="native-candidate-v1.png">Native148/82/54 board</a> · <a href="source-provenance.json">Source selection and exact prompts</a></p>'''
(H/'index.html').write_text(html,encoding='utf-8');print(f'{checks} package checks PASS;4gearstates/24refs,195native PASS')
