from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
v=json.loads((R/'output'/P.name/'validation.json').read_text())
r=json.loads((P/'review.json').read_text())
c=json.loads((P/'preceding-capture-comparison.json').read_text())
assert v['passed'] and r['checks']==4235 and r['failures']==0 and r['capturePairs']==218
assert not v['realProfileChanges'] and not v['frozenInputChanges']
assert c['sameActorFields']==190 and c['sourcePixelsChanged']==16 and c['nativeCropsExact']==174
assert c['guardSourcePixelsExact']==c['guardNativeCropsExact']==28
assert (P/'capture-motion-browser.png').is_file()
review='Current four exit native/source chronological boards and preceding-native-comparison inspected. Revised squat and near-standing cloth darker; near-standing head closer to master. Normal walking endpoint unchanged. Remaining squat head, grade, segment/hardware, contact and moving joins provisional. Entry and guard visual evidence reused from prior inspection with exact current source/native crop parity; not newly inspected all entry/guard boards.'
r['visualReview']=review
(P/'review.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
m=json.loads((P/'capture-motion.json').read_text());m['visualReview']='Browser bare/exit/quarter replay controls exercised and screenshot saved. Chronological exit boards reviewed; screenshot is sampled playback, not full continuous temporal/contact acceptance.'
(P/'capture-motion.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
heading='Bill South revised rising sources refreshed native evidence — October 2, 2026'
body=f"""Fixture character/{P.name} stages unchanged South entryV2 and revised independent South exitV3, both gears. Current normal actor/player and fixture-only renderer/main; original geometry, oxygen and safety retained. No normal candidate selection.

Fresh native interval {v['seconds']} seconds: 4235 checks, zero failures; {v['frozenInputs']} frozen inputs unchanged; all {v['realProfileFileCount']} owner non-log files unchanged under scratch APPDATA. 218 source/native pairs (436 PNGs): 190 advancing 60Hz captures and 28 synthetic guard presentations. Exact captured source registrations and eight decoded finite normal/quarter motion replays.

Compared preceding South native fixture: all 190 named actor-field comparisons unchanged (foot, tick, clock, state, direction, water, medium, materialWeight). 174 advancing source/native fixed-root crops exact; 16 changed captures exclusively revised exit source indices5/6. All28 guard source/native crops exact. Saved compare_preceding.py reproduces both advancing and guard comparisons; diagnostic summary records are excluded from captured guard inventory. Whole-scene outside-crop equality is not established.

{review}

Browser bare/exit/quarter controls exercised with saved screenshot. Captured replay preserves simulation timing but does not establish full continuous live motion/contact acceptance. SourceV3 now has scoped fresh native evidence; nativeAcceptance and normalSelected remain false. No new checkpoint/TitleContinue interval in this milestone.

Lesson: source revisions need a refreshed frozen native interval. Reuse preceding visual evidence only for exactly matched source and native crops, and inspect the changed poses separately. Compare named motion fields independently of changed artwork; distinguish captured guard presentations from summary/event records. Passing mechanics do not certify master fidelity.

Next remaining South master/head/grade/segments/contact/moving joins, scratch checkpoint/TitleContinue, other-direction master audits, normal admission/cargo lifecycle and full-library consistency/polish. Full Bill objective remains active/incomplete.
"""
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
 with f.open('rb') as stream:stream.seek(max(0,f.stat().st_size-131072));tail=stream.read()
 if heading.encode() not in tail:
  with f.open('a',encoding='utf-8') as stream:stream.write('\n## '+heading+'\n\n'+body+'\n')
(P/'HANDOFF.md').write_text('# Project handoff\n\n## Objective\nFull Bill animation set matching masters, followed by full-library consistency/polish. Active/incomplete.\n\n## Accepted decisions\nPreserve original camera/source density, canonical equipment, normal actor/player, original collision/safety and isolated saves. SourceV3 remains a candidate.\n\n## Current state\n'+body+'\n## Changed files\ncompare_preceding.py, comparison report/board, record_milestone.py, review.json, capture-motion.json/browser screenshot, sourceV3 master-revision-review.json/HANDOFF.md and six guidance files. Existing fixture/captures provide refreshed evidence.\n\n## Verification\n4235/0 native, 2001 stable inputs, 2931 owner files unchanged;190 named-field comparisons,174 exact advancing source/native crops and28 exact guard pairs. Revised source indices5/6 only visual changes.\n\n## Next action\nFinish South master/contact/motion and scratch resume checks; normal admission and full cross-family polish remain.\n',encoding='utf-8')
s=R/'character/bill-water-exit-south-v3';q=json.loads((s/'master-revision-review.json').read_text())
q['nativeFixtureEvidence']=dict(fixture='character/'+P.name,checks=4235,failures=0,seconds=v['seconds'],sourceNativePairs=218,frozenInputs=v['frozenInputs'],ownerProfileFilesUnchanged=v['realProfileFileCount'],visualReview=review,scope='Scoped refreshed fixture evidence; full master/contact/motion and resume acceptance pending.')
q['nativeAcceptance']=False;q['normalSelected']=False
(s/'master-revision-review.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
h=s/'HANDOFF.md';t=h.read_text(encoding='utf-8');mark='## Refreshed native fixture evidence — October 2, 2026'
if mark not in t:h.write_text(t+'\n'+mark+'\n\n'+body,encoding='utf-8')
print(json.dumps(dict(checks=r['checks'],pairs=r['capturePairs'],guidanceFiles=len(paths),goal='active/incomplete')))
