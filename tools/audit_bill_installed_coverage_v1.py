"""Resolve normal loader and inherited selected banks; preserve dated inventories."""
from pathlib import Path
import json,re,hashlib,importlib.util,contextlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-installed-coverage-2026-10-04';D.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('old_bill_resolution',R/'character/bill-coverage-audit-v1/build_audit.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.P=D
with (D/'resolution.log').open('w',encoding='utf-8') as log,contextlib.redirect_stdout(log):mod.main()
q=json.loads((D/'source-audit.json').read_text());order=[]
def append(path,gear):
 p=R/path[6:];data=json.loads(p.read_text());relative=p.relative_to(R).as_posix();order.append({'gear':gear,'manifest':relative});q['manifestBindings'][relative]=hashlib.sha256(p.read_bytes()).hexdigest()
 for s in data['states']:
  files=[R/f[6:] if f.startswith('res://') else (p.parent/f).resolve() for f in s['frameFiles']]
  q['selected'][gear][s['id']]={'manifest':relative,'status':data.get('status',''),'files':[f.relative_to(R).as_posix() for f in files],'timing':s['frameDurationsMs'],'loop':s['loop'],'pivot':data.get('pivot',[46,86]),'standingHeight':data.get('standingHeight',74),'precomposed':data.get('precomposed',False),'mirrored':False}
for script in ['character/bill-carry-cardinal-runtime-v1/carry_player.gd','character/bill-carry-cardinal-runtime-v2/stow_player.gd']:
 text=(R/script).read_text().split('func frame(',1)[0]
 paths=re.findall(r'"(res://[^\"]+\.json)"',text)
 for path in paths:append(path,'helmet' if 'helmet-manifest' in path else 'bare')
text=(R/'scripts/bill_carry_player.gd').read_text()
for field in ['NORTH_BANKS','SOUTH_BANKS','MASTER_BANKS']:
 block=text.split('const '+field+'=',1)[1].split('\nconst ',1)[0]
 for path in re.findall(r'"(res://[^\"]+\.json)"',block):append(path,'helmet' if 'helmet-manifest' in path else 'bare')
q.update(scope='Literal catalog/normal grid loader then inherited production source bank order; native materialized rows checked separately. Presence is not full visual acceptance.',inheritedLoadOrder=order,stateCounts={gear:len(rows) for gear,rows in q['selected'].items()})
q['lifeRows']=[{'action':a,'direction':d,'gear':g,'present':a+'-'+d in q['selected'][g]} for a in mod.ACTIONS for d in ['north','east','south','west'] for g in ['bare','helmet']]
q['selectedSlots']={g:sum(len(s['files']) for s in rows.values()) for g,rows in q['selected'].items()}
q['sourcePaths']=sorted({p for rows in q['selected'].values() for s in rows.values() for p in s['files']})
(D/'source-audit.json').write_text(json.dumps(q,indent=2)+'\n')
print(json.dumps({'states':q['stateCounts'],'slots':q['selectedSlots'],'inheritedBindings':len(order),'uniqueSources':len(q['sourcePaths']),'missingLifeRows':sum(not r['present'] for r in q['lifeRows'])}))
