from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;read=lambda p:json.loads(p.read_text());old=read(R/'character/krusher-complete-animation-v1/progress.json');new=read(H/'candidate-bank-index.json');banks={};cache={}
for tag,index in [('old',old),('new',new)]:
 for gear,paths in index['candidatePacks'].items():
  states={}
  for path in paths:
   mp=R/path[6:];m=read(mp)
   for s in m['states']:states[s['id']]=(mp,m,s)
  banks[tag,gear]=states
def image_hash(tag,gear,key,i):
 mp,m,s=banks[tag,gear][key];f=s['frameFiles'][i];path=R/f[6:] if f.startswith('res://') else mp.parent/f;ck=(str(path),tuple(m['pivot']))
 if ck not in cache:
  assert all(float(v).is_integer() for v in m['pivot']);im=Image.open(path).convert('RGBA');canvas=Image.new('RGBA',(512,512));canvas.alpha_composite(im,(256-int(m['pivot'][0]),320-int(m['pivot'][1])));cache[ck]=hashlib.sha256(canvas.tobytes()).hexdigest()
 return cache[ck]
rows=[];errors=[]
for gear in ['bare','helmet']:
 states=banks['new',gear];pairs=[]
 def add(a,ai,b,bi,kind):
  if a in states and b in states:pairs.append((a,ai,b,bi,kind))
 for d in ['east','north','south','west']:
  idle='idle-'+d
  for entry in ['kneel','torch-draw','sit-down','lie-down','death-ground','inspect','eat','drink']:add(idle,0,entry+'-'+d,0,'standing-entry')
  for exit in ['stand','torch-stow','sit-rise','get-up','inspect','eat','drink','recover-air']:add(exit+'-'+d,-1,idle,0,'standing-return')
  for a,b in [('kneel','repair'),('repair','stand'),('torch-draw','weld'),('weld','torch-stow'),('sit-down','sit-idle'),('sit-idle','sit-rise'),('read-seated-enter','read-seated'),('read-seated','read-seated-exit'),('read-seated-exit','sit-idle'),('lie-down','sleep'),('sleep','get-up'),('swim-start','swim'),('swim-stop','tread'),('salvage','swim-pickup'),('swim-pickup','swim-carry'),('pickup','carry'),('carry','unload')]:add(a+'-'+d,-1,b+'-'+d,0,'action-handoff')
  add('tread-'+d,0,'swim-start-'+d,0,'water-entry');add('swim-'+d,0,'swim-stop-'+d,0,'water-exit');add('swim-'+d,0,'swim-distress-'+d,0,'distress-entry');add('swim-distress-'+d,-1,'swim-'+d,0,'distress-return')
 for a,b in [('bunk-enter-east','bunk-sleep-east'),('bunk-sleep-east','bunk-exit-east')]:add(a,-1,b,0,'bunk-handoff')
 add('idle-east',0,'bunk-enter-east',0,'bunk-entry');add('bunk-exit-east',-1,'idle-east',0,'bunk-return')
 for key,(mp,m,s) in states.items():
  if key.startswith(('swim-turn-','swim-carry-turn-','carry-turn-')):
   origin,target=key.split('-')[-2:];prefix=key.rsplit('-turn-',1)[0];add(prefix+'-'+origin,0,key,0,'turn-entry');add(key,-1,prefix+'-'+target,0,'turn-return')
  if key.startswith('swim-cancel-'):
   origin=s.get('provenance',{}).get('sourceProvenance',{});entrance=origin.get('entrance','');j=origin.get('entranceIndex',0)
   if 'release' in key:parts=key.split('-');entrance='swim-pickup-'+parts[-1];j=int(parts[-2])
   add(entrance,j,key,0,'indexed-cancel-entry');add(key,-1,'swim-'+key.rsplit('-',1)[1],0,'cancel-return')
  if key.startswith('meal-return-'):add(key,-1,'idle-'+key.rsplit('-',1)[1],0,'meal-return')
  if s.get('loop'):add(key,0,key,-1,'loop-closure')
 for a,ai,b,bi,kind in pairs:
  before=image_hash('old',gear,a,ai)==image_hash('old',gear,b,bi);after=image_hash('new',gear,a,ai)==image_hash('new',gear,b,bi);row={'gear':gear,'from':a,'fromIndex':ai,'to':b,'toIndex':bi,'kind':kind,'baselineExact':before,'newExact':after};rows.append(row)
  if before and not after:errors.append(row)
report={'comparisons':len(rows),'baselineExact':sum(q['baselineExact'] for q in rows),'newExact':sum(q['newExact'] for q in rows),'errors':errors,'rows':rows,'scope':'Whole visible RGBA rendered at common physical foot pivot. Named entries/returns/action handoffs/turns/indexed cancellations/loops preserve previously exact joins. Baseline-distinct motion poses recorded, not forced equal. No station or palette acceptance.'}
(H/'candidate-bank-joins.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['rows','scope','errors']}));print(json.dumps({'regressions':len(errors),'examples':errors[:20]}))
