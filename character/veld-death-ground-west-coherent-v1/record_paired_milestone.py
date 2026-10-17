"""Record scoped paired candidate evidence without relabeling prior bare proof."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-death-ground-west-candidate-v1'
native=json.loads((O/'validation.json').read_text());package=json.loads((P/'paired-verification.json').read_text())
assert native['passed'] and package['checks']==44 and package['failures']==0
index=R/'tests/index.json';data=json.loads(index.read_text());key='test_veld_death_ground_west_candidate'
if key not in data['subsystems']['veld-dry-death']:data['subsystems']['veld-dry-death'].append(key)
data['lanes'][key]={'lane':'native','reason':'Paired west dry-collapse candidate requires native148/82 visual board.'}
index.write_text(json.dumps(data,indent=2)+'\n')
note='''

## Veld west paired dry-collapse candidate — October 1, 2026

West bare source fit now paired with exact selected helmet idle and native34x38west component, source neck registration/20,38,50,85,88degree tilt. Component stays native scale; pose body pixels outside local head/helmet regions and all prior bare exports exact. Built-in closed-eye source exec-93010918-558a-4ddd-83f9-9c1735b99eb6 contributes only8native RGBpixels to frames4/5; all original shell/visor/collar/face outline and component alpha protected.44 paired package/master/body checks and18deterministic files PASS.70 actual-player checks PASS, native148/82 reviewed; explicit scratchAPPDATA,2,928real non-log files unchanged during5.88s interval. Correct finite1420ms corpse and in-memory player snapshot/paused clock; candidate only, not normal mortality/Continue/world or owner visual acceptance. Prior31bare package proof and earlier east profile-guard failures retain dated scope. North/south dry collapse, generic rest/life, actual survival/Continue/clearance and full cross-family master/perspective/scale/material/detail/motion polish remain. Full goal active. Handoff:character/veld-death-ground-west-coherent-v1/HANDOFF.md.

Lesson: calibrate a generated eyelid insert from adjacent cheek skin, not from the dark eyelid itself. Using the eyelid median for exposure amplified highlights and made the first insert look open. Preserve the native shell, alpha and every protected facial pixel; review the resulting expression at native and station scales as well as enlarged. Frozen ruler and exact cardinal component are technical constraints, not a certificate of natural falling motion or furniture clearance.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    p=R/rel;old=p.read_bytes()
    if note.lstrip().encode('utf-8') not in old:p.write_bytes(note.lstrip().encode('utf-8')+old if rel=='docs/CURRENT_STATUS.md' else old+note.encode('utf-8'))
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.encode('utf-8') not in installed.read_bytes():
    with installed.open('ab') as f:f.write(note.encode('utf-8'))
handoff='''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld paired west dry collapse

## Objective and acceptance
Full matching Veld set plus whole-set master/perspective/proportion/material/detail/motion polish. West paired collapse remains candidate only; full goal active.

## Accepted decisions and constraints
Actual selected bare west idle and selected west helmet idle/native34x38component are authorities. Independent west art/tool ownership, one148/471ruler, dry256/p128,224/H148, original1420ms finite6poses. Native helmet scale1, exact cardinal entries, closed terminal expression without redesigned shell. No production selection/commit/export or owner profile edit.

## Current state
Bare builder and all6exports unchanged. build_helmet.py registers native west component to measured source neck/tilt; expression contributes8RGBpixels in native region[5,17,9,19] to helmet4/5 only, all component alpha and outside pixels exact. Raw generation/exact prompt/expression crop and cheek-gain reference retained. Paired6+6frames, manifests, registration/hashes, review boards and finite synchronized HTML. Initial bright eye calibration corrected before package/native proof. Prior bare HANDOFF/index/evidence preserved under revisions/bare-fit-v2.

## Verification
44paired master/component/protected-body/package checks PASS;18deterministic rebuilt files. Prior31bare checks retain their scope.70actual CrewSpritePlayer checks PASS: exact loaded12pixels/metadata/slots, finite terminal, arbitrary initial clock, validated in-memory player snapshot and paused restore. Native148/82 complete board reviewed. Runner5.88s passed, scratchAPPDATA and all2,928real non-log files unchanged. Candidate injection, not normal loader/survival/Continue/furniture clearance. Source pose/head/neck/grade visually reviewed against west masters; fine insignia/face/cloth/detail/pacing remain part of family polish.

## Next action
Author independent south/north dry collapse from own selected masters; fit paired canonical helmets/expression at source ruler. Then prove actual mortality and disk Continue/clearance/joins from other states before normal selection. Generic rest/life and complete cross-animation matching/polish remain. No blocker; east failed profile guards remain recorded, this west interval does not relabel them.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
paths=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and 'revisions' not in p.parts and p.name not in ['paired-candidate-evidence.json','bare-candidate-evidence.json']]
paths += [R/'tests/test_veld_death_ground_west_candidate.gd',R/'tests/test_veld_death_ground_west_candidate.gd.uid',R/'tools/run_veld_death_ground_west_candidate.py',index]+[O/name for name in ['validation.json','native.log','native-contact.png','profile-before.json','profile-after.json']]
evidence={'scope':'paired west candidate and actual player source/timing/metadata/in-memory paused snapshot; no normal mortality/Continue/world claim','normalSelection':False,'packagingChecks':44,'nativePlayerChecks':70,'nativeRunner':native,'files':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(P/'paired-candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({'boundFiles':len(paths),'packagingChecks':44,'nativePlayerChecks':70,'runnerPassed':native['passed'],'normalSelection':False}))
