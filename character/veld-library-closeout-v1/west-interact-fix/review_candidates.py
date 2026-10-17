"""Review-only extraction. Never writes a runtime manifest or selected source."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np,re
P=Path(__file__).resolve().parent;R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=json.loads((P/'INPUTS.json').read_bytes())
for name,digest in inputs['bindings'].items():assert sha(R/name)==digest,name
manifest=R/'character/veld-action-west-matched-v1/manifest.json'
state=next(s for s in json.loads(manifest.read_bytes())['states'] if s['id']=='interact-west')
rows=[];bindings=dict(inputs['bindings']);board=Image.new('RGB',(1104,1070),'#202a30');draw=ImageDraw.Draw(board)
for version in range(4):
 raw=None
 if version:
  raw=Image.open(P/f'raw-v{version}.png').convert('RGBA');w,h=raw.size
  assert w==h and w%2==0
  bindings[(P/f'raw-v{version}.png').relative_to(R).as_posix()]=sha(P/f'raw-v{version}.png')
 for i in range(6):
  old=Image.open(manifest.parent/state['frameFiles'][i]).convert('RGBA');image=old
  if version and 0<i<5:
   k=i-1;image=raw.crop(((k%2)*w//2,(k//2)*h//2,(k%2+1)*w//2,(k//2+1)*h//2)).resize((184,184),Image.Resampling.LANCZOS)
   path=P/f'candidate-v{version}-{i:03}.png';image.save(path)
   data=np.array(image);ys,xs=np.where(data[:,:,3]>=128)
   rows.append(dict(version=version,slot=i,height=int(ys.max()-ys.min()+1),top=int(ys.min()),floor=int(ys.max()),left=int(xs.min()),right=int(xs.max())))
  board.paste(image,(i*184,version*260+30),image)
  draw.text((i*184+4,version*260+4),(['Selected','Rejected V1','Rejected V2','Rejected V3'][version])+' '+str(i),fill='white')
board.save(P/'all-candidates-comparison.png')
for file in ['prompt.txt','prompt-v2.txt','prompt-v3.txt','edit-target-four-poses.png','edit-target-registered-idle-grid.png','appearance-original-west.png','appearance-selected-idle.png']:
 bindings[(P/file).relative_to(R).as_posix()]=sha(P/file)
inv=json.loads((R/'character/veld-library-closeout-v1/installed/selected-library.json').read_bytes())
block=(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8').split('if actor == "veld":',1)[1].split('elif actor == "branforth":',1)[0]
bare=re.findall(r'player\.load_manifest\("res://([^"\n]+)"',block)
helmet=re.findall(r'player\.load_equipment_manifest\("diving-helmet", "res://([^"\n]+)"',block)
assert inv['loader']['bare'][-len(bare):]==bare and inv['loader']['helmet'][-len(helmet):]==helmet
source_count=0
for gear in ['bare','helmet']:
 for key in ['idle-west','walk-west','interact-west','repair-west']:
  item=inv['resolved'][gear][key]
  assert sha(R/item['manifest'])==inv['bindings'][item['manifest']]
  for path in item['frameFiles']:
   assert sha(R/path)==inv['sourceBindings'][path],path
   source_count+=1
verdict=dict(status='All three redraws rejected; current selected sources and normal Veld loader order unchanged',mapping='Equal2x2 crop and fixed184/cellwidth scale. No pose-bound fit, local grade/anatomy edits, recentering, re-flooring, or rescue crop.',reference=dict(height=148,top=24,floor=171),measurements=rows,reasons={'v1':'160–162px tall, enlarged head, floor177–178 instead of171','v2':'153–154px tall; head top16–17 instead of24, floor169; identity/panels drift','v3':'139px tall; reflow puts row1floor164 and row2floor156; figure shifted laterally'},sourcePresentationsVerified=source_count,bindings=bindings,nativeTests='Not run: candidates fail source visual/registration review before admission. Prior native passes refer only to their original sources.',scope='One West interaction repair attempt; no completed correction or full-set acceptance.')
(P/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(candidatePoses=len(rows),selectedWestSourcesVerified=source_count,status=verdict['status'])))
