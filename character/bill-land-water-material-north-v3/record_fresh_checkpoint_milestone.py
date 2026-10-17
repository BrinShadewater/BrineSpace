from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;D=P/'fresh-checkpoint-review'
e=json.loads((D/'review.json').read_text(encoding='utf-8'));v=e['validation']
assert v['passed'] and not e['targetedInputChanges'] and not v['realProfileChanges']
assert e.get('visualReview') and 'pending' not in e['visualReview'].lower().split('.')[0]
heading='Bill North fresh-scene transition restoration — October 2, 2026'
body=f"""Four actual normal checksum RunSave disk write/read/restore_staged cases exercise
North entry pose4/tick81 and independent exit pose5/tick432, bare/helmet.
Fresh actual current-main scenes, normal actors/player, real workshop navigation,
medium/oxygen rules and source-bound blended water material. Resource-free fixture
sidecar admitted only after world/actor/clock restore, exact bank/source/extent/phase
validation. Eight malformed kinds per case reject without mutating admitted state.

{e['checks']}checks/0failures;160future60Hz ticks compare physical root/facing/state/
medium/needs/oxygen/source/material/head/bridge activity. Eight before-after native
and source pairs exact, including normal terminal gait,16native presentations.
{e['frozenInputCount']}prelaunch targeted inputs stable;{v['realProfileFileCount']}owner non-log files
unchanged under scratch APPDATA. Native interval {v['seconds']}seconds.
Visual review: {e['visualReview']}

First native interval completed1449checks/0failures and owner2931unchanged,
but scripts/grid_canvas.gd changed concurrently during its frozen interval.
All captures/log/profile/records and original frozen map retained under
output/bill-land-water-fresh-checkpoint-north-v1/changed-renderer-interval-v1.
That interval is not credited as a frozen-revision pass. Preparation refreshes
current fixture main/codec/test and entire targeted map before corrected rerun.

Lesson: restore the actual normal scene/actor/world first, then admit only a
resource-free sidecar whose directional bank, both endpoint sources, phase, geometry
and visual clock match current loaded art. North9/8pose banks cannot inherit West7
frame assumptions. Reuse actual axial clear route and its intervening turn; preserve
real navigation/medium rules. Source equality complements native presentation and
future trajectory equality, without implying normal production wiring or Continue.

Next new-process North TitleContinue, full motion/contact/master polish, South
bridges, normal admission/cargo lifecycle and full-library consistency. Entire Bill
objective remains active/incomplete. Review: character/{P.name}/fresh-checkpoint-review/index.html.
"""
entry='\n## '+heading+'\n\n'+body+'\n'
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
 with f.open('rb') as stream:stream.seek(max(0,f.stat().st_size-131072));tail=stream.read()
 if heading.encode() not in tail:
  with f.open('a',encoding='utf-8') as stream:stream.write(entry)
(D/'HANDOFF.md').write_text(f"""# Project handoff

Updated: October2,2026 · Project: {R} · Task: Bill North fresh scene water restore

## Objective and acceptance
Full Bill animation set/master fidelity and final cross-family polish; incomplete.

## Accepted decisions and constraints
Fixture-only source-bound sidecar after normal world restoration. Owner profile
isolated. Original masters/route/medium/oxygen rules and normal catalog retained.

## Current state
North checkpoint.gd, fresh_fixture_main.gd/scene, paired UID files,
tests/test_bill_land_water_fresh_checkpoint_north_v1.gd and runner added.
prepare_fresh_checkpoint.py stages/freezes; build_fresh_checkpoint_review.py
publishes eight before-after native/source pairs and saved disk/sidecar evidence.

## Verification
{e['checks']}checks/0failures,160future ticks exact, eight native/source pairs exact.
{e['frozenInputCount']}inputs stable;{v['realProfileFileCount']}owner files unchanged.
{e['visualReview']}

## Next action
New-process North TitleContinue; full motion/contact/master polish, South bridges,
normal admission/cargo lifecycle, full-library consistency/polish.
""",encoding='utf-8')
print(json.dumps(dict(guidanceFiles=len(paths),checks=e['checks'],pairs=8,goal='active/incomplete')))
