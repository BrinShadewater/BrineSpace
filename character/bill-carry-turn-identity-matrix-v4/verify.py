from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];b=json.loads((P/'bindings.json').read_text());a=json.loads((R/b['inventory']).read_text());checks=[]
def check(ok,name):
 assert ok,name
 checks.append(name)
for gear,name in [('bare','bare-manifest.json'),('helmet','helmet-manifest.json')]:
 m=json.loads((P/name).read_text());states={s['id']:s for s in m['states']};check(len(states)==12,'All12turn states')
 for key,st in states.items():
  ref=a['selectedStateSources'][gear][key];old=json.loads((R/ref['manifest']).read_text());before=next(s for s in old['states'] if s['id']==key)
  for field in ['frameDurationsMs','loop','facings']:
   check(st[field]==before[field],'Original '+field)
  check(len(st['frameFiles'])==len(ref['sourceFiles']),'Full original pose count')
  start,end=key.split('-')[-2:]
  for index,d in [(0,start),(-1,end)]:check((R/st['frameFiles'][index][6:]).read_bytes()==(R/a['selectedStateSources'][gear]['pickup-'+d]['sourceFiles'][-1][6:]).read_bytes(),'Exact current cardinal join')
  if len(st['frameFiles'])==6:
   rev=states['carry-turn-'+end+'-'+start];check(st['frameFiles']==rev['frameFiles'][::-1],'Exact quarter reverse')
  else:
   check(sum(st['frameDurationsMs'])==1600,'Original half-turn duration');check(st['frameFiles'][5] in [a['selectedStateSources'][gear]['pickup-'+d]['sourceFiles'][-1] for d in ['east','west','south','north']],'Exact current cardinal midpoint')
 for row in [x for x in b['rows'] if x['gear']==gear]:
  for f,h in zip(row['sourceFiles'],row['sourceSha256']):check(hashlib.sha256((R/f[6:]).read_bytes()).hexdigest()==h,'Frozen bound source pixels')
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'scope':'Full24selected matrix bindings,all48exact joins,half midpoints,quarter reverses and original clocks;one interior identity gap remain'},indent=2)+'\n');print(str(len(checks))+' matrix checks pass')
