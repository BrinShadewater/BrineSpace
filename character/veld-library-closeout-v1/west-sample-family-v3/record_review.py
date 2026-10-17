from pathlib import Path
import json,hashlib,uuid,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f,h in json.loads((P/'FAMILY_REVIEW.json').read_text())['bindings'].items():assert sha(R/f)==h
inv=json.loads((R/'character/veld-library-closeout-v1/installed/selected-library.json').read_text());refs=set();manifests=set()
for gear in ['bare','helmet']:
 for key in ['idle-west','walk-west','interact-west','kneel-west','repair-west','stand-west']:
  row=inv['resolved'][gear][key];refs.update(row['frameFiles']);manifests.add(row['manifest'])
for f in refs:assert sha(R/f)==inv['sourceBindings'][f]
for f in manifests:assert sha(R/f)==inv['bindings'][f]
for f in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json']:assert 'west-sample-family-v3' not in (R/f).read_text()
(P/'SELECTION_REVIEW.json').write_text(json.dumps(dict(unchangedWestSources=len(refs),unchangedWestManifests=len(manifests),failures=0,normalSelectionChanged=False),indent=2)+'\n')
for name in ['veld-west-sample-family-v3','veld-west-sample-controller-v3']:assert json.loads((R/f'output/{name}/validation.json').read_text())['passed']
title='## Veld original West complete sample cycle staged — October 4, 2026'
note=title+"""

West one-knee lower/examine-stow/rise now staged as a coherent1s/4s/1s family
at character/veld-library-closeout-v1/west-sample-family-v3/. Bare/helmet share
57lower poses from kneel-motion-v2 source14..70,142new examination poses, and
same57whole poses reversed for rise. No body/foot patches or grading. Same256
canvas/pivot128224/standingHeight148. Existing original rigid West shell;
bodyoutsidehelmet exact142/142 in new examination. Viewer loop is replay only.

Corrected contact diagnosis: original front/far toe ends219, near/rear boot223.
Old x<133ground band included the rear boot's toe then lost it as rear leg lifted;
its apparent3pxfrontsole lift was mixed-foot measurement. Separate fronttoe ROI
105..121,y210..230 gives source220..221 and x107..108:1px downwardsettling/0up,
not3pxlift. Registered authoredkey toe221. Original alpha-edge difference1..2px
is below1px at47pxcharacterheight; no pressure/worlddepth proof. Old reports kept;
corrected evidence kneel-motion-v2/CORRECTED_FRONT_TOE_REVIEW.json and ankle board.
Do not paint originalboot over movingleg on this false lift diagnosis.

One scoped kneeling examination Hailuo02 job448697760727515 succeeded;
6s768P24fps, estimatedUSD0.28/billingunverified. Same first/last input is existing
lower endpoint70, no regenerated identity. Exact prompt/input/task/full142source
retained at west-examine-kneeling-v1. All142raw/bare poses reviewed: headtop118,
headwidth27/axis148 throughout, floor222..223. Small vial drawn/examined/stowed;
empty hand before rise. Slight vial silhouette variation during return remains
for motion review; fixed colour ROI is a diagnostic, not rigidprop/grip proof.
Whole source5917ms uniformlyretimed4000ms(~1.47925x), every pose retained;
lower remains2.375x. Full unretimed sources visible.1028joined build/APNG checks
pass; saved builder reproduces7outputartifacts byte-exact.

3122final nativeplayer checks/512presentations at47/93/148px pass.5846actual
controlled-scene NPC checks pass:2ordinary maintenance cycles, arrival dispatch,
57/142/57slot coverage each gear at120Hzcontrolled sampling, fixed worldfoot,
valid actorsnapshots, stowedvial/finitephase/returnidle and maintenance reward.
Actual repair starts1.0083s/stand5.0167s due discrete timerstep; no timercodechanged.
20native room/sourcecaptures, representative bareexamination and helmetrise
visually reviewed. This is actual controlled NPC/render submission evidence,
not free-runningstation/controllerinterruption/worldpressure/diskContinue proof.
1030targetedinputs and2931ownerprofilefiles unchanged in each passing interval.
Selected West274PNGs/4manifests unchanged; no normal admission/controller changes.

First intervals preserved: playerfixture sampled4s after4.00001s causing clock
reset, corrected to monotonic sample; controllerfixture incorrectly expected
emptygoal aftercompletion. Probe showed idle with nextmaintenance route planned
and reward applied; expectation corrected without gameplayedit. Evidence under
output/veld-west-sample-family-v3-first-clock-check and controllerfirst-next-goal/
probe; finalpassing outputs veld-west-sample-family-v3/veld-west-sample-controller-v3.

Next: review complete motion and adjoining Westcargo/stance/material joins before
coherent normal admission; maintenance interruption and fresh-processContinue
remain open, along with other directional closeout. Full Veldlibrary incomplete.
Preview index.html and HANDOFF.md here. No live job or approval gate.

"""
(P/'HANDOFF.md').write_text("""# Project handoff

Updated: October 4, 2026 · Brine Space · Veld West complete sample sequence

## Objective and acceptance
Finish Veld against original masters. This interval stages coherent West lower/examine-stow/rise, checked through actual controlled-scene maintenance controller in both gears. Normal admission/full library remain open.

## Accepted decisions and constraints
Same original standing and existing one-knee endpoint, fixed whole extraction; no anatomy/RGB/boot edits or per-frame reposition/scale. Original rigid helmet shell; bodyoutsidehelmet exact. Preserve sources and approved planted turns. Earlier frontlift diagnosis corrected using separate boots, not patched art.

## Current state
Paired sequence manifests/APNGs here:57lower/142examine/57rise,1s/4s/1s. Lower source14..70 retimed2.375x, rise exactreverse. One new examination task448697760727515 (estimatedUSD0.28/billingunverified), samefirst/last loweringendpoint70 input, complete142raw poses retained under ../west-examine-kneeling-v1,5917ms uniformlyto4000ms(~1.47925x). Vial stowed before rise, slight silhouettevariation during return remains for review. Same256/pivot128224/H148. No normal selection/controller change.

## Verification
All142examinationraw/bareposes, helmetvial details and paired sixjoinpanels viewed.142helmet exactbody checks.1028joinedbuild/APNG checks; savedbuilder7artifacts byte-exact.3122nativeplayer checks/512presentations at47/93/148 pass, entry/finiteendpoint/idle/freshplayerrestore.5846actual controlled-scene NPCchecks:2maintenance arrival/lower/repair/stand cycles, all57/142/57slots sampled at120Hz pergear, fixed worldfoot, validactor snapshots, maintenance reward/idle return.20native room/sourcecaptures, representative bareexamine/helmetrise reviewed.1030inputs/2931owner files unchanged perpassing interval,274selectedWestPNGs/4manifests unchanged. Evidence output/veld-west-sample-family-v3 and veld-west-sample-controller-v3.

## Corrections and retained evidence
Frontfar mastertoe219 vsnearboot223. Oldbroadband mixedfeet, falselyflagged3pxlift. Newfronttoe ROI source220..221,x107..108:1pxdown/0up; originalalphaedges1..2pxdifference below1px at47pxheight. No boot edit needed on that diagnosis. Corrected report in kneel-motion-v2. Firstplayer testclockbackwards fixed; controlleremptygoal assumption fixed after probe showed idle+plannednextmaintenance route/reward. Failedintervals/probe preserved; no gameplay changes.

## Next action
Review complete motion and Westcargo/stance/material joins before coherent admission. Verify service-loss/interruption and full fresh-processContinue; other directional materials/furniture/water/death coverage still open. Actual fixture proof does not establish free-runningstation, physical pressure/worlddepth or real-time60Hz coverage. Full library unfinished; no live job/approval gate.
""",encoding='utf-8')
(P/'VERDICT.md').write_text('# Staged coherent West sample cycle\n\nComplete1s lower/4s examine-stow/1s rise, both gears;3122player and5846actual controlled-scene NPCchecks pass. Corrected mixed-foot measurement: no3pxfrontlift and no boot patch. Slight source/detail/prop variation remains for motion review. No normal admission, interruption or fullContinue acceptance. See HANDOFF.md.\n',encoding='utf-8')
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(20):
  with path.open('r',encoding='utf-8') as f:head=''.join(next(f,'') for _ in range(120))
  if title in head:break
  before=path.stat();tmp=path.with_name(path.name+'.veld-'+uuid.uuid4().hex+'.tmp')
  with tmp.open('wb') as dest,path.open('rb') as source:dest.write(note.encode('utf-8'));shutil.copyfileobj(source,dest,1024*1024)
  after=path.stat()
  if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):tmp.unlink();time.sleep(.5);continue
  try:tmp.replace(path)
  except PermissionError:tmp.unlink();time.sleep(.5);continue
  print(path.name,'updated');break
 else:raise RuntimeError('Concurrent update prevented prepend: '+str(path))
parent=P.parent/'HANDOFF.md';section='\n## Original West complete sample cycle staged — October4\nCoherent1s lower/4s examine-stow/1s rise in both gears.3122player/5846actual controlled-NPC checks pass;all57/142/57slots pergear, fixedworldfoot. Corrected3pxlift flag mixednear/farfeet; fronttoe actuallysettlesdown1px. One new sourcejob448697760727515 estimatedUSD0.28, all142retained. No normal admission/interruption/Continue proof. See west-sample-family-v3/HANDOFF.md.\n'
text=parent.read_text(encoding='utf-8')
if '## Original West complete sample cycle staged' not in text:parent.write_text(text+section,encoding='utf-8')
print('Selected West274source files/4manifests unchanged; final evidence verified.')
