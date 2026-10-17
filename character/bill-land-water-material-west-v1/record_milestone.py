from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
f=P/'review.json';e=json.loads(f.read_text(encoding='utf-8'))
assert e['validation']['passed'] and e['checks']==2987 and not e['targetedChanges']
e['visualReview']='Both complete advancing entry boards inspected:90 source/native pairs. Body/head/helmet remain readable and connected through captured crouch/push/lift/prone. Wet material changes progressively rather than immediately applying full swimming tint. Source intermediate fabric is bluer/lighter than normal dry walking/helmet endpoint and patch/detail differs; underwater tint softens this but does not resolve master consistency. Posture/head changes at source boundaries and continuous unpaused motion require review. No authored exit bridge or current West checkpoints/Continue.'
e['guardVisualReview']='All fourteen native/source active/takeover pairs inspected. Gear/facing/death/stage/clock/geometry cancellation returns normal source and clears bridge material. Synthetic death/stage snapshot is not natural action completion/dispatch. Raw guard thumbnails are not common-pivot registered.'
e['visualAcceptance']='Staged entry technically passed; full material/master consistency and continuous motion not accepted.'
f.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
note='''## Bill West actual moving water-entry native milestone — October 2, 2026

New fixture-only bill-land-water-material-west-v1 stages paired compact V2 entry
with actual current normal Bill actor navigation/needs/oxygen/safety and source
clock. Uses exact outgoing walking/current incoming swimming phases, union of
actual loaded silhouettes for planar clearance admission/recheck,500ms finite
bridge and terminal gait-phase rebind. Five West head anchors and left-facing
material head offset; per-draw actual-source binding keeps weight/head instance
local. Entry only: no reversed entry as exit; draining uses normal source.
No normal production source/controller admission or new art/grade edits this turn.

2987native checks0fail/engine0/103.57s. Scratch APPDATA; all2931owner non-log files
unchanged. All26targeted pre/post hashes stable, including14paired new source PNGs.
Both bare/helmet entry admitted at1.1166667 and completed1.6166667 with exact
incoming gait source.60060Hz ticks per gear in prescribed10s room rise/hold/drain
and graph-validated path; actual subsequent movement/medium/oxygen checks. Native
captures every entry boundary tick60..104:90advancing source/native pairs. Four
APNGs verify180decoded captured intervals. Fourteen synthetic active/takeover
pairs retained for gear/facing/death/stage/clock/geometry.104pairs/208files total.

Both full90-frame source/native boards and all14guard pairs reviewed. Connected
head/helmet/body, progressive wet material and moving route readable in captures.
Source interior suit remains bluer/lighter than normal dry walking/helmet endpoint;
patch/detail differs. Underwater tint softens the mismatch but does not repair it.
Posture/head source-boundary changes and continuous unpaused motion need review.
Synthetic takeover snapshots do not prove natural priorities/death completion.
No authored West exit bridge, checkpoint/Continue, natural jobs/hydrology or full
master/style acceptance. Actor foot remains planar navigation/depth anchor, not
a separately simulated vertical floor height. Do not claim vertical buoyancy.

New grid/view/current-main fixture with unique paired UIDs, prepare/review builder/
finalizer/recorder, tests/test_bill_land_water_material_west_v1.gd and scratch runner.
Normal shared renderer/actor/player/save code and selected sources unchanged.
Review:character/bill-land-water-material-west-v1/index.html. Goal active/incomplete.
Lesson: cardinal source expansion needs fresh native moving phase/material/clearance
evidence. Technical same-phase completion and a gentle wet tint do not certify
source palette/detail or motion; inspect raw and rendered pairs together.
Next West source grade/detail and continuous motion, independently authored exit,
current-bank checkpoint/Continue; North/South bridges, cargo lifecycle and complete
Bill master/style/perspective/size/height/proportion/colour cross-family polish.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    p=R/rel;t=p.read_text(encoding='utf-8')
    if heading not in t:p.write_text(note+t,encoding='utf-8')
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    t=p.read_text(encoding='utf-8')
    if heading not in t:p.write_text(t+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October2,2026 · BrineSpace · Bill West native water entry

## Objective and acceptance
Complete full master-consistent Bill set, then cross-family polish. This native
entry-only staging milestone leaves the full goal active/incomplete.

## Accepted decisions and constraints
Original left-facing West sources, canonical native helmet, common148 source ruler.
Actual actor/geometry/oxygen remain authoritative. Dry pivot is a planar anchor;
no vertical buoyancy claim. No reversed entry stand-in for an authored exit.
Scratch APPDATA/all-owner fingerprints; preserve concurrent crew work and V1 art.

## Current state
New grid.gd/view.gd/current-main fixture and unique paired UIDs, prepare.py,
prepare_review.py/build_review.py/finalize_review.py/record_milestone.py,
native test and scratch runner. Paired V2 source bank unchanged.104capture pairs,
two full advancing boards/guard board/four APNGs; six guidance files updated.

## Verification
2987checks0fail/engine0/103.57s;2931owner files unchanged,26targeted inputs stable.
Both500ms entries finish on exact incoming swimming phase.90advancing paired
captures and14synthetic guard pairs inspected;180decoded APNG intervals verified.
Progressive wet material/neck connections readable. Raw source palette/detail
mismatch and posture/head changes still need continuous visual review. No normal
admission, natural hydrology/jobs, authored exit or West checkpoint/Continue proof.

## Next action
Source grade/detail and continuous motion, independent West exit, current source
checkpoint/Continue. North/South bridges and remaining cargo lifecycle/full Bill
cross-family master/style/perspective/anatomy/matte consistency polish remain.
''',encoding='utf-8')
print('Recorded2987-check West entry evidence and unresolved material/motion; six guidance files updated.')
