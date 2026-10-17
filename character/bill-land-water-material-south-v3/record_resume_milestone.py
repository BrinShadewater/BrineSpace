from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;D=P/'fresh-checkpoint-review'
fresh=json.loads((D/'review.json').read_text(encoding='utf-8'));v=fresh['validation']
assert v['passed'] and fresh.get('visualReview') and not fresh['targetedInputChanges'] and not v['realProfileChanges']
assert all(x['roomExact'] and x['sourceExact'] for x in fresh['nativeSourcePairs'])
heading='Bill South fresh-scene water transition restoration - October 2, 2026'
body=f"""Four actual normal checksum RunSave disk write/read/restore_staged cases exercise South entryV2 pose4/tick81 and revised independent exitV4 pose5/tick432, bare/helmet. Fresh current-main scenes and normal actors/player; real navigation, oxygen and medium rules. Fixture resource-free transition sidecar admitted only after actor/world/clock restore and bank/source/extent/phase validation. Eight malformed kinds per case reject without mutating admitted state.

{fresh['checks']}checks/0failures in {v['seconds']} seconds;160future60Hz ticks compare root/facing/state/medium/needs/oxygen/source/material/head offset/bridge activity. Eight exact before-after native/source pairs,16native presentations including exact terminal normal gait. {fresh['frozenInputCount']} inputs stable; all {v['realProfileFileCount']} owner non-log files unchanged under scratch APPDATA.

Visual review: {fresh['visualReview']}

Initial1449/1 interval failed only a portrait-strip rectangle [63,100,160,148],4420RGBpixels; all source/future comparisons and seven other full-scene pairs passed. Root evidence retained in output/bill-land-water-fresh-checkpoint-south-v1/failed-roster-readiness-v1. Actual CrewPortraitPanel refresh plus observed restored membership readiness fixes fixture capture timing; whole-scene equality remains required. No production UI code changed.\n\nLesson: wait for restored visible UI membership as well as actor/room submissions before full native screenshot parity. Do not hide the UI or reduce comparison coverage to bypass unrelated stale render state. Source revision resume evidence must exercise the actual revised pose rather than an unchanged endpoint. Keep current directional bank signatures, material/crown registration and incoming normal phase with a resource-free sidecar; restore actual world and actor before admission. Mirrored South route retains real geometry. Exact restoration is independent of full master/contact/motion acceptance.

Next separate new-process South TitleContinue, remaining cardinal master/contact/motion review, normal admission/cargo lifecycle and full-library consistency/polish. Full Bill goal active/incomplete. No normal candidate selection.
"""
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
 with f.open('rb') as stream:stream.seek(max(0,f.stat().st_size-131072));tail=stream.read()
 if heading.encode() not in tail:
  with f.open('a',encoding='utf-8') as stream:stream.write('\n## '+heading+'\n\n'+body+'\n')
(D/'HANDOFF.md').write_text('# Project handoff\n\n## Objective\nFull Bill set matching masters and full-library polish; active/incomplete.\n\n## Accepted decisions\nFixture-only bridge after normal world restoration; scratch saves, original source density/camera/geometry, normal selections retained.\n\n## Current state\n'+body+'\n## Changed files\ncheckpoint.gd and pairedUID; fresh_fixture_main.gd/UID/scene; prepare_fresh_checkpoint.py, fresh test/UID and runner; build_fresh_checkpoint_review.py, captures/disk saves/source sidecars/reports; six guidance files.\n\n## Verification\n'+str(fresh['checks'])+'/0; eight native/source pairs exact;160futureticks exact; isolated owner profile unchanged.\n\n## Next action\nActual title Continue in new processes, full master/contact/motion and normal admission, then complete cross-family polish.\n',encoding='utf-8')
print(json.dumps(dict(checks=fresh['checks'],guidanceFiles=6,nativePairs=8,goal='active/incomplete')))
