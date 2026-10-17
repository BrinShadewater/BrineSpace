"""Record normal-loader evidence only after terminal success and visual review."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-north-chair-falls-selected-native-v1'
n=json.loads((O/'validation.json').read_text())
records=json.loads((O/'records.json').read_text())
visual=json.loads((P/'visual-review.json').read_text())
review=json.loads((P/'review-evidence.json').read_text())
metadata=json.loads((P/'post-run-metadata.json').read_text())
assert n['passed'] and len(records)==28 and visual['reviewedBoards']==review['boards']
assert metadata['passed'] and metadata['sourcePNGsUnchanged'] and metadata['otherRegistrySelectionsPreserved']
packages=[json.loads((R/'character'/folder/'package-checks.json').read_text()) for folder in ['veld-lounge-fall-north-v1','veld-lounge-partial-fall-north-v1','veld-lounge-late-fall-north-v1','veld-lounge-early-fall-north-v1']]
assert all(x['failures']==0 and x['normalSelection'] for x in packages)
package_count=sum(x['checks'] for x in packages)
count=int(re.search(r'VELD NORTH CHAIR FALLS SELECTED: (\d+) checks,0 failures;28 fresh disk restores',(O/'native.log').read_text())[1])
assert all(len(x['reference'])==len(x['resumed'])==150 for x in records)
heading='## Veld North chair falls normally selected - October 2, 2026'
note=f'''
Normal grid_canvas loader now admits bare/helmet North full-seated, partial,
late3/late4 and early0/early1 fall families through eight whole manifest paths.
All six selected lowering/rising entrances and two distinct held-breathing sources
exercise actual mortality with no fixture animation-manifest injection.
No new raster art, ruler, palette, furniture geometry or death-controller change.

Native {count} checks, 0 failures / {n['seconds']}s, engine0/clean log:
28 actual RoomFlooding.kill cases, 28 ordinary eligible RunSave disk saves/reads
and fresh main-scene restores. 150 reference + 150 resumed 20ms actor steps per
case = 8400 future actor updates. Exact source/root/depth/physical foot/gear/needs/
timer/corpse equivalence and finite terminal clock oracle; 224 malformed saved
bindings rejected, unmarked sources rejected, wrong marked entry rejected for
partial poses. Sixteen existing/boundary selector guards and distinct held
breathing entrance checks for both gears. Root fade remains pose-specific:
early zero340ms, partial zero520ms, late/full zero720ms.

All six compact paired source/native/master boards reviewed, covering all28cases
and 196 paired future source/native captures plus actual entrance/chair crops.
{visual['finding']}
The interactive replay uses exact captured source/root traces, not a continuous
native world movie. Review: character/veld-north-chair-falls-selected-v1/
resume-review.html; visual findings and input bindings retained alongside it.

All {n['targetedInputCount']} targeted inputs unchanged during the native run;
broader scene/library dependencies not frozen. Scratch APPDATA preserved all
{n['realProfileFileCount']} owner non-log files. Scope default lounge rotation0,
prescribed death API/stage/timer and actor-only future while main paused;
not natural chooser/hazard cadence, all layouts/rotations or title/new-process
Continue. Existing paid Bill ward wake supplies ordinary survivor/save eligibility;
its repair route is not certified by this fixture. Post-run manifest status
labels are separately checked as metadata-only changes.
Post-admission {package_count} package/source/alpha checks pass across four families.

Lesson: previously staged fall families need a combined normal-loader matrix,
including held breathing and reverse source clocks. Candidate-only tests cannot
prove production admission or precedence. Freeze the loader with the source
bindings, then compare saved future motion and actual room contact against the
same master ruler. Keep motion evidence and natural-world coverage distinct.

Next paired bunk normal admission/remaining real furniture contexts, broader
natural task/hazard checks and full-library master/material/perspective/size/
proportion/motion polish. Full Veld goal active/incomplete; no final owner
acceptance, commit or export claim.
'''
handoff=f'''# Project handoff

Updated:2026-10-02 · Project:BrineSpace · Task:Normally selected North chair falls

## Objective and acceptance
Full master-matching Veld animation set and cross-family polish remain active.
North chair falls now select normally; final owner/world motion acceptance open.

## Accepted decisions and constraints
Keep exact selected entrance pixels and registered chair-to-floor root/depth.
Reuse existing body/material/native helmets; preserve furniture/owner geometry,
physical foot, ordinary mortality/save eligibility and isolated owner profile.

## Current state
scripts/grid_canvas.gd admits eight North fall manifests (both gear versions),
also recorded in character/ACTIVE_ASSETS.json with other selections preserved.
New test/UID, scratch runner, six paired master/native/source boards and exact
future replay in character/veld-north-chair-falls-selected-v1. Manifest/build
status labels reflect normal local admission; no raster/controller changes.
Pipeline, bible and both crew-life skill copies updated with combined proof.

## Verification
{count} native checks / 28 normal-loader mortality/disk/fresh-scene cases,
8400 future actor steps, 224 malformed guards, 16 selector guards and distinct
held breathing per gear; 0failures, engine0/{n['seconds']}s. All six boards reviewed.
{n['targetedInputCount']} frozen inputs and {n['realProfileFileCount']} real owner files unchanged during run.
Post-run status changes metadata-only. Rotation0 prescribed API/stage/timer,
paused-main actor future; natural cadence/all layouts/new-process Continue open.
{package_count} post-admission package/source/alpha checks also pass.

## Next action
Paired bunk normal admission and remaining real furniture contexts, broader
natural-world task/hazard verification and full cross-family master polish.
No blocker, commit/export or final owner acceptance claim.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
(P/'native-evidence.json').write_text(json.dumps({'native':n,'nativeChecks':count,'records':28,'futureActorUpdates':8400,'malformedGuards':224,'existingAndBoundarySelectorGuards':16,'distinctHeldEntrancesPerGear':True,'normalSelection':True,'postAdmissionPackageChecks':package_count,'postRunMetadata':metadata,'visual':visual,'scope':'Rotation0 prescribed mortality/disk/fresh-main-scene actor-future Continue; no manifest injection'},indent=2)+'\n')
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 t=path.read_text(encoding='utf-8')
 if heading not in t:path.write_text(heading+'\n'+note+'\n'+t if path.name=='CURRENT_STATUS.md' else t.rstrip()+'\n\n'+heading+'\n'+note+'\n',encoding='utf-8')
print(f'{count} native checks/28 normal cases recorded in handoff and five lesson targets')
