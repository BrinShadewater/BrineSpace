from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
path=P/'cross-family-review-evidence.json';e=json.loads(path.read_text(encoding='utf-8'))
assert hashlib.sha256((P/e.get('inventorySnapshotPath','selected-library.json')).read_bytes()).hexdigest()==e['inventorySHA256']
for relative,digest in e['bindings'].items():assert hashlib.sha256((R/relative).read_bytes()).hexdigest()==digest,relative
e['reviewedBoards']=e['boards'];e['reviewedSourcePresentations']=80
e['visualReview']='All four boards/80 source presentations inspected. Current dry/water sampled helmets retain graphite shared construction; historical orange-helmet findings must not be applied to later selected overrides. Flag larger-looking West/South carry faces relative to idle and warmer South prone rear hardware for original directional-master/detail comparison. These flags are not confirmed source defects or authority for global recolouring. Perspective and prone foreshortening preserved; no motion/native/full-set acceptance.'
path.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
block='''## Veld current selected-library comparison — October 2, 2026

Refreshed actual catalog/ordered normal-loader inventory after partial South fall
admission:198 bare/192 helmet IDs,118 manifests,4804 unique source files, no missing
references. Original pre-admission snapshot retained. Six bare-only IDs are helmet
equip/remove and four weld aliases; equipment-changing semantics/controller validity
must govern parity, not automatic creation of six helmet counterparts. Inventory
now binds exact source hashes and declared timing as well as manifest/profile paths.

All four new cross-family boards/80 source presentations inspected: first/middle
idle/carry/swim/swim-carry/water-fall in all cardinals/both gears, fixed H148/pivot
translation only. Newer sampled water helmets retain graphite shared construction;
historical orange-helmet defects cannot be assigned to superseding selected art.
West/South carry face size and South prone warmer rear hardware are comparison
flags for original directional-master/detail review, not confirmed defects or a
global recolouring instruction. Prone perspective is not standing-height drift.

Lesson: preserve inventory baselines, resolve current overrides before applying
historical findings, and bind the sampled art. Compare equipment parity against
valid behavior and rear-view material against the correct original master. Source
samples can find drift but do not certify all frames, motion or native rendering.
Earlier side sit/read source issues and full-library consistency work remain open.
Normal partial South Continue remains running; its separate handoff owns progress.
Evidence:character/veld-animation-coverage-audit-v1/cross-family-review-evidence.json.
Full goal active/incomplete. No source mutation, commit or export in this audit.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for dest in paths:
    old=dest.read_text(encoding='utf-8')
    if block.splitlines()[0] not in old:dest.write_text(block+old,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld selected-library fidelity

## Objective and acceptance
Full master-consistent Veld set followed by cross-family polish. Current inventory
and sampled comparisons identify review targets; full acceptance remains open.

## Accepted decisions and constraints
Actual catalog and ordered normal overrides define selection. Keep H148 and pivots;
preserve prone foreshortening. Grade/detail changes need directional master evidence.
Original owner decisions and canonical shared helmet remain authoritative.

## Current state
audit.py now binds4804unique selected sources and timing metadata; original inventory
saved as selected-library-before-partial-admission.json. Current198bare/192helmet
IDs/118manifests/no missing sources. review_cross_family.py produces four boards,
80presentations; all viewed/source hashes retained. record_current_review.py updates
status/pipeline/bible/maintained and installed skill. No runtime/source mutation.

## Verification
Static inventory and source comparison only. Newer sampled water helmets match
shared graphite construction; superseded orange-shell notes do not apply blindly.
West/South carry face proportions and South prone warm rear hardware are flags,
not confirmed defects. Prior48furniture samples identify older side sit/read drift.
Equipment-only equip/remove and controller-invalid helmet weld explain parity
questions; do not manufacture missing gear art solely to equalize counts.

## Next action
Complete running normal South partial Continue (session54472), then run/review
character/veld-sofa-partial-fall-south-selected-v1/review_continue.py. Its handoff
owns exact running scope. Confirm cross-family flags beside original directional
masters and complete full-frame/native joins before any source/grade repair.
Earlier side source candidates remain staged; default lounge North/readSouth
contacts must not be fabricated to admit dormant art. Full natural scheduler,
traffic/hazards, Title/new-process and final cross-library polish remain open.
No commit/export/full-goal completion.
''',encoding='utf-8')
print('80-source review recorded; five maintained references and audit handoff updated')
