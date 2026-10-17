from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-south-breathing-v1'
v=json.loads((O/'validation.json').read_text());assert v['passed'] and not v['realProfileChanges']
p=json.loads((P/'verification.json').read_text());assert p['checks']==65 and not p['failures']
title='Veld south seated local breathing — October 1, 2026'
note='''

## Veld south seated local breathing — October 1, 2026

Paired held-only candidate in character/veld-seated-south-breathing-v1 uses exact
fitted South neutral with locally authored rib/sleeve expansion. North maximum
.363636px/side, phases0/.5/1/.75/.25/0, six600ms slots/3.6sec. All materials from
locked neutral; no generated RGB/new full-body motion/no additional grade.
Face/hair/helmet/collar/central chest fittings/belt/hands/knees/boots protected;
neutral seam/down/rise exact. Original South finite/static pack unchanged.
Existing paired head fit difference ends y129; breathing starts y131 to retain
hardware. One148/509 ruler/p128224, staged/unselected held manifests.

65package checks/16deterministic files;182native checks/0failures,24.36sec
engine0/no errors. Controlled Veld source hook, normal player plus fixture-only
overrides, two visual-clock cycles/third seam, exact sources/joins, snapshot
admission/pause, paired148/82 native board and source board reviewed. All2931
non-log owner files unchanged under scratch APPDATA. No actual South furnishing,
service loss/fresh Continue/natural route/owner acceptance proof.

Lesson: held actions use visual-clock looping; finite frame_at_elapsed does not
wrap and life_seated actor timer does not select breathing phase. Initial fixture
180checks/52failures retained; corrected fixture, no runtime change. Bound source
deformation below actual shared helmet/collar pixels, not an assumed head boundary.
Tiny local respiration is distinct from newly generated coherent body poses.
Default lounge sit resolver requests North; preserve furniture rather than force
South and claim natural room coverage. Next South motion/contact, natural North
approach/exit/hazards, independent East/West seated sources, rest/death joins and
full-set polish. Full goal active/incomplete. Handoff: this candidate/HANDOFF.md.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 old=path.read_bytes()
 if title.encode() not in old:
  new=note.encode();path.write_bytes(new.lstrip(b'\n')+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+new)
files=[f for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name!='evidence.json']
files += [O/n for n in ['native.png','native.log','validation.json','profile-before.json','profile-after.json']]
files += [R/'tests/test_veld_seated_south_breathing.gd',R/'tests/test_veld_seated_south_breathing.gd.uid',R/'tools/run_veld_seated_south_breathing.py',R/'tests/index.json']
files += [R/f'character/veld-seated-south-coherent-v1/frames/{g}/sit-down-south/005.png' for g in ('bare','helmet')]
files += [R/'character/veld-seated-north-breathing-source-v1/fitted-registration.json']
bound={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(P/'evidence.json').write_text(json.dumps({'scope':'paired local held breathing source and controlled native player; no normal selection/furniture/Continue/owner acceptance','packageChecks':65,'nativeChecks':182,'files':bound},indent=2)+'\n')
print(json.dumps({'boundFiles':len(bound),'notes':5,'normalSelection':False}))
