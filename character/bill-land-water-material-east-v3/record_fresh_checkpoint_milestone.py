from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;D=P/'fresh-checkpoint-review'
e=json.loads((D/'review.json').read_text(encoding='utf-8'))
assert e['validation']['passed'] and e['failures']==0 and not e['targetedInputChanges']
assert len(e['freshRestores'])==4 and all(x['roomExact'] and x['sourceExact'] for x in e['nativeSourcePairs'])
e['visualReview']='All16 native immediate/future before-after presentations inspected in fresh-before-after.png. Eight native/source pairs byte-exact. No master-motion, natural contact, full-family or normal admission acceptance inferred.'
e['priorIntervals']='First87.09s interval retained: obsolete cargo recorder field plus historical copied-main/current James restore mismatch. Second295.11s/781checks4fail retained: actor/source/material future parity passed but all four later native comparisons differed under asymmetric paused updates. Final run uses current-main one-preload fixture and equal paused update calls on both branches; strict native equality retained.'
(D/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
note=f'''## Bill East water bridge fresh actor/world restoration — October 2, 2026

Four actual normal checksum RunSave write/read/restore_staged passes into fresh
same-process scenes and normal Bill actors, entry/exit/both gears. Separate staged
resource-free bridge sidecar admitted only after actual world/actor/visual clock
restoration; no normal optional save field or title/new-process Continue wiring.
Forty subsequent60Hz ticks per case compare exact foot/facing/state/medium/needs,
oxygen/tank/source/material/head offset/bridge activity through normal gait return.
Sixteen native immediate/terminal presentations; all eight native/source before-
after pairs byte-exact and inspected. No native image for every future tick.

Final {e['checks']}checks0fail/{e['validation']['seconds']}s/engine0, scratch APPDATA,
all2931owner non-log files unchanged. Seventeen targeted prelaunch/post source
hashes stable; actual current-main fixture differs only in grid preload. Historical
fixtures preserved. No full dependency/artwork freeze or normal admission.

First87.09s interval failed obsolete cargo-only recorder field and copied-main
predating concurrent James actor/restore integration; preserved. Second295.11s,
781checks4fail: all actor/source/material future comparisons passed, four whole-
scene future native comparisons failed. Paused scene update was called only on
restored branch, updating lighting there. Both branches now capture paused and
receive equal paused update calls; all strict native comparisons pass, no pixel
tolerance/lighting override introduced. Both failed intervals and images retained.

Lesson: fresh restoration must use a compatible current actor factory, player and
save codec together. Preserve historical fixtures, create a new narrowly changed
current fixture. Drive paused render updates equally before interpreting scene
pixel differences as source-grade drift; preserve strict comparison and evidence.
Master artwork/scale/pivots unchanged. Full motion/support/contact/water/wake and
natural priority/hydrology acceptance remain open. Next title/new-process paired
bridge admission and other cardinals; cargo lifecycle and full Bill source/master/
grade/proportion/cross-family polish remain. Goal active/incomplete, no commit/export.
Review:character/bill-land-water-material-east-v3/fresh-checkpoint-review/index.html.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 f=R/rel;text=f.read_text(encoding='utf-8')
 if heading not in text:f.write_text(note+text,encoding='utf-8')
for f in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 text=f.read_text(encoding='utf-8')
 if heading not in text:f.write_text(text+'\n'+note,encoding='utf-8')
(D/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Bill fresh water restore

## Objective and acceptance
Complete master-consistent full Bill set then cross-family consistency/polish.
Current staged East bridge does not complete that scope.

## Accepted decisions and constraints
Preserve normal actor rules, original art/scale/pivots and owner saves. Separate
staged sidecar, no normal save schema/source selection change. Fair paused updates.

## Current state
prepare_fresh_checkpoint.py; fresh_fixture_main.gd/UID and scene/current main
one-grid-preload copy; fixture/17targeted input hashes; native test/UID/scratch
runner; build_fresh_checkpoint_review.py; four base saves/sidecars and16 paired
native views/review.json. Pipeline/bible/status/maintained-installed skill updated.

## Verification
{e['checks']}native checks0fail/{e['validation']['seconds']}s/engine0;2931owner files unchanged.
Four fresh scenes/normal actors/worlds restored via actual checksum RunSave.
160 future ticks physical/medium/needs/oxygen/source/material/bridge parity.
All16 native views inspected;8 native/source pairs exact.17targeted hashes stable.
Two failed intervals retained; cargo recorder/current-factory and asymmetric
paused lighting calls corrected. Native equality gate retained.

## Next action
Actual title/new-process Continue and paired optional bridge integration, then
other cardinal transitions. Natural hydrology/priorities and continuous physical
contact/wake/support acceptance remain, as do cargo lifecycle and full master/
style/grade/proportion/cross-family polish. Goal active. No commit/export.
''',encoding='utf-8')
print('Recorded fresh scene water restore and fair paused-render lesson.')
