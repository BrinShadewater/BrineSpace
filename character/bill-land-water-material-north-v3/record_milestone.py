from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;EXIT=P.parent/'bill-water-exit-north-v1'
e=json.loads((P/'review.json').read_text(encoding='utf-8'));v=e['validation'];b=json.loads((EXIT/'browser-review/review.json').read_text(encoding='utf-8'))
assert v['passed'] and not v['frozenInputChanges'] and not v['realProfileChanges']
heading='Bill North paired native entry-exit and sampled motion — October 2, 2026'
body=f'''Fixture-only character/{P.name} stages tested NorthV3 nine-pose entry
and independently authored NorthExitV1 eight-pose exit, both bare/helmet,500ms each.
Actual current normal Bill actor/player, real workshop navigation/clearance/medium/
oxygen rules, prescribed ten-second water rise/hold/drain. Source-bound blended
dry/swim waterline retained. Dynamic exact outgoing/incoming gait phases, finite
completion/rebind and union pose envelope admission/recheck remain authoritative.

{e['checks']}native checks/0failures in{v['seconds']}seconds; one admission/completion each
entry/exit per gear with exact normal terminal source.190advancing60Hz boundary
views plus28active/takeover views, all{e['capturePairs']}source-room pairs identify frozen decoded
registration. Gear/facing/death/stage/clock/local blocker clears bridge/material.
Intermediate actual South route keeps North-only bridge inactive. {v['frozenInputs']}prelaunch
targeted code/source files stable; all{v['realProfileFileCount']}owner non-log files unchanged.

Initial route failed exit assertions because actual controller had turned South
before draining boundary. Isolated real per-frame trace proves128world-unit clear
vertical segment, North entry and South return, no North exit admission. Failed
native source/room captures/log/profile/frozen map retained in failed-route-v1;
69.3second trace also retains2004stable inputs and2931owner files unchanged.
Revised initial path turns halfway along the SAME clear segment first, then South,
then North across exit. Explicit subset clearance and actual South-inactivity checks
added. No room geometry, movement speed, medium rules or animation guard weakening.

Actual source-browser controls exercised exit at normal/quarter speed both gears:
{b['samples']}advancing screenshots; quarter labels1..7both gears, normal bare3..7/helmet4..7.
All four cases reach7; initial0 separately paused. AX sampled before screenshot can
cross hold boundary; no exact source-phase pixel binding or full normal chronology/
duration claim. Same fixed screen crop per pose, progressing board inspected:
connected canonical helmet/collar, modest bare head/metal-grade variation remains.

Native visual review: {e['visualReview']}

Lesson: observe actual facing at the medium boundary before diagnosing a missing
directional bridge. A correctly guarded bank can remain inactive because the test
route turned. Preserve failing trace/captures, adjust only the prescribed path inside
validated existing geometry, and assert the intervening direction remains excluded.
Source moving evidence and real native contact/material/safety evidence stay distinct.

Next full North moving/contact/master polish and checkpoint/TitleContinue; South
bridges, normal admission/cargo lifecycle and full cross-family consistency remain.
Full Bill objective active/incomplete. Review:character/{P.name}/index.html.
'''
entry='## '+heading+'\n\n'+body+'\n'
for relative,prepend in [('docs/CURRENT_STATUS.md',True),('docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',True),('docs/ASSET_PIPELINE_AND_WORKFLOW.md',False),('docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',False),('skills/brinespace-character-pipeline/references/crew-consistency.md',False)]:
 f=R/relative
 with f.open('rb') as stream:
  first=stream.read(131072);stream.seek(max(0,f.stat().st_size-131072));last=stream.read()
 if heading.encode() not in first+last:
  with f.open('a',encoding='utf-8') as stream:stream.write('\n'+entry)
f=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md');s=f.read_text(encoding='utf-8')
if heading not in s:f.write_text(s+'\n'+entry,encoding='utf-8')
old=json.loads((EXIT/'exit-review.json').read_text(encoding='utf-8'));old['browserMotionReview']=b;old['nativeCandidateReview']='res://character/bill-land-water-material-north-v3/review.json';old['normalSelected']=False
(EXIT/'exit-review.json').write_text(json.dumps(old,indent=2)+'\n',encoding='utf-8')
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 2, 2026 · Project: {R} · Task: Bill North paired transitions

## Objective and acceptance
Full Bill animation set matching masters, camera, proportions and matte grade,
then entire-set consistency/polish. This staged milestone leaves goal active.

## Accepted decisions and constraints
Independent exit, current normal actor/player, source registration/pivots retained.
Fixture only; owner profile isolated. Original room/speed/failure rules preserved.

## Current state
prepare.py stages9pose entry/8pose exit paired banks and actual current main.
test/runner freeze2002inputs. build_review.py publishes chronological native/source
boards and guards. prepare_trace.py retains original South-at-exit route diagnosis.
Exit browser-review contains71advancing screenshots and sampled moving board.

## Verification
{e['checks']}checks/0failures,{e['capturePairs']}exact source-room pairs,{v['frozenInputs']}inputs stable,
{v['realProfileFileCount']}owner files unchanged. {e['visualReview']}
Normal motion/master acceptance, full contact and checkpoint/Continue pending.

## Next action
North full motion/contact/master refinement and checkpoint/TitleContinue, then
South bridges, normal admission/cargo lifecycle and full-library polish.
''',encoding='utf-8')
print(json.dumps(dict(guidanceFiles=6,checks=e['checks'],pairs=e['capturePairs'],goal='active/incomplete')))
