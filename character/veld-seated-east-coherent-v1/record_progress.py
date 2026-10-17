"""Bind this source/native milestone and append concise reusable lessons."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent; R=P.parents[1]
v=json.loads((P/'verification.json').read_text()); n=json.loads((R/'output/veld-seated-east-candidate-v1/validation.json').read_text())
assert v['failures']==0 and n['passed'] and not n['realProfileChanges']
title='Veld independent east seated pair — October 1, 2026'
note=f'''## {title}

Independent right-facing6pose source exec3bfbb1ae-74a3-4bed-8eb6-178698517547;
selected east idle palette/anatomy, side foundation detail, South source articulation
only. One148/542 standing ruler; occupied heights542/510/464/419/416/418.
Pooled6material curves before extraction; exact selected standing joins,800ms down,
exact reverse rise/static held.6states/26refs/12exports,256canvas/p128224/H148.
Selected native34x38 east helmet unchanged scale/grade, source collar-tracked.
Source/native closeups caught rear low-bun fragment beyond initial face-centered
head mask; final bounds include full rear silhouette for grade/removal, preserving
body outside fit. Lesson: profile face landmarks do not bound the bun; inspect rear
extent separately in every pose at native scale, not just frontal crops.
72package checks0failures/22deterministic files; final233native candidate checks,
0failures/25.00s engine0/no errors,2931real non-log files unchanged scratchAPPDATA.
Native148/82 source board and browser seated helmet/master reviewed. Earlier two
native intervals retained; final evidence supersedes their pixel scope.
New art staged/unselected; controlled player/actor interrupted-rise hook and
snapshot admission, not furniture/natural routing/service-loss/fresh Continue or
smoothness/owner acceptance. Next complete motion/east chair contexts, held breath,
independent West source and cross-family polish. Full goal active/incomplete.
Handoff:character/veld-seated-east-coherent-v1/HANDOFF.md.

'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in targets:
 old=path.read_bytes()
 if title.encode() not in old:
  if path.name=='CURRENT_STATUS.md': path.write_bytes(note.encode()+old)
  else:
   with path.open('ab') as out: out.write(b'\n\n'+note.encode())
files=[p for p in P.rglob('*') if p.is_file() and p.suffix not in ('.import','.pyc') and p.name!='candidate-evidence.json']
files += [R/'tests/test_veld_seated_east_candidate.gd',R/'tests/test_veld_seated_east_candidate.gd.uid',R/'tools/run_veld_seated_east_candidate.py']
files += [R/'output/veld-seated-east-candidate-v1'/name for name in ('validation.json','native.log','native.png','profile-before.json','profile-after.json')]
bindings={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged/unselected east seated pair','packageChecks':v['checks'],'nativeChecks':233,'nativeSeconds':n['seconds'],'ownerProfileFilesUnchanged':n['realProfileFileCount'],'bindings':bindings,'remaining':'full motion/furniture/interruptions/fresh Continue/West source/full-set consistency and acceptance'},indent=2)+'\n')
print(json.dumps({'boundFiles':len(bindings),'notes':5,'goal':'active/incomplete'}))
