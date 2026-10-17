from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];W=R/'character/bill-walk-north-master-head-v1';assert not (P/'runtime-evidence-crown-v2.json').exists()
families=[];files=[P/'build.py',P/'verify.py',P/'head-registration.json',P/'crown-audit.json',W/'build.py',W/'verify.py',W/'head-registration.json']
for folder,output,checks,package in [(P,'bill-run-head-locked-selected-native-v1',289,141),(W,'bill-walk-north-master-head-selected-native-v1',280,125)]:
 o=R/'output'/output;n=json.loads((o/'validation.json').read_text());v=json.loads((folder/'verification.json').read_text());log=(o/'native.log').read_text();assert n['artPassed'] and n['returnCode']==0 and f'{checks} checks,0 failures' in log and v['checks']==package
 families.append({'family':folder.relative_to(R).as_posix(),'nativeChecks':checks,'packageChecks':package,'native':n});files.extend([folder/'verification.json',o/'native.log',o/'validation.json'])
 files.extend(o.glob('*.png'))
audit=json.loads((P/'crown-audit.json').read_text());assert all(d['missingCrownPixels']==0 for d in audit['directions'])
evidence={'revision':'complete-crown-v2','families':families,'packageChecks':266,'nativeChecks':569,'scope':'Complete14-row native master crown and soft edges, protected bodies and unchanged original gait/equipment references. Selected normal-loader checks and reviewed native captures, not full face/collar/motion/route or owner acceptance','sha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'fullGoalComplete':False}
(P/'runtime-evidence-crown-v2.json').write_text(json.dumps(evidence,indent=2)+'\n')
note='''

### Bill run/north-walk complete crown revision — October 1, 2026
Independent crown audit contradicted the earlier component completeness assumption: west run component omitted141 master crown pixels,88 opaque, with four visible top rows missing; east14/south16/north16 soft edge pixels omitted. Warm-silhouette extraction can lose gray hair, while exact retained-pixel equality and connected alpha still pass. Current bill-run-head-locked-v1 builder now unions the complete master crown/soft edges with the bounded face mask at native scale1. All four missing-pixel counts now0; rebuilds also restore the shared north-walk component.24 run+30 north-walk bare exports revised, original authored bodies/clocks/stride protected and equipment references untouched. Earlier package/native evidence and exports retained under review-before-crown-v2; new evidence is runtime-evidence-crown-v2.json, not an overwrite of historical acceptance.
141 run+125 north-walk package checks pass; independent full crown coverage checks now supplement exact component/body/source/clock proofs. Native289 run+280 north-walk checks pass, engine0 at11.75/11.94s, four148/82 run captures plus all-pose north-walk native capture reviewed. Both strict2931-file non-log guards false,last_session.json only; attribution unproven, no owner restore or guard-clean retry. Literal selection paths unchanged, inventory locomotion-v6 remains authoritative for load order; sampled/all-frame/moving reviews rebuilt with current source hashes. Full14-row crown proof is not full face/neck/shoulder/whole-motion acceptance. Continue remaining full-frame cardinal/material/moving joins, then full selected family master anatomy/perspective/motion and prior physical/service/checkpoint contexts. Full goal active.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Brine Space · Bill complete native crown revision v2

## Objective and acceptance
Continue full Bill master-consistent set and cross-family polish. Previous turn was progress:96 west walk frames selected,978 scoped checks. This revision restores omitted gray crown/soft edges in54 selected bare run/north-walk exports. Full goal and owner acceptance remain open.

## Accepted decisions and constraints
Native accepted master pixels, no resampling; original authored gait/body and paired helmet sources preserved. Check completeness separately from subset equality. Crown coverage is scoped to14 rows and does not certify full face/neck/shoulder motion. No NPC heading/run behavior, owner-save restore, export/commit/push.

## Current state
Run build.py/verify.py and native components/24 frames updated; audit_crown.py/crown-audit.json provide independent full coverage evidence. Shared north-walk builder regenerated component/30 poses; verify.py now checks complete crown. Prior exports/recipes/reports copied into review-before-crown-v2 in both folders. Selection manifests/loader paths unchanged. Current locomotion source comparisons rebuilt against unchanged locomotion-v6 load-order inventory.

## Verification
266 package and569 normal-loader native checks pass, engine0. Missing crown pixels east/west/south/north now0 versus14/141/16/16. Native run11.75s and north-walk11.94s; all fresh captures reviewed. Both strict all2931 non-log owner-profile guards false,last_session.json only; attribution unproven, no restore or clean retry. New source/native hashes in runtime-evidence-crown-v2.json; original runtime-evidence remains historical. No live run route/Continue/full-set acceptance claim.

## Next action
Review remaining all-frame cardinal walking boards/materials and moving joins, then full family head/neck/shoulder/anatomy/perspective/material consistency. Address actual service/physical/checkpoint contexts left unproven in prior handoffs. Current source212bare/194helmet counts do not establish completion.
'''
(P/'HANDOFF_CROWN_v2.md').write_text(handoff);(W/'CROWN_v2.md').write_text('Current native head includes complete master crown and soft edges. See ../bill-run-head-locked-v1/HANDOFF_CROWN_v2.md and runtime-evidence-crown-v2.json. Earlier exports/evidence are frozen under review-before-crown-v2.\n')
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/name).open('ab') as f:f.write(note.encode())
shutil.copy2(R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md'))
status=R/'docs/CURRENT_STATUS.md';prefix='''## Bill run/north-walk complete crown revision — October 1, 2026

Independent master crown audit found west141 missing pixels/88 opaque/four visible rows; east14/south16/north16 soft edges missing. Repaired run components at native scale1 and rebuilt24 run+30 shared north-walk bare poses. Complete audited crown counts now0 in all directions; bodies/gait/gear references preserved.266 package+569 normal-loader native checks pass, fresh run/north-walk captures reviewed. Both strict2931-file non-log guards false,last_session.json only, attribution unproven. Earlier evidence frozen under review-before-crown-v2; new runtime-evidence-crown-v2.json/HANDOFF_CROWN_v2.md. Current load-order inventory locomotion-v6 unchanged; visual reviews rebuilt. Complete crown proof is scoped, not full-face/anatomy/whole-motion/route/Continue acceptance. Full goal remains active; next remaining cardinal/material/moving joins and broader family/physical/service/checkpoint polish.

''';status.write_bytes(prefix.encode()+status.read_bytes());print('Recorded54 revised bare poses,835 scoped checks and complete-crown lesson')
