"""Record normal bunk admission only after native, source and visual evidence."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-selected-native-v1'
n=json.loads((O/'validation.json').read_text());c=json.loads((R/'output/veld-bunk-selected-continue-v1/validation.json').read_text())
v=json.loads((P/'visual-review.json').read_text());review=json.loads((P/'review-evidence.json').read_text());metadata=json.loads((P/'post-run-metadata.json').read_text())
assert n['passed'] and c['passed'] and metadata['passed'] and v['reviewedBoards']==review['boards'] and len(review['boards'])==18
assert review['missingReplaySources']==0
packages=[json.loads((R/'character'/f/'package-checks.json').read_text()) for f in ['veld-bunk-body-master-v1','veld-bunk-early-fall-v1']]
assert all(x['failures']==0 and x['normalSelection'] for x in packages)
case_counts={};steps=0
for label in ['settle','early','fire','continue']:
 rows=json.loads((R/'output'/('veld-bunk-selected-'+label+'-v1')/'records.json').read_text());case_counts[label]=len(rows)
 for row in rows:
  assert len(row['reference'])==len(row['resumed']);steps+=len(row['reference'])+len(row['resumed'])
assert case_counts=={'settle':4,'early':8,'fire':6,'continue':8}
continue_checks=int(re.search(r'VELD BUNK BODY RESUME: (\d+) checks,0 failures',(R/'output/veld-bunk-selected-continue-v1/native.log').read_text())[1])
checks=sum(s['checks'] for s in n['suites'])+continue_checks;package_count=sum(p['checks'] for p in packages)
heading='## Veld paired bunk body and falls normally selected - October 2, 2026'
note=f'''
grid_canvas now admits paired master-body bunk and early floor-fall manifests
through four whole literal paths. ACTIVE_ASSETS records both bare/helmet families;
other selections preserved. Existing42PNG/72references in seven states retained:
entry7/exit7/sleep1/held death3/supported settle7, early standing fall6/crouch5
per gear. Fixed256x272/p128,224/H148, exact master endpoints and pooled materials;
no source redraw, grade/rescale, room geometry, controller or save-rule change.

Six normal-loader native suites: {checks} checks/0failures, all engine0/clean logs.
No test-only manifest injection; every fresh scene binds all72 production frame
references exactly to the paired source files. Actual need choice/route/arrival/
complete rest in both gears:2cases/38source-native captures, including final walk
and exact standing exit. World main is paused and actor updates are stepped;
this is real actor choice/navigation, not natural whole-world scheduler cadence.

Four rotations/two gears/lower and reverse rise/five supported poses:80actual
actor mortality APIs,320same-clock actor-file restores,640malformed guards and
early unsupported exclusions.18native sequences sampled through support and
relaxed terminal; all80source clocks checked by an independent authored oracle.
This is actor-level mortality, distinct from world roster/death bookkeeping.

26ordinary eligible RunSave disk reads/writes and fresh-main-scene continuations:
4supported world deaths,8early floor world deaths,6fire-rise/refuge phases,
6living lower/held/rise saves and2held world deaths. {steps}reference+resumed future
actor updates total, exact source/contact/depth/gear/foot/timer/needs/corpse and
pause equivalence.14actual RoomFlooding.kill cases;32early malformed guards.
Fire restores actual fire predicate/escape goal, holds foot through finite rise,
reaches exact standing master before the actual clear-floor refuge route.
Normal save eligibility uses existing paid Bill ward wake; repair route not
certified. Fresh scene is not title/new-process Continue.

All18normal native/source/master boards visually reviewed, including four room
rotations and future fall/fire/Continue sources. {v['finding']}
{review['nativePresentations']}native room presentations retained beside exact source captures;
interactive replay reconstructs26saved source/foot/offset traces, not continuous
native world video. Fire route may leave its fixed replay canvas; native room
boards preserve the submitted captures. Owner final/world motion review open.
Fire captures omit intermediate walk images but retain per-step pixel hashes:
80selected locomotion PNGs bind exactly to those native hashes, padding only.
Their post-run pixel bindings complete replay references; those walk PNG files
were not frozen in the prior native interval. Keep this separate from admission
of new artwork or another native gameplay run.

Both frozen intervals pass: {n['targetedInputCount']}targeted inputs across five suites and
{c['targetedInputCount']}in living/held Continue unchanged. Broader scene dependencies
not frozen. Scratch APPDATA preserved all{n['realProfileFileCount']}owner non-log files
in both intervals. Post-run four manifest status fields metadata-only; registry
additions preserve other actors. {package_count}package/source/alpha checks0fail after
admission; all42PNGs unchanged. Historical staged reports keep original scope.

Lesson: adopt paired furniture motion with a normally loaded need-driven route,
not only parked candidate poses. Keep whole body and shared shell on one ruler,
then distinguish mattress-supported settling from early unsupported floor falls.
Check forward/reverse partial clocks, living and dead Continue, actual room depth,
and finite emergency standing before navigation. Freeze loader and registry with
source inputs; normal-family admission is separate from natural hazard cadence.

Next remaining real seated/tablet interruption/fall contexts (South sofa differs
from North lounge), broader whole-world task/hazard cadence and full-library
master/style/perspective/height/proportion/material/motion polish. Full Veld goal
active/incomplete; no final owner acceptance, commit or export claim.
'''
handoff=f'''# Project handoff

Updated:2026-10-02 · Project:BrineSpace · Task:Paired bunk normal admission

## Objective and acceptance
Full master-matching Veld set followed by cross-family consistency/polish remains
active. Paired East bunk now normally admitted; full world/owner acceptance open.

## Accepted decisions and constraints
Retain all42original PNGs, whole body/native shared helmet and H148 ruler.
Keep registered mattress/floor contact, physical foot, finite standing escape,
original furniture/owner geometry and ordinary save/needs/mortality rules.

## Current state
scripts/grid_canvas.gd loads four whole bunk body/early-fall manifest paths.
ACTIVE_ASSETS registry plus authoring status/build/validator labels updated.
Six normal tests with paired UIDs, scratch runners,18native/source/master boards,
26future replays and evidence here. Pipeline/bible/both crew-life copies updated.
No raster, controller, save-rule or unrelated actor selection changes.

## Verification
{checks}native checks0fail across six suites;2need-driven rest cycles,
80supported actor deaths/320actor-file restores across4rotations,
26ordinary eligible disk/fresh-main-scene continuations/{steps}future actor steps.
14world mortality cases,6fire phases,672malformed guards; all18boards reviewed.
{package_count}post-admission source/package checks pass; all42PNGs exact.
{n['targetedInputCount']}/{c['targetedInputCount']}targeted inputs and {n['realProfileFileCount']}owner files unchanged during intervals.
Main paused/actor stepped; prescribed hazards and most disk cases rotation0,
not natural world scheduler/hazard cadence, title/new-process or owner acceptance.

## Next action
Check actual remaining South sofa/read interruptions/falls against masters,
broader whole-world task/hazard cadence and full-family consistency/polish.
No blocker, commit/export or full-goal completion claim.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
(P/'native-evidence.json').write_text(json.dumps({'normalLoaderOnly':True,'native':n,'livingHeldContinue':c,'nativeChecks':checks,'packageChecks':package_count,'naturalActorRestCases':2,'partialActorDeaths':80,'sameClockActorFileRestores':320,'freshMainSceneDiskCases':26,'futureActorUpdates':steps,'actualWorldMortalityCases':14,'firePhases':6,'malformedGuards':672,'visual':v,'review':review,'metadata':metadata,'fullGoalComplete':False},indent=2)+'\n')
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 text=path.read_text(encoding='utf-8')
 if heading not in text:path.write_text(heading+'\n'+note+'\n'+text if path.name=='CURRENT_STATUS.md' else text.rstrip()+'\n\n'+heading+'\n'+note+'\n',encoding='utf-8')
print(f'{checks}native checks/26fresh disk cases/{steps}future updates recorded with scoped visual evidence and five lesson targets')
