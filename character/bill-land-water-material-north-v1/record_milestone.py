from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
e=json.loads((P/'review.json').read_text(encoding='utf-8'));v=e['validation']
assert v['passed'] and not v['frozenInputChanges'] and not v['realProfileChanges']
heading='Bill North native entry and interruption evidence — October 2, 2026'
body=f'''Fixture-only character/{P.name} stages NorthV3 nine-pose bare/helmet
entry on the actual current Bill actor and normal bill_carry_player. Current main
copied with only fixture GridCanvas preload changed. Prescribed vertical actual
workshop graph route and ten-second water rise/hold/drain retain normal navigation,
medium selection and oxygen/failure rules. Dynamic outgoing/incoming normal gait
frames, union-pose clearance admission/recheck, finite500ms target-phase rebind.
Normal dry return remains unchanged; no independently authored North exit yet.

{e['checks']}native checks,0failures/{v['seconds']}seconds; one entry admission and exact
normal swimming completion per gear. Ninety advancing60Hz boundary captures plus
fourteen active/takeover presentations: gear/facing/death/stage/clock/local blocker.
All{e['capturePairs']}source-room pairs identify exact frozen decoded source registration.
{v['frozenInputs']}targeted code/source inputs stable; all{v['realProfileFileCount']}owner non-log files
unchanged under scratchAPPDATA. Initial3069-check interval passed mechanics but
inventory missed normal helmet walking; retained logs/profile/records superseded
for complete prelaunch source coverage by the corrected rerun. No inferred fallback.

Visual review: {e['visualReview']}
Captured room images establish native context, not continuous motion acceptance.
Source head-centre material bias remains provisional; normal endpoint/master grade,
full floor/water contact, checkpoint/TitleContinue, independent North exit, South
bridges, normal admission/cargo lifecycle and cross-family polish remain open.

Lesson: axial fixture source inventories must include the base normal runtime
helmet/dry banks as well as directional overrides. Exact source identity should
be checked against every advancing and takeover capture; a successful mechanics
run cannot certify an omitted source dependency. Freeze before launch, retain the
incomplete interval and rerun with corrected coverage rather than backdating proof.
Source comparison boards project every captured image through its recorded pivot
and standing-height metadata onto one shared physical canvas. Per-file thumbnail
fitting falsely makes padded transition art smaller than normal gait art; never
use that presentation to judge size continuity. Native room crops retain fixed
pixel scale and follow the recorded root; full screenshots preserve world context.
Review: character/{P.name}/index.html. Full Bill objective active/incomplete.
'''
for relative,prepend in [('docs/CURRENT_STATUS.md',True),('docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',True),('docs/ASSET_PIPELINE_AND_WORKFLOW.md',False),('docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',False),('skills/brinespace-character-pipeline/references/crew-consistency.md',False)]:
 f=R/relative;s=f.read_text(encoding='utf-8');entry='## '+heading+'\n\n'+body+'\n'
 if heading not in s:f.write_text(entry+s if prepend else s+'\n'+entry,encoding='utf-8')
f=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
s=f.read_text(encoding='utf-8')
if heading not in s:f.write_text(s+'\n## '+heading+'\n\n'+body+'\n',encoding='utf-8')
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 2, 2026 · Project: {R} · Task: Bill North native entry

## Objective and acceptance
Complete Bill's full animation set matching masters, camera, proportions and matte
grade, then cross-family polish. This fixture is one evidence milestone.

## Accepted decisions and constraints
Existing masters/source NorthV3 preserved. Fixture only; actual current actor and
normal player. Owner data isolated. No source reversal standing in for new exit.

## Current state
prepare.py generates grid/view/current-main fixture, paired native test/runner,
prelaunch targeted-inputs and decoded source inventory. build_review.py publishes
actual captures; review.json and index.html retain evidence. No production selection.

## Verification
{e['checks']}checks/0failures; {e['capturePairs']}exact source-room pairs; {v['frozenInputs']}inputs stable;
{v['realProfileFileCount']}owner files unchanged. {e['visualReview']}
Full motion/contact/master acceptance and save/Continue still pending.

## Next action
Resolve observed visual limitations, author independent North exit and test full
North transition lifecycle; South bridges, normal admission and entire-set polish.
''',encoding='utf-8')
print(json.dumps(dict(guidanceFiles=6,handoff=True,goal='active/incomplete')))
