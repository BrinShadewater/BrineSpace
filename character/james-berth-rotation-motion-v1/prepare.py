from pathlib import Path
import hashlib,json,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];inputs={}
def freeze(p):inputs[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
cov=json.loads((R/'character/james-animation-coverage-2026-09-30/runtime-coverage.json').read_bytes())
for mode in ['body','equipment']:
 for d in ['north','south','east','west']:
  for action in ['lie-down','sleep','get-up','idle']:
   f=R/cov[mode][action+'-'+d]['path'];freeze(f);m=json.loads(f.read_bytes());s=next(s for s in m['states'] if s['id']==action+'-'+d)
   for rel in s['frameFiles'][:1] if action=='idle' else s['frameFiles']:
    freeze(R/rel.removeprefix('res://') if rel.startswith('res://') else (f.parent/rel).resolve())
for rel in ['scripts/branforth_npc.gd','scripts/bill_npc.gd','scripts/crew_life.gd','scripts/crew_room_activity.gd','scripts/grid_canvas.gd','scripts/main.gd','scripts/room_layout_store.gd','character/james-rest-material-continuity-v1/validate.gd','character/james-rest-material-continuity-v1/no-layout-overrides.json']:
 freeze(R/rel)
(P/'runtime-inputs-before.json').write_text(json.dumps(inputs,indent=2)+'\n');(P/'runtime-coverage.json').write_text(json.dumps(cov,indent=2)+'\n');shutil.copy2(R/'character/james-locker-continue-v1/run_validation.py',P/'run_validation.py')
print('Frozen',len(inputs),'source/manifest/controller/fixture inputs; strict scratch runner ready.')
