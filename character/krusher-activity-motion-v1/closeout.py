from pathlib import Path
import json,shutil,hashlib
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;P=R/'character/krusher-animation-package-v11'
reports={};checks=0;captures=0
for lane in ['review-v2','turns-v2','repair-v3','construction-v4']:
 d=H/lane;q=json.loads((d/'report.json').read_text());r=json.loads((d/'run-verification.json').read_text())
 assert not q['failures'] and r['engineExit']==0 and not r['ownerFilesChanged'],lane
 log=(d/'engine.log').read_text(errors='replace');assert not any(w in log for w in ['ERROR:','WARNING:','leaked']),lane
 checks+=q['checks'];captures+=len(q['records']);reports[lane]={'checks':q['checks'],'captures':len(q['records']),'cases':len(q.get('episodes',q.get('cases',[]))),'ownerFilesFingerprinted':r['ownerFilesFingerprinted'],'ownerFilesChanged':r['ownerFilesChanged'],'scope':q['scope']}
 dst=P/'verification/activity-motion'/lane;dst.mkdir(parents=True,exist_ok=True)
 for f in ['report.json','run-verification.json','engine.log']:shutil.copy2(d/f,dst/f)
baseline=json.loads((R/'character/krusher-station-motion-v1/candidate-contract.json').read_text())
assert all(hashlib.sha256((P/k).read_bytes()).hexdigest()==v for k,v in baseline.items())
(H/'candidate-contract.json').write_text(json.dumps(baseline,indent=2))
turns=json.loads((H/'turns-v2/report.json').read_text());assert len(turns['episodes'])==72 and all(not x['missingTurnSlots'] for x in turns['episodes'])
summary={'candidate':'krusher-animation-package-v11','artChanged':False,'checks':checks,'failures':0,'nativeCaptures':captures,'activityEpisodes':24,'turnTrials':72,'authoredTurnHoldsReached':sum(len(x['turnSlots']) for x in turns['episodes']),'maintenanceCases':8,'paidBuildCases':2,'reports':reports,'visualMethod':'Agent inspected 368 sampled native sitting/reading/workshop poses (19 sheets), all552 native turn-slot head/collar details (12 sheets), source/room context and sampled maintenance/construction witnesses. Capture counts do not imply uninterrupted human viewing.','result':'No additional head/neck defect found; current V11 source/manifests retained.','limits':'Room activity contacts and locomotion legs are staged; production arrive/update/move/player/render and actual clearance are exercised. Lounge resolves north and observation reading south across room rotations. Normal roster integration, autonomous dispatch and fresh Continue remain separate. Native replays align crops at the foot and reconstruct simulation cadence.'}
summary['fixtureHashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in H.glob('*.gd')}
summary['workingWitnesses']={'maintenanceSamples':176,'constructionSamples':78,'constructionInterruptionInteriorChangesIncluded':True}
(H/'summary.json').write_text(json.dumps(summary,indent=2));shutil.copy2(H/'summary.json',P/'verification/activity-motion/summary.json')
for name in ['candidate-contract.json','media-validation.json','media-index.json']:
 if (H/name).exists():shutil.copy2(H/name,P/'verification/activity-motion'/name)
(H/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 15, 2026 · Project: Brine Space · Task: Krusher Dom sitting, working, carrying and swimming review

## Objective and acceptance
Continue the requested in-game animation pass, especially sitting, work, cargo and water transitions; repair visible head/collar defects while preserving accepted body art and source timing.

## Accepted decisions and constraints
V11 remains the current 586-state / 8,058-hold animation candidate. No additional art defect was found in this pass; no repaint, palette change, rescale, normal roster admission or Site redeployment. Prior private gallery remains current. Owner visual acceptance remains separate.

## Current state
New fixtures, source/position-change native captures, reports and foot-aligned replays are in character/krusher-activity-motion-v1. index.html and media/ contain the replay review. prepare.py builds the actual activity matrix; prepare_turns.py builds moving carrying/swimming trials; prepare_work.py adapts the existing maintenance and ordinary paid-construction fixtures to current V11. Rebuilds use local files only.

## Verification
24 actual arrive/update activity sequences: crew lounge, observation reading and salvage workshop, both gears / four room rotations. All complete. Lounge faces north and reading south across rotations; workshop reaches all four work facings plus real pickup/carry turns/unload/idle. Do not equate room rotation with cardinal actor coverage.

72 ordinary carry/swim/swim-carry turn trials use production move/player/render and real furnished-room transition clearance. All 552 authored turn holds reached. Native swimming trials include stop/return to tread. Eight real equipment-contact maintenance cases complete kneel/repair/stand; two ordinary paid construction cases exercise draw/weld/stow plus power-loss stow/hold/resume and pause.

Final combined checks: {checks:,}, zero failures/errors/warnings/leaks; {captures:,} native captures. All four isolated runners preserve all 2,947 fingerprinted owner non-log files. V11 package/ordered manifests match the prior station-motion contract exactly. All fixture GDScript UID pairs retained.

Visual evidence: 368 chronological sampled native activity poses on19 sheets, all552 turn-slot head/collar details on12 sheets, full-room contexts and sampled working witnesses. Agent review found no new detached collar, visor overlap or head/body density mismatch. Full 1,716 activity pose and 698 turn/gait pose witness sets are retained, but were not all manually inspected. Dark submerged output is retained; water-detail-diagnostic.png is a review-only exposure lift, not revised art. Native crop replays reconstruct source/position-change simulation timing and align the declared foot; they are not full-room real-time videos.

Initial activity startup was stopped before capture while tracing setup. Initial turn trials exposed fixture camera clipping and correctly blocked loaded-water turns in an aisle: rejected turns/ evidence is retained. Final turns-v2 selects actual cargo-turn clearance at both ends and follows the actor; no collision guard was bypassed. Maintenance's full-viewport capture hit its360s limit; final repair-v3 uses actor crops plus first-action room contexts and one-frame/post-draw synchronization, completing in70.35s with the same controller guards. Fixture indentation and metadata identifier errors were corrected before final evidence. Construction-v3 established the paid-job behavior; final construction-v4 additionally captures every changed interruption/return source. Reviewed176 maintenance samples and78 construction samples, including all captured interruption interiors. All7 exported replays decode with exact recorded durations. Earlier rejected/partial evidence is retained and is not counted in the final50,998checks.

## Next action
Review the native replays alongside the unchanged private animation gallery. No known head/neck issue remains in the reviewed cases. Normal roster integration, autonomous dispatch, additional furniture contacts and fresh Continue are not established by this pass.
''',encoding='utf-8')
status=R/'docs/CURRENT_STATUS.md';old=status.read_text(encoding='utf-8-sig');entry=f'''## Krusher Dom in-game activity/turn pass — October 15, 2026

V11 art retained after24 actual sitting/reading/workshop lifecycles,72 carrying/
swimming turn trials (all552 authored turn holds),8 equipment-contact maintenance
cases and2 ordinary paid-build cases. Both equipment variants; workshop/repair
use all four work facings, lounge resolves north and observation reading south.
{checks:,} checks / zero failures; {captures:,} native captures, sampled chronological
visual review and every turn-slot head/collar detail inspected. No new head/neck
defect found. All2,947 fingerprinted owner files unchanged in each final runner.
[Native replay review](../character/krusher-activity-motion-v1/index.html) and
[handoff](../character/krusher-activity-motion-v1/HANDOFF.md). Normal roster
integration and owner visual acceptance remain separate.

'''
if not old.startswith('## Krusher Dom in-game activity/turn pass'):status.write_text(entry+old,encoding='utf-8')
print({'checks':checks,'captures':captures,'failures':0,'artChanged':False})
