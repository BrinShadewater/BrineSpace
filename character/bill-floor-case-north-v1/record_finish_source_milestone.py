from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
v=json.loads((R/'output/bill-floor-case-finish-plan-v1/validation.json').read_text());s=json.loads((P/'finish-source-evidence.json').read_text());assert v['passed'] and s['passed']
note='''## Bill finite ordinary North set-down exit study — October 2, 2026

New unselected finish_plan.gd continues the remaining exact authored North unload
sources after an ordinary service cancellation. Requires canonical release cue,
actual displayed source/gear/live stow clock; rejects arrival/turn prefixes and
extended service terminal hold. Keeps elapsed current hold and original remaining
clock, ends at .64seconds authored unload rather than restarting or retaining2s.
No actor art, grading, normal controller/selection or gameplay changes.

765headless source-clock checks0fail/6.36s/engine0. All14authored interiors/both
gears retain exact entrance texture, unchanged original plan and future source
sequence; wrong clock/gear/missing plan/extended hold rejected. Scratch APPDATA;
all2931owner non-log files unchanged. These are planner tests, not live service exits.

Eight lossless APNG source-only previews: cuts1/4/7/10both gears, remaining first
hold, exact original RGBA and durations;10189decoded/opaque-idle-body checks pass.
Terminal preview composes independent case behind unchanged original idle; not
replacement body art. Two registered source boards viewed at full and65.28/148
density. Helmet/head/detail/matte preserved by reuse; terminal boots/stance still
change visibly into idle and need native motion/contact review. APNG600ms viewer
terminal hold/repeat is not runtime behavior. No continuous-film acceptance.

Lesson: ordinary service cancellation can finish already-authored contact/rise
from the actual source clock; restarting a clip invents a jump. Do not use this
finite ordinary exit to delay fire/flood/death/gear priority. Those need separate
disposition and real-world tests. Next staged actor/player exit integration with
normal needs/hazard update, root/floor ownership, priority cancellation and ordinary
Continue, then normal admission/remaining full-set/cross-family master polish.
Full goal active/incomplete. Review:character/bill-floor-case-north-v1/
finish-source-review.html; FINISH_SOURCE_HANDOFF.md. No commit/export.

'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 old=path.read_text(encoding='utf-8');assert note.splitlines()[0] not in old;path.write_text(note+old,encoding='utf-8')
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 with path.open('a',encoding='utf-8') as f:f.write('\n\n'+note)
(P/'finish-plan-evidence.json').write_text(json.dumps({'validation':v,'checks':765,'sourceEvidence':'finish-source-evidence.json','boardsViewed':2,'continuousMotionReviewed':False,'normalSelection':False,'postRunHelperHash':hashlib.sha256((P/'finish_plan.gd').read_bytes()).hexdigest()},indent=2)+'\n')
(P/'FINISH_SOURCE_HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill ordinary North exit

## Objective and acceptance
Complete Bill set matching masters/style/perspective/size/proportions/matte grade,
then full cross-family consistency/polish. Full goal active, incomplete.

## Accepted decisions and constraints
Ordinary service exit may finish remaining already-authored set-down/rise. Do not
delay hazards, gear or mortality. Original actor art and selected controller retained.

## Current state
finish_plan.gd+UID, source-clock fixture/runner, lossless motion/source review builder,
eight APNG previews and two registered boards. Planner starts on actual source/clock
and ends at authored .64s. Arrival prefixes/other-direction exits remain separate.

## Verification
765headless checks pass;2931owner non-log files unchanged under scratch APPDATA.
10189lossless-decoding/opaque-master-idle preservation checks. Both boards viewed.
Boot stance changes into idle; contact/join requires native continuous motion.
Source-only study: no actual cancelled actor, normal selection or Continue admission.

## Next action
Integrate staged finite exit through ordinary actor/player, preserving ongoing needs
and priority dispatch. Bind floor release to that program, prove actual interruption,
fixed root, shared-room rendering and checkpoint/Continue; then normal admission and
remaining equipment/motion families/full-library master/color consistency pass.
''',encoding='utf-8')
print('Finite-exit study handoff, status, pipeline, bible and both skill copies updated.')
