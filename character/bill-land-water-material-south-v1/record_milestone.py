from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
v=json.loads((R/'output'/P.name/'validation.json').read_text());r=json.loads((P/'review.json').read_text());motion=json.loads((P/'capture-motion.json').read_text())
assert v['passed'] and r['checks']==4235 and r['failures']==0 and r['capturePairs']==218
review='Inspected four chronological native boards, four common-physical-scale source boards and28 guard presentations. South bare/helmet entry and independent exit visible at station scale; helmet neck/shoulder joins connected in inspected captures. Deep entry crouch remains muted/submerged; rising exit sources brighter than incoming normal walk. Pose/head/segment/detail continuity needs further master review. Native captures and safety checks do not establish full physical contact or continuous motion acceptance.'
r['visualReview']=review;(P/'review.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
motion['visualReview']='Chronological recorded native boards inspected; browser helmet/exit/quarter controls and replay verified, saved capture-motion-browser.png. Complete temporal/master/contact acceptance pending.'
(P/'capture-motion.json').write_text(json.dumps(motion,indent=2)+'\n',encoding='utf-8')
heading='Bill South paired native entry and independent exit — October 2, 2026'
body=f'''character/{P.name} stages SouthV2 nine-pose entry and independent SouthExitV2
eight-pose exit in both gears. Fixture-only renderer inherits current normal grid;
main copy changes only GridCanvas preload. Current normal Bill actor/player,
original room geometry, oxygen and safety retained. Graph-clear workshop vertical
route prescribed with mirrored starting end/first halfway turn so both boundaries
faceSouth; intermediateNorth leaves bridge inactive. Ten-second water rise/hold/
drain staged, not natural hydrology/job dispatch.

Native interval {v['seconds']}s:4235checks/0failures, {v['frozenInputs']}pre/post frozen inputs
stable; all {v['realProfileFileCount']}real non-log profile files unchanged, scratchAPPDATA.
190 advancing60Hz boundary captures plus28synthetic guard presentations:
218exact source/room pairs436PNGs and source inventory registrations. Gear/facing/
death/stage/clock-reversal/geometry takeovers return current normal texture and
clear fixture material. Both finite bridges complete on exact incoming gait phase.
Source union envelope gates admission/recheck, no collision-clear bypass.

South material head anchors follow source registered crowns, not North crowns.
Selected standing offset-58world and approximate proneSouth-4.4world, not North-12;
endpoint material/contact calibration remains provisional. Per-instance presentation
blends standing/swim waterlines at same actor root; source textures never mutated.
No normal candidate selection.

{review}

Eight finite APNG recorded-motion replays from exact190native room crops: normal/
quarter, both gears/transitions, fixed200square root-follow framing. Entry60..104
(45ticks),exit410..459(50ticks); cumulative60Hz timing rounded16/17ms, quarter4x.
Only equalRGBA crops coalesce, retaining tick/hold mapping. All decodedRGBA/holds/
loop1exact. Browserhelmet/exit/quarter controls exercised and screenshot saved.
Captured replay is not a new live interval or complete continuous review.

Lesson: axial studies need direction-specific head/pivot registration rather than
copied North offsets. Mirrored prescribed route preserves real collision geometry
and controller while exercising correct cardinal admission. Source decode, runtime
safety and native master/contact acceptance remain separate. Passing counters do
not remove visible matte/head/proportion discrepancies.

Next South master/material/pose/contact/motion refinement, scratch checkpoint and
TitleContinue parity, normal admission/cargo lifecycle and full-library polish.
Full Bill goal active/incomplete. Preview capture-motion.html.
'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
 with f.open('rb') as stream:stream.seek(max(0,f.stat().st_size-131072));tail=stream.read()
 if heading.encode() not in tail:
  with f.open('a',encoding='utf-8') as stream:stream.write('\n## '+heading+'\n\n'+body+'\n')
(P/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October2,2026 · Bill South native transitions\n\n## Objective and acceptance\nFull Bill set matching masters and entire-library consistency/polish. Active/incomplete.\n\n## Accepted decisions\nNormal actor/player; fixture-only independent paired transitions; real geometry/oxygen/safety; scratch saves/frozen interval.\n\n## Current state\n'+body+'\n## Changed files\nprepare.py, grid.gd/view.gd/fixture_main.gd with pairedUIDs, fixture.tscn, inventory/freeze, test and runner, build_review.py/build_capture_motion.py, captures/boards/reports, replays/browser screenshot; six guidance files.\n\n## Verification\n4235/0;218exact pairs;2001stableinputs;2931owner files unchanged. Eight chronological boards and28guards inspected. Full master/contact/motion pending.\n\n## Next action\nSouth master/grade/contact refinement and checkpoint/TitleContinue; normal admission and complete library polish.\n',encoding='utf-8')
print(json.dumps(dict(checks=r['checks'],pairs=r['capturePairs'],guidanceFiles=len(paths),goal='active/incomplete')))
