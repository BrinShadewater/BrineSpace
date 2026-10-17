from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;D=P/'title-checkpoint-review'
e=json.loads((D/'review.json').read_text(encoding='utf-8'))
assert e['validation']['passed'] and e['nativeChecks']==252
assert len(e['comparisonPairs'])==8 and all(x['sourceRGBAExactToPrior'] and x['registeredRoomCropRGBAExactToPrior'] for x in e['comparisonPairs'])
assert e['targetedInputChanges']==['scripts/james_cargo_actor.gd']
e['visualReview']='All eight new native presentations viewed against eight historical fresh-scene references in title-comparison.png. Source RGBA,240x220 physical-root-registered room crops and recorded root/state/facing/bridge/material/head offsets byte/value-exact. Whole-scene frames are not byte-exact; historical UI/profile differences outside crop visible. Raw source thumbnails are not common-pivot registered. No new motion/master/contact or normal admission acceptance.'
e['concurrentInputChange']={'path':'scripts/james_cargo_actor.gd','before':e['targetedPrelaunchSHA256']['scripts/james_cargo_actor.gd'],'after':hashlib.sha256((R/'scripts/james_cargo_actor.gd').read_bytes()).hexdigest(),'scope':'Concurrent inactive James actor source changed during group.16other targeted files stable. No full prelaunch dependency freeze/per-process James version proof; all four actual fresh-process restore intervals passed, Bill endpoints/crops exact.'}
(D/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
seconds=round(sum(x['seconds'] for x in e['validation']['intervals']),2)
note=f'''## Bill East staged new-process title Continue bridge — October 2, 2026

Four independent native processes, actual title Continue button, loading
transmission/Continue button and normal main pending checksum restoration.
Current title copied with only GAME_SCENE changed; current main copied with only
grid preload changed. Derived staged ready hook adds view and validates/rebuilds
the exact bridge after normal actor/world/clock restoration. Four existing normal
checksum saves sealed with resource-free staged_bill_water_bridge envelope;
paired title gate checks saved root/gear/clock/playback before calling normal
Continue. Loaded source/bank/metadata/collision codec checks remain afterward.
No normal production optional-field or renderer/source selection installation.

252 native checks0fail across four processes; four envelopes sealed/normal codec
compatible in separate headless interval. Five engine0 intervals/{seconds}s sum,
scratch APPDATA/all2931owner non-log files unchanged.160 subsequent60Hz ticks
check actual survival and exact terminal normal gait source; not all per-tick
trajectory comparisons or native capture every tick. Eight native/source endpoint
presentations retained and inspected against prior fresh-scene references.
All eight source RGBA,240x220 native room crops registered to physical root/camera,
recorded root/state/facing/bridge/material/head offsets exact. Whole-scene images
are not exact: historical UI/profile differences outside these registered crops
remain visible. Raw source thumbnails unregistered; no per-pose normalization.

Sixteen of17targeted prelaunch/post files stable; concurrent inactive James actor
changed during group, pre/post hashes recorded. Not a full dependency freeze or
per-process James version proof. Historical fixtures/saves and normal actor work
preserved. Source art/scale/pivots/master style unchanged; no full continuous
motion/contact/head/wake/support/natural scheduling acceptance inferred.

Lesson: exercise title button, loading acknowledgement and pending-world restore
in a separate process before claiming Continue. Keep staged extensions clearly
distinct from production admission. Report registered actor/room crop equality
separately from whole-scene/profile/UI equality and concurrent dependency drift;
do not repaint matching character art to hide unrelated screen differences.
Next normal guarded paired source/save admission after visual/contact acceptance,
other cardinal water bridges, cargo lifecycle and full Bill master/style/grade/
proportion/cross-family polish. Full goal active/incomplete, no commit/export.
Review:character/bill-land-water-material-east-v3/title-checkpoint-review/index.html.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 f=R/rel;text=f.read_text(encoding='utf-8')
 if heading not in text:f.write_text(note+text,encoding='utf-8')
for f in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 text=f.read_text(encoding='utf-8')
 if heading not in text:f.write_text(text+'\n'+note,encoding='utf-8')
(D/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Bill staged title Continue

## Objective and acceptance
Full master-consistent Bill set then cross-family consistency/polish. Still open.

## Accepted decisions and constraints
Preserve sources/scale/pivots/gameplay/owner saves. Staged title/source/view/bridge
hooks are explicit, no production source/save admission. No source repaint for UI.

## Current state
title_bridge_envelope.gd/UID; title_fixture/title_fixture_main and paired UIDs;
copied current title/base-main+UIDs and scenes; seal_title_checkpoints.gd/UID;
prepare_title_checkpoint.py; native test/UID/five-interval scratch runner;
build_title_checkpoint_review.py; four checksummed envelopes/eight native-source
views/comparison/review.json. Status/pipeline/bible/maintained-installed skill updated.

## Verification
252native checks0fail,4independent title/loading Continue processes plus sealing.
Five engine0 intervals/{seconds}s sum;2931owner files unchanged.
All8source RGBA/registered240x220 room crops/root/state/facing/material fields
exact to historical fresh-scene endpoints.8new native views reviewed; whole
screens not exact outside crops.160future ticks survival/terminal-source checks,
not full per-tick trajectory/native capture.16targeted files stable; concurrent
inactive James actor changed, recorded hashes; no full dependency/version freeze.

## Next action
Continuous physical water/contact/head/wake/support acceptance and other cardinal
bridges. Guarded normal paired source/save admission after that review. Cargo
lifecycle/full-set/master/style/grade/proportion/cross-family polish remain.
Goal active; no live processes/commit/export.
''',encoding='utf-8')
print('Recorded staged new-process title Continue and registered-crop evidence.')
