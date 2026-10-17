"""Record South source family, true staged course, and controlled-cut limits."""
from pathlib import Path
import json,os,hashlib,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'native-handoffs-candidate-evidence.json').read_text());v=json.loads((P/'native-handoffs-candidate-validation.json').read_text())
assert e['failures']==0 and v['exitCode']==0 and not v['timedOut']
assert len(e['controlledCuts'])==44
assert not any('ERROR:' in line for line in (P/'native-handoffs-candidate.log').read_text().splitlines())
m=json.loads((P/'handoffs-manifest.json').read_text());states={s['id']:s for s in m['states']};assert len(states)==50
assert {k:len(x) for k,x in e['frameCoverage'].items()}=={'meal-acquire-south':8,'eat-south':6,'meal-deposit-south':8,'cup-acquire-south':8,'drink-south':6,'cup-deposit-south':8}
views=[];times=[]
for action,repeats,budget in [('meal-acquire',1,900),('eat',3,1400),('meal-deposit',1,900),('cup-acquire',1,900),('drink',1,1200),('cup-deposit',1,900)]:
 state=states[action+'-south'];ds=state['frameDurationsMs'];total=sum(ds);durations=[round(d*budget/total) for d in ds];durations[-1]+=budget-sum(durations)
 for repeat in range(repeats):
  for index,duration in enumerate(durations):
   im=Image.open(P/'handoff-captures'/f'{action}-{index:02d}.png').convert('RGB');view=Image.new('RGB',(432,458),'#303b40');view.paste(im,(0,26));ImageDraw.Draw(view).text((8,8),'Staged native source review / '+action+f' {index}',fill='white');views.append(view);times.append(duration)
assert sum(times)==9000
views[0].save(P/'native-course-review.gif',save_all=True,append_images=views[1:],duration=times,loop=0)
selection=json.loads((P/'selection.json').read_text());selection['status']='south_bowl_cup_handoffs_and44returns_staged_normal_binding_pending'
selection['handoffsCandidate']={
 'manifest':'handoffs-manifest.json','normalStates':6,'derivedReturnStates':44,'totalStates':50,
 'newCupWholeSourcePoses':3,'uniquePoseCoverageWarning':'Deposit reversals and44return variants reuse whole sources; these are not50 newly authored animations.',
 'cupSource':'cup-source-v2.png','cupPrompt':'cup-source-prompt-v2.txt','cupOriginal':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-fd2ca656-ef8e-45da-93c8-3fde1c81d95d.png',
 'retractSource':'cup-retract-source.png','retractPrompt':'cup-retract-prompt.txt','retractOriginal':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-f7f34dcb-db41-4fc1-a36f-ef7ae1598a27.png',
 'registration':'cup-registration.json','nativeChecks':e['checks'],'nativeFailures':0,
 'normalCourseSeconds':9,'normalTextureCoverage':44,'controlledDrawerReturns':44,
 'currentLiveIdleCanvas':'184x184','registeredHandoffCanvas':'256x256','completionJoin':'Full image at metadata pivot, not fixed184x192 crop',
 'review':'native-course-review.gif','reviewMethod':'Actual source-event captures assembled at declared handoff/3mouthful/1sip clocks; not a frame-rate video recording.',
 'ownerVisualAcceptance':False,'productionInstalled':False,'strictOwnerProfileUnchanged':v['realProfileUnchanged'],'profileDelta':v['profileDelta'],
 'remaining':['Production South state/loader binding','Real hazard/gear/movement interruption eligibility and clearance','Eight-index snapshots and pause/Continue','Other open-counter placements/rotations/adjacent-prop context','Full master/face/proportion review and full-set cross-family polish']}
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
note='''

## James South bowl/cup handoffs and return-source family — October 1, 2026

Full James/master/style/perspective/size/height/proportion/grade and later
cross-family polish goal active. New cup v1 rejected: widened stance/duplicate
torch. v2 gives deep cup and midlift at ONE .22236842 matching deep-empty ruler;
its upright panel compresses lower legs, so remains unused. Independently edited
whole bowl-retract reference becomes left-held gray cup/right empty relaxed arm,
one belt wrench/holstered torch; full matching-pose density .12734494 to134.095
projected body height, not per-part scaling. Fixed pooled neutral/gold source
curves against master. Four shared empty poses and exact selected cup-held
endpoint retained. No body splicing/limb painting/mirroring. All prompts/raw
sources/rejections retained. Cup neutral medians61..64R/59..63G/59..63B;
unchanged inherited eat/drink loops63..65R/61..63G/60..61B. Broad metrics are not
head identity or complete perspective/skin-material proof; full source review stays open.

Staged handoffs-manifest has6normal states:8pose bowl/cup pickup, exact reversed
8pose deposits, and unchanged padded6pose eat/drink. Plus44source-index return
variants: pickup prefix reversal, deposit suffix, mouth lowering to neutral then
deposit. Their first pixels/depth and final empty stance are exact. These reuse
whole South sources, not50new independently authored animations. Package44
endpoint chains pass. Actual supported South chooser/in-room route and original
Life.next6s meal->3s drink are exercised via TEMPORARY CandidateJames presentation;
all44normal textures and5phase joins plus final live empty idle pass, then44
controlled source-index return dispatches pass first/depth/terminal checks.
1410native checks/0fail, engine0/clean/no timeout; scratch APPDATA correct. Strict
owner-profile guard false,last_session.json only; attribution unproven. Actual
cup4/5/6 and deposit4 native captures reviewed: worktop cup contact, intermediate
lift and body-matched retract; toolkit stays holstered/attached. Contact49 remains
limited to tested open prep at[0,126]/foot[48,128].

Initial1408/1410runs failed final comparison because fixture assumed184x192
live idle; diagnostic proved unchanged South foot/idle with actual184x184.
Register ENTIRE images by metadata pivots on256plane; complete bytes now match,
without clipping away extra pixels. Both failure records retained. Never weaken
a join or alter art until actual phase/direction/pivot/canvas are observed.
native-course-review.gif reconstructs declared9s course from actual source-event
captures (three mouthfuls/one sip), not a frame-rate recording or full production
journey. HANDOFF and selection preserve scope. No normal controller/loader change,
real interruption-decision/clearance, eight-index snapshot or Continue proof.

Next bind supported South lifecycle/manifest and preserve North behavior, replacing
North-only direction and fixed0..5 snapshot/return assumptions with valid source
counts/facing. Test actual hazard/gear/movement cuts, pauses/Continue and other
counter placement/rotation/neighbor contacts before production selection. Continue
remaining rest/life/death contexts and eventual full-set consistency/polish; do
not substitute this50state candidate or1410checks for complete-goal acceptance.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=path.read_bytes()
 if b'## James South bowl/cup handoffs and return-source family' in old:continue
 data=note.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+note.encode();tmp=path.with_name(path.name+'.james-handoffs.tmp');tmp.write_bytes(data);os.replace(tmp,path)
handoff=P/'HANDOFF.md';archive=P/'HANDOFF-before-south-cup.md'
if not archive.exists():shutil.copy2(handoff,archive)
handoff.write_text('''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James full-set goal / South meal lifecycle

