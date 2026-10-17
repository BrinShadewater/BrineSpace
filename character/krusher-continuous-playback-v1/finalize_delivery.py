from pathlib import Path
import json, shutil

R=Path(__file__).resolve().parents[2];H=R/'character/krusher-continuous-playback-v1';P=R/'character/krusher-animation-package-v11'
V=P/'verification';V.mkdir(exist_ok=True)
for name in ['continuous-coverage','repair-validation','registered-alias-audit','gallery-validation','changed-scope','preview-export','remote-preview']:
    p=H/(name+'.json')
    if p.exists():shutil.copy2(p,V/p.name)
for name in ['native','bunk','water']:
    dst=V/name;dst.mkdir(exist_ok=True)
    for fn in ['report.json','run-verification.json','engine.log']:shutil.copy2(H/'review'/name/fn,dst/fn)
    q=json.loads((dst/'report.json').read_text());r=json.loads((dst/'run-verification.json').read_text())
    assert not q.get('errors',[]) and not q.get('failures',0) and r['engineExit']==0 and not r['ownerFilesChanged']
q=json.loads((P/'package.json').read_text());q['status']='V11 complete animation asset review candidate; continuous playback pass verified; owner visual acceptance pending';q['verification']='res://character/krusher-animation-package-v11/verification/summary.json'
(P/'package.json').write_text(json.dumps(q,indent=2))
summary={'states':586,'frameHolds':8058,'indexedPngFiles':3486,'correctedDrawings':21,'changedStates':19,'changedHolds':91,'nativeChecks':63664,'nativeFailures':0,'ownerFilesChanged':0,'packageChecks':16790,'registeredPoseConflicts':0,'continuousCoverage':'All current source holds observed; 101 recordings, 198 contextual plans including 72 turn chains.','visualMethod':'Chronological decoded motion witnesses for every state plus selected live playback; not uninterrupted human viewing of all recordings.','integration':'Portable candidate only; normal roster integration and owner acceptance remain separate.'}
(V/'summary.json').write_text(json.dumps(summary,indent=2))
refs=P/'references';refs.mkdir(exist_ok=True)
for fn in ['motion-comparison.png','final-bunk-motion.png']:shutil.copy2(H/fn,refs/fn)
(P/'README.md').write_text('''# Krusher Dom V11 animation candidate

586 states (338 bare, 248 helmet), 8,058 authored frame holds and 3,486 indexed PNGs. Load the ordered whole-path manifests in package.json; retain their timings, pivots, canvases and 148-pixel standing ruler.

This pass changes 21 drawings across 19 states / 91 holds: five rigid helmet/collar registrations through bunk entry, recline and return, and sixteen swimming-turn visor interiors. Reverse turns and other shared-pose aliases receive identical repairs. Existing portrait pixels retain their density; body pixels outside declared local masks are exact. Bare art is unchanged from V10.

All states ran and were recorded continuously at original timing, with two loop cycles and contextual entry/action/destination sequences. Current-source coverage accounts for every hold, including a bounded retry of one 20ms hold. Visual review used chronological decoded motion witnesses for every state, selected live playback, all turn families and close-ups of the revised collars. See verification/summary.json and the detailed reports. Component contact alone did not establish collar quality; the final close-up and bunk replay closed the remaining horizontal slit.

The private animation gallery offers Previous/Revised comparisons and smooth gait/turn/return cycles. Lossless WebP exports pass 3,486 decoded RGBA comparisons. Native fixtures pass 63,664 checks with the owner's profile unchanged. This is a complete animation asset candidate; normal game roster integration and owner visual acceptance remain separate. Retained unindexed frame hashes support earlier recorded review contracts.
''')
handoff='''# Project handoff

Updated: October 14, 2026 (published October 15 UTC) · Project: Brine Space · Task: Krusher Dom continuous animation review

## Objective and acceptance
Run every animation continuously, inspect head/body fit especially through turns and transitions, repair remaining issues and update the private review gallery. Final art remains subject to owner visual acceptance.

## Accepted decisions and constraints
Retain existing likeness, pixel density, source timings, original full-body poses and per-pack geometry. Repair existing authored pixels locally. No normal roster integration, gameplay change, game-repository commit or export. Private Site audience preserved.

## Current state
Delivery: character/krusher-animation-package-v11. Repair scripts, masks, recordings, observed contracts and visual witnesses: character/krusher-continuous-playback-v1. Five bunk helmet/collar translations and sixteen observed visor-aperture composites change 21 drawings across 19 states / 91 holds. Shared source poses remain consistent. Final collar evidence: final-bunk-motion.png; turn comparisons: visor-pilot-00.png and 01.

The gallery supports Previous/Revised, native/2x/3x nearest display and smooth gait/turn/destination/return playback for all 72 turns. Production details are in remote-preview.json. Original reference homepage retained.

## Verification
586 states / 8,058 holds ran continuously. Final-source coverage: 101 recordings, zero missing holds; 198 contextual plans including 72 turns. One 20ms hold needed a bounded original-timing retry. Every state was visually inspected through decoded chronological motion witnesses, with selected live playback; this was not uninterrupted human viewing of every recording. Final sealed bunk replay covers all 15 holds.

16,790 portable-package checks; 8,058 slots / 3,464 registered pose groups with zero conflicts; 21 local mask checks; 3,486 lossless decoded WebP comparisons; 802 gallery geometry checks. Native full-bank 57,025 + bunk 240 + water 6,399 = 63,664 checks, zero failures/errors/warnings/leaks. All 2,947 fingerprinted owner non-log files unchanged. Native .uid pairs preserved. Body pixels outside the declared repair masks are exact; visor alpha is exact.

Lesson: opaque component contact alone missed a horizontal collar slit. Require a full collar close-up and continuous recline/return replay. Automatic warm-pixel hulls selected equipment and were rejected; repair_visors_observed.py and its manually observed polygons are authoritative. repair_visors.py is exploratory/rejected.

## Next action
Owner can review the private gallery. No known remaining head/neck issue found in this pass. Keep V10 as the comparison baseline and V11 as the current candidate. Integration remains a separate owner decision.
'''
(H/'HANDOFF.md').write_text(handoff)
status=R/'docs/CURRENT_STATUS.md'
entry='''## Krusher Dom continuous animation pass — October 14, 2026

V11 repairs 21 drawings across 19 states / 91 holds: bunk collar gaps and
helmet visor overlap through swimming turns. Existing density, timings and
pack geometry retained. All 586 states / 8,058 holds ran in continuous recorded
playback; final-source coverage has zero missing holds, including 72 turn chains
and 126 other transition contexts. Visual review used chronological motion
witnesses for every state plus selected live playback. Native 63,664 checks pass;
all 2,947 fingerprinted owner files unchanged. Private gallery updated with
Previous/Revised and smooth turn cycles. Complete asset candidate; owner visual
acceptance and normal roster integration remain separate.
[Handoff](../character/krusher-continuous-playback-v1/HANDOFF.md) and
[package](../character/krusher-animation-package-v11/README.md).

'''
old=status.read_text(encoding='utf-8-sig')
if not old.startswith('## Krusher Dom continuous animation pass'):status.write_text(entry+old,encoding='utf-8')
print(summary)
