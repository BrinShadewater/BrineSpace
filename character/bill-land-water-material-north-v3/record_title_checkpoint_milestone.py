from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;D=P/'title-checkpoint-review'
e=json.loads((D/'review.json').read_text(encoding='utf-8'));v=e['validation'];pairs=e['comparisonPairs']
assert v['passed'] and not v['frozenInputChanges'] and not e['targetedInputChanges'] and not v['realProfileChanges']
assert len(pairs)==8 and all(x['sourceRGBAExactToPrior'] and x['registeredRoomCropRGBAExactToPrior'] for x in pairs)
assert e.get('visualReview')
seconds=round(sum(x['seconds'] for x in v['intervals']),2);whole=sum(x['roomRGBAExactToPrior'] for x in pairs);count=len(e['targetedPrelaunchSHA256'])
heading='Bill North independent-process Title Continue — October 2, 2026'
body=f"""Four independent native launches restore bare/helmet North entry and independently
authored exit through actual title Continue callbacks, loading acknowledgement
and current main pending checksum world/actor restore. Current title copied with
only game-scene redirect; current base main with only grid preload redirect.
Derived fixture gate/view/ready hook admits resource-free source-bound sidecar
only after normal restore. Exact current normal Bill actor/player and all34loaded
North9entry/8exit source frame pixels verified per launch. Not production wiring.

{e['nativeChecks']}native checks/0failures; five passing intervals (sealing plus four
independent native processes),{seconds}s cumulative. {count}prelaunch/post targeted
inputs stable, including transitive scanned code and prior source/native reference
captures and saved sidecar bytes; not every unrelated artwork in the project.
{v['realProfileFileCount']}owner non-log files unchanged under scratchAPPDATA.
Eight new source RGBA and root/facing/state/bridge/material/head fields exact to
reviewed fresh-scene endpoints. All eight registered240x220 native room crops
byte-exact. Whole-scene equality {whole}/8, reported separately.160future60Hz ticks
check survival and exact terminal normal gait; not all per-tick trajectories or
native capture every tick. Earlier fresh-scene test has separate scoped trajectory
proof. Visual review: {e['visualReview']}

Lesson: cover both axial entry and independent exit in new-process Continue, with
current bank pixels and actor identity checked inside actual restored scene.
Freeze native reference images and records as well as sources/checkpoint bytes
before launch. Separate matching actor crops from full-screen differences, and
fixture admission from normal catalog/save wiring. Save fidelity cannot certify
master grade, anatomy, ground contact or continuous smoothness.

Next full North moving/contact/master polish, South entry/exit, guarded normal
admission/cargo lifecycle and entire-library consistency/polish. Full Bill goal
active/incomplete. Review: character/{P.name}/title-checkpoint-review/index.html.
"""
entry='\n## '+heading+'\n\n'+body+'\n'
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
 with f.open('rb') as stream:stream.seek(max(0,f.stat().st_size-131072));tail=stream.read()
 if heading.encode() not in tail:
  with f.open('a',encoding='utf-8') as stream:stream.write(entry)
(D/'HANDOFF.md').write_text(f"""# Project handoff

Updated: October2,2026 · Project: {R} · Task: Bill North new-process Continue

## Objective and acceptance
Full master-matched Bill animation set then cross-family consistency/polish.
Goal incomplete; staged restoration evidence does not certify visual/normal admission.

## Accepted decisions and constraints
Current title/main/normal actor/world restore retained; fixture-only redirects,
source/view/sidecar gate. Original master sources/pivots/material rules retained.
ScratchAPPDATA and full owner fingerprints; no owner saves or selections changed.

## Current state
prepare_title_checkpoint.py and copied/derived title/main/gate/sealer scripts with
paired UIDs/scenes; native test/runner; {count}-input inventory; publisher/recorder.
Four sealed normal-compatible saves, eight native/source captures and comparisons.

## Verification
{e['nativeChecks']}native checks/0failures; four independent native launches plus
sealing/{seconds}s total. {count}inputs stable;{v['realProfileFileCount']}owner files unchanged.
Eight source/native registered crops exact; whole screens {whole}/8exact.
160future ticks survival and exact normal terminal source; separate trajectory scope.
{e['visualReview']}

## Next action
Full motion/contact/master polish, South entry/exit, guarded normal admission,
cargo lifecycle and full-library consistency/polish. No commit/export; goal active.
""",encoding='utf-8')
print(json.dumps(dict(nativeChecks=e['nativeChecks'],stableInputs=count,wholeScenePairs=whole,guidanceFiles=len(paths),goal='active/incomplete')))
