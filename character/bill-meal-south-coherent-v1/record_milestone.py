from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OUT=ROOT/'output/bill-meal-south-candidate-native-v1'
assert json.loads((P/'source-rulers.json').read_text())['source']=='sources/eat-v1.png','Historical v1 record; use record_detail_v2.py for current source'
v=json.loads((P/'verification.json').read_text());n=json.loads((OUT/'validation.json').read_text())
assert v['passed'] and n['passed'] and not n['realProfileChanges']
assert '71 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
handoff='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill south eating candidate

## Objective and acceptance
Complete Bill's full master-consistent animation set, then full-set polish.
South eating authored and native reviewed. Design correction/transitions pending.

## Accepted decisions and constraints
Selected south idle owns identity, perspective, body size and matte materials.
Left hand supports small bowl low, right connected spoon hand scoops/lifts/bites/
lowers. Two hands, planted upright stance, front camera, no turn/step/bob.
Face grading bounded separately from neutral suit so matte matching does not
blacken skin. Current actual galley contacts N/S; original service clocks unchanged.

## Current state
Raw built-in exec-f273b762-856d-45f6-91ff-75bb55a1e62a/exact prompt retained.
Six461/461/461/457/457/457px source figures. Fixed[.32,.3214] atlas ruler,
density1.05, selected south neutral/hair/face/burgundy grade and master sole223.
One bare staged eat-south state/seven960ms slots/six distinct poses/exact closure.
Shared256plane/pivot128,224/H148/dry0. Build/verify/preview/registration/hashes/
master alpha-band comparison/evidence retained. No normal loader/actor changes.

## Verification
24package/71native PASS12.75s. Source/hash/master bindings, exact loaded pixels,
direction/action/dry metadata, shared plane, pacing/repeated cycles and closure.
Native148/82 and idle boards reviewed; bowl/supporting hand/spoon path readable,
no obvious extra hand or detached arm. Scratch APPDATA; all2,914 owner non-log
files unchanged. Actual meal contact/pickup/return/interruption/restore unproved.
Alpha crowns76–77 vs master77, sole223 throughout. Frame0 head114–142 vs master
115–140; legs106–152 vs106–149; boots102–156 vs101–155. Small broader build/head,
brighter red chest badge and reduced fine suit/harness details remain. Metrics
support visual review; this is not final master-consistency acceptance.

## Next action
Correct south chest badge/detail and compare proportions across south drinking
and transitions as authored; do not propagate the red badge as a new authority.
Complete south cup/bowl pickup-return family, then actual N/S service phase/contact/
interrupt/restore proof. West meals, generic rest/dry death, wider inspection
audits and full-set cross-animation polish remain. Full goal active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''
Bill south eating candidate — September30,2026.
Built-in exec-f273b762-856d-45f6-91ff-75bb55a1e62a/exact prompt retained.
Six461/461/461/457/457/457px front figures, fixed[.32,.3214] ruler,density1.05,
selected south matte neutral/hair/face/burgundy grade, sole223. Left bowl support,
right spoon scoop/lift/bite/lower, upright planted body. One bare staged state,
seven960ms slots/exact whole-pose closure.24package/71native PASS12.75s;
native148/82 and idle boards reviewed. All2,914 owner files intact in scratch.
No normal loader/actor/geometry/reward changes. Source/native checks do not prove
actual counter contact or saved service phases. Alpha crown76–77 vs master77;
frame0 head114–142 vs115–140, legs106–152 vs106–149, boots102–156 vs101–155.
Recorded visible mismatches: slightly broader head/legs, redder chest badge and
reduced fine harness/suit detail. Staged structural success is not final identity
acceptance; correct these instead of adopting the new badge as master authority.
Lesson: separately bound front face grading and inspect chest detail/alpha bands
alongside grip anatomy at148 and82px; numeric height alone can miss design drift.
Next south design correction/drinking/pickup-return, actual N/S service integration,
remaining west/rest/drydeath and full-set polish. Full goal active.
Handoff:character/bill-meal-south-coherent-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill south eating candidate — September30,2026\n'+note+'\n').encode()+status.read_bytes())
files=[P/name for name in ['build.py','verify.py','manifest.json','verification.json','HANDOFF.md','index.html','source-rulers.json','registration.json','frame-hashes.json','material-grade.json','contact-sheet.png','master-comparison.json','compare_master.py']]+list((P/'sources').glob('*'))+[OUT/'validation.json',OUT/'loaded-water-carry.png',ROOT/'tests/test_bill_meal_south_candidates.gd',ROOT/'tools/run_bill_meal_south_candidate_validation.py']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':24,'native':71},'native':n,'scope':'staged eating loop only; recorded badge/detail/proportion correction and real meal phases/contact/interruption/restore pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded south eating source/native proof and specific master drift to correct')
