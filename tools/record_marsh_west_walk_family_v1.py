"""Record West whole-family source, staged world and sampled browser evidence."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'character/marsh-west-walk-family-detail-v1'
OUT=ROOT/'character/marsh-west-walk-family-contact-v1'
RUN=ROOT/'output/marsh-animation-audit/west-walk-world-v1-2026-10-03'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=json.loads((SOURCE/'review.json').read_text())
for r in review['records']:
    assert sha(ROOT/r['rawPath'])==r['rawSha256'] and sha(ROOT/r['framePath'])==r['frameSha256']
    assert r['soleDisplacement']==0
    receipt=json.loads((SOURCE/f"phase-{r['slot']:03}.result.json").read_text())
    assert receipt['rawSha256'].lower()==r['rawSha256']
frozen=json.loads((RUN/'inputs-after.json').read_text())
changes=[p for p,h in frozen.items() if sha(ROOT/p)!=h]
assert changes==['tools/prepare_marsh_west_walk_world_v1.py'],changes
vpath=OUT/'world-review/verification.json';v=json.loads(vpath.read_text())
assert (v['checks'],v['failures'],v['pairedCaptures'],v['samples'],v['actorRestores'],v['inputsStable'],v['ownerNonLogStable'])==(1561,0,36,260,3,5509,2931)
for b in v['boards']:
    assert sha(ROOT/b['path'])==b['sha256'];b['reviewed']=True
v['visualReview']='First full1600x900native and all six complete928wide same-root source/native boards inspected. Figure/material/collar/face clearer at station scale; all staged soles retain original depth. No continuous watched cadence or full-set acceptance.'
v['postNativeHelperChanges']=changes;v['otherExistingTestedInputsStillExact']=len(frozen)-len(changes)
v['currentPreparerSha256']=sha(ROOT/changes[0]);vpath.write_text(json.dumps(v,indent=2)+'\n')
crowns=[r['opaqueBounds'][1] for r in review['records']];oldcrowns=[r['originalOpaqueBounds'][1] for r in review['records']]
maximum=lambda xs:max(abs(xs[(i+1)%6]-xs[i]) for i in range(6))
receipt={'normalAdmission':False,'fullGoalComplete':False,'decision':'Complete six-pose material/definition improvement retained provisionally. Normal selection unchanged. Closing/opening and half-cycle bob still needs assessment before admission.','sourceReviewSha256':sha(SOURCE/'review.json'),'nativeVerificationSha256':sha(vpath),'allSixRawFiguresReviewed':True,'sourceBoards':[{'path':(SOURCE/n).relative_to(ROOT).as_posix(),'sha256':sha(SOURCE/n),'reviewed':True} for n in ['family-joins-native.png','heads-2x.png']],'crownSequence':crowns,'originalCrownSequence':oldcrowns,'maxAdjacentCrownChange':maximum(crowns),'originalMaxAdjacentCrownChange':maximum(oldcrowns),'residual':'Max3nativepixel crown jump versus original2; one additional pixel=.441081world units at65.28/148. Do not infer anatomical bob solely from hair bounds; inspect actual joins.','browser':{'pageSha256':sha(OUT/'motion-review/motion-review.html'),'screenshotSha256':sha(OUT/'motion-review/browser-quarter.png'),'observations':['normal phase0clock83draw6','quarter phase1clock7481draw457','screenshot quarter phase4clock9633draw973','quarter phase2clock12097draw1564','paused phase4clock14191draw2076'],'scope':'Sampled advancement and controls, not continuously watched complete loop.'},'next':'Check closing/opening and half-cycle bob at station density; normal catalogue/player admission when supported, then remaining movement and other family joins.'}
(OUT/'acceptance-review.json').write_text(json.dumps(receipt,indent=2)+'\n')
note='''

## Marsh West full walking family detail/contact study — October 3, 2026

Six built-in whole-pose edits from exact current walk-west, whole184square to
1024nearest guides, shared ownidle identity/grade and unpainted original-master
collar/suit crop[340,400,670,900]. Exact request/ref/raw/result provenance in
character/marsh-west-walk-family-detail-v1. Six originals copied immediately;
all six complete raw figures, native family/master/idle/start/stop/run/selected
East comparison and2xheads inspected. Collar/harness/seams/glove/boot definition
clearer, muted ivory and face shade coherent. Original West master visibly has
natural near ear/temple; do not import hardware from another directional master.

One whole-canvas184/1254resample per raw, raw alpha retained. No anatomy splice,
recolour, pose fit or per-frame size normalization. Opaque heights99.315..100.685%
of old, crowns within1px, all soles exact;IoU.93731..97404. Contact bank
character/marsh-west-walk-family-contact-v1 comprises six exact byte copies,
no registration necessary. All original timing/pivot/height/stride metadata
retained. Original master display uses fixed147/1201ruler and source foreground
bounds[373,179,639,1380]; this display reference does not fit candidate anatomy.
APNG6x150ms generated, not claimed continuously watched.

Actual normal actor/main/grid/player with staged instance override:1561checks0
failures,260movement samples,36source/native pairs,3moving actor restores; all
six walking and4start/4stop holds observed on96/112unit West dry routes.5509inputs/
2931owner non-log files unchanged in scratch APPDATA,engine0/no errors/warnings,
session82263terminal. All72submitted sources exact expected RGBA; first full
1600x900native and all6complete928wide boards inspected. Default cold_store, same
root source sole depth strict/equal, pause stable, actual approximate arrival.
Publisher inherited East's1653/43count assumptions; corrected to actual1561/36
without rerunning successful native. Preparer changed after interval for
reproducible publisher;5508other existing tested input hashes still exact, actual
tested fixture/fingerprinter reproduced unchanged. No gameplay/runtime edits.

Crowns27,24,25,25,24,24 vs original26,24,25,26,24,25; maximum adjacent/closing
crown change3vs2. Extra1pixel=.441081world units; inspect actual head/half-cycle
joins rather than assume hair bounds prove anatomical bob. Whole family remains
PROVISIONAL/UNSELECTED. Browser sampled normal/quarter advancement and pause,
saved screenshotphase4clock9633draw973; not continuous cadence acceptance.
Normal228states/1190slots/90body manifests unchanged; latest post-East inventory.

Lesson: a complete family shared grade/material reference can improve definition
while preserving source sole depth without registration. Still measure crown/
closing joins; source height success is not temporal consistency. Derive expected
coverage from actual direction/state timing and observed holds, not another
direction's capture count. Separate display ruler, raw packing and world proofs.
Next closing/opening bob/half-cycle review, then normal catalogue/player admission
and other movement families. No full2Dplanted foot, autonomous jobs, paid building,
all rooms/rotations, disk fullSave/TitleContinue or full-library acceptance inferred.
Handoff:docs/MARSH_WEST_WALK_FAMILY_HANDOFF_2026-10-03.md. Full goal active.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('Six provisional West poses/source/native/browser reviews recorded;1561checks/36pairs;5508other tested hashes exact; four notes/skill mirror updated.')
