"""Record selected family with explicit source/native limits and fixture history."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-v2/supplemental/east-walk-polish-v1'
RUN=ROOT/'output/marsh-animation-audit/east-walk-selected-world-v3-2026-10-03'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
vpath=OUT/'world-review/verification.json';v=json.loads(vpath.read_text())
assert (v['checks'],v['failures'],v['inputsStable'],v['ownerNonLogStable'])==(1671,0,5456,2931)
for b in v['boards']:
    assert sha(ROOT/b['path'])==b['sha256'];b['reviewed']=True
v['visualReview']='All eight complete native/source comparison boards and first full1600x900native inspected. Source full-figure/family/head/master/idle/start/stop/run review complete for changed poses; selected East walking improvement accepted within recorded scope.'
vpath.write_text(json.dumps(v,indent=2)+'\n')
frozen=json.loads((RUN/'inputs-after.json').read_text());assert all(sha(ROOT/p)==h for p,h in frozen.items())
inventory=ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-east-walk/inventory.json'
browser=inventory.parent
receipt={'normalAdmission':True,'fullGoalComplete':False,'nativeVerificationSha256':sha(vpath),'normalInventorySha256':sha(inventory),'testedHashesStillExact':len(frozen),'reviewed':True,'sourceReviewSha256':sha(ROOT/'character/marsh-east-walk-halfcycle-polish-v1/review.json'),'browserPageSha256':sha(browser/'motion-review.html'),'browserScreenshotSha256':sha(browser/'browser-quarter.png'),'browserObservations':['normal phase0clock83draw6','quarter phase5clock7197draw440','screenshot quarter phase4clock8736draw809','quarter phase1clock10125draw1142','paused phase4clock12331draw1681'],'limits':'Sampled browser advancement, not continuous watched cadence. Actual normal catalogue body/player/actor/main/grid source/depth and prescribed routes proven; not complete2Dplanted foot, autonomous jobs, all rooms/rotations, paid building or disk fullRunSave/TitleContinue/full-library acceptance.','fixtureHistory':['V1relative counterfactual path failed image load and nulltexture; zero captures, stopped own verified engine64996,exit-1;5456inputs/2931owner stable.','V2full paths passed1659checks/43pairs with six resource-image warnings;5456inputs/2931owner stable.','V3PNG-byte buffer decoder added12checks;1671checks0failures/43pairs/no warnings,5456inputs/2931owner stable. Earlier sources/logs retained.']}
(OUT/'acceptance-review.json').write_text(json.dumps(receipt,indent=2)+'\n')
note='''

## Marsh East six-phase normal walking polish selected — October 3, 2026

The detailed family, bob repair1/2/5 and final whole-pose phase4 face-grade edit
are selected in character/marsh-v2/supplemental/east-walk-polish-v1. Phase4raw
exec-5b0f6037-2f81-4bf0-baaf-26bc81edfb21 and exact request/ref/output receipts
retained in character/marsh-east-walk-halfcycle-polish-v1. Whole raw1254square
to184resampling with raw alpha; five exact neighbor copies. New raw figure,
complete family/master/idle/start/stop/run board and2xheads inspected. Detail and
face grade more coherent; camera, proportions, pose silhouette and sole preserved.
Requested phase4crown23was not achieved: remains22. Crowns24,23,22,24,22,22;
original23,22,21,23,22,21. Both have maximum adjacent crown change2pixels,
including closing/opening join. Half-cycle residual1nativepixel=.441081world
units at65.28/148; retained explicitly, no anatomical fit or contact relaxation.

Normal catalogue changes only walk-east six drawings;227effective states exact
by metadata/source hashes, all original state timing/pivot/height/stride flags
preserved. Current normal228states/1190slots/90body manifests; authoritative
inventory character/marsh-selected-normal-audit-2026-10-03-post-east-walk/inventory.json.
Earlier post-South inventory is historical evidence, not current selection.

NativeV3normal catalogue (no candidate override), actual actor/main/grid/player,
explicit original source counterfactual:1671checks0failures,270movement samples,
43paired source/native captures,3moving actor restores;5456inputs/2931owner
non-log files unchanged under scratch APPDATA,engine0/no errors/warnings.
All8complete928wide boards plus first full1600x900native inspected. Strict same
root source sole depth remains exact. FixtureV1relative comparison paths failed
before capture, own verified engine stopped;V2full paths passed1659checks with
six image-loading warnings. Both5456/2931stable,failed sources/logs retained;
V3uses FileAccess PNG bytes and explicit decoder results. Native/source browser
sampled normal/quarter advancement and pause, screenshot saved; not continuous
watched cadence. Selected improvement accepted; full animation goal incomplete.

Lesson: subpixel source differences need actual display-scale and cyclic motion
context. Preserve the measured residual rather than force anatomical fitting or
repeatedly chase a one-pixel prompt. This does not weaken physical sole checks.
Resolve relative manifest paths before comparison; decode PNG bytes with the
runtime method to avoid imported-resource warnings in source-only fixtures.
Next other movement families (West walking), cross-family master/idle/action
grade and broader natural/water/equipment/furniture/fullSave/Continue checks.
No complete2Dplanted-foot, autonomous-goal or whole-library acceptance inferred.
Handoff:docs/MARSH_EAST_WALK_SELECTED_HANDOFF_2026-10-03.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('Normal selected East walk acceptance recorded;5456tested hashes exact; four notes/skill mirror updated; full goal remains active.')