## Objective and acceptance
Full animation set faithful to masters/style/perspective/size/height/proportions/grade; keep skills/pipeline/bible current, then full cross-family consistency/polish. Goal active; South candidate not production or owner-selected.

## Accepted decisions and constraints
Matte neutral James, fixed belt wrench image-left and holstered torch image-right; no hand wrench, duplication or limb/body splices. Whole authored source density and metadata foot pivots; preserve North-only raised counters and owner layouts. Existing registered open prep supports South service, source fixture at[0,126]/foot[48,128]. Contact49 proved only this placement.

## Current state
Staged South handoffs-manifest:6normal states/44normal source slots,44derived source-index returns (not new authored pose coverage). Three new whole cup poses fit against canonical contact and existing bowl-retract body. Both pickup/deposit8poses/900ms; exact master and held joins; inherited eat/drink6poses unchanged. Prompts/raw/rejections, palette/ruler/audits and source package proof in this folder. Source body neutral/gold calibrated; full face/anatomy/context review remains. Prior notes archived HANDOFF-before-south-cup.md.

## Verification
Native1410/0fail: actual normal chooser/route and original meal6s->drink3s Life.next through all6phase textures, exact joins and final full live idle registered184x184 to256plane;44controlled return drawer cuts exact first/depth/terminal. Cup/deposit scene poses visually reviewed. No normal producer/loader, actual hazard/clearance cuts, source-count8 snapshots or Continue proof. Engine0/clean/no timeout/scratch APPDATA; strict owner-profile guard false,last_session.json only, cause unproven. Two prior fixture-only final-size failures retained. native-course-review.gif is actual source captures assembled at declared9s clocks, not direct video or production journey.

## Next action
Inspect current production branforth_npc.gd and loader. South needs active lifecycle/facing gate, full literal manifest loading, source-count-aware return/index snapshots and actual interruption policy. Preserve existing North behavior and equipment suppression. Prove real cuts/pause/Continue and other open-counter contacts before selection. Then remaining James contexts and full-set polish. No outstanding native process; latest owned handle26104 terminal.
''')
print(json.dumps({'nativeChecks':e['checks'],'states':50,'derivedReturns':44,'newCupWholePoses':3,'productionInstalled':False,'fullGoal':'active'}))
