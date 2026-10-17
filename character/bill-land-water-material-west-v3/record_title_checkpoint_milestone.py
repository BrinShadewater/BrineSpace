from pathlib import Path
import json

P=Path(__file__).resolve().parent
R=P.parent.parent
D=P/'title-checkpoint-review'
e=json.loads((D/'review.json').read_text(encoding='utf-8'))
assert e['validation']['passed'] and not e['targetedInputChanges']
assert len(e['comparisonPairs'])==8
assert all(x['sourceRGBAExactToPrior'] and x['registeredRoomCropRGBAExactToPrior'] for x in e['comparisonPairs'])
e['visualReview']='All eight new-process native endpoints inspected against prior fresh-scene captures. Exact source pixels and registered240x220 room crops; root/state/facing/material/head fields exact. Full continuous motion/master/contact acceptance remains pending.'
e['failedInterval']='Initial sealing passed; first native launch stopped at parser duplicate variable path in inserted raw-bank check. No native visual evidence from that interval. Logs, test and input inventory retained under output/bill-land-water-title-checkpoint-west-v1/parser-failed-v1. Renamed raw_path; full group rerun.'
(D/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
seconds=round(sum(x['seconds'] for x in e['validation']['intervals']),2)
whole=sum(x['roomRGBAExactToPrior'] for x in e['comparisonPairs'])
count=len(e['targetedPrelaunchSHA256'])
note=f'''## Bill West new-process Title Continue for entry/independent exit — October 2, 2026

Four independent native launches exercise actual title Continue button, loading
acknowledgement and normal pending checksum world/actor restoration, then staged
bridge-ready admission. Current title differs only in scene redirect; current
base main differs only in grid preload. Derived fixture hook adds source-bound
view and bridge. Four retained normal saves sealed with resource-free staged
envelopes after paired root/gear/clock/playback gate. Loaded current main/grid
paths and all28 candidate-bank frame pixels explicitly verified in each launch.
No normal production source/save installation; this remains staged evidence.

{e['nativeChecks']}native checks0fail in four independent processes plus separate
headless sealing, five passing intervals/{seconds}s cumulative. Scratch APPDATA,
all{e['validation']['realProfileFileCount']}owner non-log files unchanged;
{count}targeted prelaunch/post inputs stable including current normal source banks,
candidate banks, captured references and save/sidecar bytes. Not all transitive
project dependencies. Initial first native parser failure preserved; raw-bank
variable renamed raw_path and full group rerun, without relaxing visual gates.

Eight new native/source endpoints visually compared with reviewed fresh restores.
All eight source RGBA, physical-root/camera registered240x220 native crops and
root/state/facing/bridge/material/head fields exact. Whole-scene exact pairs:
{whole}/8, separately reported rather than inferred from actor crops.160 future60Hz
updates check survival and terminal exact normal gait source; this separate-process
test does not compare all per-tick trajectory fields or capture every native tick.
Earlier fresh-scene evidence supplies its own scoped per-tick trajectory checks.

Lesson: an independent exit needs its own new-process restore proof. Keep current
loaded-bank pixel checks inside actual Title Continue runs, not only in unused
fixture helpers. Separate staged admission from production installation and actor
crop equality from complete screen equality. A matching restoration does not
repair normal endpoint suit-detail/face/material differences or certify motion.

Review:character/bill-land-water-material-west-v3/title-checkpoint-review/index.html.
Next continuous native/source motion and master/normal-endpoint matching, remaining
North/South water transitions, guarded normal admission, cargo lifecycle and full
Bill cross-family style/perspective/scale/height/proportion/grade/loop polish.
Full goal active/incomplete; no commit/export.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    f=R/rel;current=f.read_text(encoding='utf-8')
    if heading not in current:f.write_text(note+current,encoding='utf-8')
for f in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    current=f.read_text(encoding='utf-8')
    if heading not in current:f.write_text(current+'\n'+note,encoding='utf-8')
(D/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October2,2026 · Project: BrineSpace · Task: Bill West new-process Continue

## Objective and acceptance
Full master-matched Bill set, then cross-family consistency and polish. Incomplete.

## Accepted decisions and constraints
Normal actor/save/world rules retained, fixture-only source/view/bridge envelope.
Preserve masters, scale/pivots and owner profile; scratch tests and exact comparisons.

## Current state
prepare_title_checkpoint.py, staged title/main/gate/sealer with paired UIDs/scenes,
native test/UID, runner,555-input inventory, publisher/recorder, four sealed saves,
eight native/source views, comparison and review.json. Six guidance files updated.

## Verification
{e['nativeChecks']}native checks0fail; four separate native Title/loading Continue
processes plus sealing/{seconds}s;2931owner files unchanged;{count}inputs stable.
Eight source/registered native crops and root/state/material fields exact, reviewed.
Whole screens {whole}/8exact.160future ticks survival and exact final gait,
not every per-tick trajectory/native image. Parser-failed interval preserved.

## Next action
Continuous motion/master/normal-endpoint review, remaining North/South water
bridges, guarded normal admission, cargo lifecycle and full-set consistency/polish.
No production installation/commit/export; goal active.
''',encoding='utf-8')
print(json.dumps({'nativeChecks':e['nativeChecks'],'stableInputs':count,'wholeSceneExactPairs':whole,'recorded':True}))
