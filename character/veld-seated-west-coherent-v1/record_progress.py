from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent; R=P.parents[1]
v=json.loads((P/'verification.json').read_text()); n=json.loads((R/'output/veld-seated-west-candidate-v1/validation.json').read_text()); f=json.loads((P/'family-review.json').read_text())
assert v['failures']==0 and n['passed'] and not n['realProfileChanges']
for name,digest in f['bindings'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
title='Veld independent west seated and cardinal comparison — October 1, 2026'
note=f'''## {title}

West6pose built-in source exec7d32d8a4-c76b-4d5e-903c-5879d1e72386 saved with
prompt/reference roles. Independent left-facing side master; selected West idle
is idle-west-transition-matte-v1 (do not infer filename from East); East atlas
articulation only. Scanner near hip/canisters far hip, no mirrored body.
One148/544 ruler, pooled6materials, exact selected standing,800ms down/exact
reverse/static held; native34x38 West helmet unchanged scale/grade/collar-tracked.
6states/26refs/12exports,256canvas/p128224/H148, staged/unselected.
72package checks0failures/22deterministic files;233controlled native player/actor
checks0failures,25.20s engine0/no errors,2931non-log owner files unchanged scratch
APPDATA. Paired source/native148/82 boards reviewed. Interrupted-rise hook and
snapshot admission, not real service loss/chair route/fresh Continue/smoothness.

Cardinal board24samples/48bound fitted sources and full lower/held/rise GIF at
shared scale/clock,10800ms slowed preview. Bare held opaque heightsN107/E114/S126/
W115. Visual South pose is taller/more upright and North shorter; investigate
pelvis/seat/thigh/shin anchors against masters and actual furniture before changing
art. Different views need not share occupied bounds. One standing ruler proves
calibration, not seated anatomy/contact; never normalize each pose's height to
hide drift. Resolver lounge sitsNorth/observation sofa readsSouth; no actual side
seated chair contact identified, keep that integration gap explicit.
Next South/North source anatomy/chair audit, complete motion/joins, side held
breath/interruptions/Continue and selection, inherited rest/death/water polish.
Full goal active/incomplete. Handoff:character/veld-seated-west-coherent-v1/HANDOFF.md.

'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in targets:
 old=path.read_bytes()
 if title.encode() not in old:
  if path.name=='CURRENT_STATUS.md':path.write_bytes(note.encode()+old)
  else:
   with path.open('ab') as out:out.write(b'\n\n'+note.encode())
files=[p for p in P.rglob('*') if p.is_file() and p.suffix not in ('.import','.pyc') and p.name!='candidate-evidence.json']
files += [R/'tests/test_veld_seated_west_candidate.gd',R/'tests/test_veld_seated_west_candidate.gd.uid',R/'tools/run_veld_seated_west_candidate.py']
files += [R/'output/veld-seated-west-candidate-v1'/name for name in ('validation.json','native.log','native.png','profile-before.json','profile-after.json')]
bindings={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}; bindings.update(f['bindings'])
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged/unselected west seated and family source audit','packageChecks':v['checks'],'nativeChecks':233,'nativeSeconds':n['seconds'],'ownerProfileFilesUnchanged':n['realProfileFileCount'],'bindings':bindings,'remaining':'cardinal anatomy/chair/motion/interruptions/fresh Continue/selection/full-set consistency and acceptance'},indent=2)+'\n')
print(json.dumps({'boundFiles':len(bindings),'notes':5,'goal':'active/incomplete'}))
