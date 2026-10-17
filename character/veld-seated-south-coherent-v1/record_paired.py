from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-south-candidate-v1'
v=json.loads((O/'validation.json').read_text());assert v['passed'] and not v['realProfileChanges']
package=json.loads((P/'verification.json').read_text());assert package['checks']==70 and package['failures']==0
title='Veld south seated paired source and player — October 1, 2026'
note='''

## Veld south seated paired source and player — October 1, 2026

Independent south source now fits paired sit-down/sit-rise/static sit-idle in
character/veld-seated-south-coherent-v1. Six states/26references/12PNGs, exact
selected standing masters,800ms finite lowering/exact reverse rise/neutral held
joins. One148/509=.2907662083source ruler retained; pooled skin/hair/cloth/metal/
science/cyan grade once before extraction. Native35x39front helmet, tracked
source collar,anchor17/35,scale1/no rotation/no regrade; opaque component and
body outside head fitting exact. Paired source/native148/82, masks and browser
first interior beside master reviewed. Staged/unselected; no normal loader/room/
gameplay changes.

70package checks/21deterministic files; latest233native player/controller checks,
0failures,24.64s engine0/no errors. All2931non-log owner files unchanged with
scratch APPDATA. Controlled Veld actor clocks/interrupted lowering reversal/
snapshot/source admission, fixture-only override in selected player. No actual
furniture/service-loss/fresh Continue/natural-route/owner acceptance claim.
Earlier233/28.86s pass retains original pre-face-mask source scope.

Lesson: correct semantic master sampling before altering overall exposure.
A centered face ellipse on a slightly turned frontal master sampled dark jaw
and excluded bright outer cheek into hair. Browser caught darker new face despite
technical pass. Corrected reference face box x124:143/y83:101 on padded master,
rebuilt raw source once; previous curve report/board retained, no full rollback
claim. Fixed paired board clipping of closeups, distinct from sprite clipping.
Use cache-versioned image URLs as well as review-page URLs after a palette edit.
Generic default lounge sit resolver currently requests North; a forced South
actor there cannot prove natural South seat selection/contact. Preserve furniture
inputs and distinguish source/player review from real directional room use.

Next South held breathing/contact/motion, North natural approach/exit/hazards,
independent East/West seated sources, rest/death joins/full-set polish. Full goal
active/incomplete. Handoff: character/veld-seated-south-coherent-v1/HANDOFF.md.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 old=path.read_bytes()
 if title.encode('utf-8') in old:continue
 new=note.encode('utf-8');path.write_bytes(new.lstrip(b'\n')+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+new)
files=[p for p in P.rglob('*') if p.is_file() and p.suffix in ['.png','.json','.py','.html','.txt','.md'] and p.name!='candidate-evidence.json']
files += [O/name for name in ['native.png','native.log','validation.json','profile-before.json','profile-after.json']]
files += [R/'tests/test_veld_seated_south_candidate.gd',R/'tests/test_veld_seated_south_candidate.gd.uid',R/'tools/run_veld_seated_south_candidate.py',R/'character/veld-shared-helmet-south-v1/fitted-helmet.png',R/'character/veld-shared-helmet-v1/frames/idle-south/000.png',R/'character/crew-runtime-matte-v1/veld/frames/idle-south-breathing-v1/000.png']
bound={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(P/'candidate-evidence.json').write_text(json.dumps({'scope':'paired source/native-player/controller/pixel/clock/joins/selected master hardware, fixture-only selection; not furniture/natural routing/Continue/owner acceptance','normalSelection':False,'packageChecks':70,'nativeChecks':233,'files':bound},indent=2)+'\n')
print(json.dumps({'evidenceFiles':len(bound),'notes':5,'normalSelection':False}))
