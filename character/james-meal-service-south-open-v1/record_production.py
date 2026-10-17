from pathlib import Path
import json,os,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'native-handoffs-production-evidence.json').read_text());v=json.loads((P/'native-handoffs-production-validation.json').read_text())
n=R/'character/james-meal-interrupt-north-v1';ne=json.loads((n/'native-return-evidence.json').read_text());nv=json.loads((n/'native-return-validation.json').read_text())
for evidence,validation,log in [(e,v,P/'native-handoffs-production.log'),(ne,nv,n/'native-return.log')]:
 assert evidence['failures']==0 and validation['exitCode']==0 and not validation['timedOut']
 assert 'ERROR:' not in log.read_text()
assert len(e['controlledCuts'])==44
assert {k:len(x) for k,x in e['frameCoverage'].items()}=={'meal-acquire-south':8,'eat-south':6,'meal-deposit-south':8,'cup-acquire-south':8,'drink-south':6,'cup-deposit-south':8}
m=json.loads((P/'handoffs-manifest.json').read_text());states={s['id']:s for s in m['states']};views=[];times=[]
for action,repeats,budget in [('meal-acquire',1,900),('eat',3,1400),('meal-deposit',1,900),('cup-acquire',1,900),('drink',1,1200),('cup-deposit',1,900)]:
 ds=states[action+'-south']['frameDurationsMs'];durations=[round(d*budget/sum(ds)) for d in ds];durations[-1]+=budget-sum(durations)
 for repeat in range(repeats):
  for index,duration in enumerate(durations):
   im=Image.open(P/'production-captures'/f'{action}-{index:02d}.png').convert('RGB');view=Image.new('RGB',(432,458),'#303b40');view.paste(im,(0,26));ImageDraw.Draw(view).text((8,8),'Production source review / '+action+f' {index}',fill='white');views.append(view);times.append(duration)
assert sum(times)==9000
views[0].save(P/'production-course-review.gif',save_all=True,append_images=views[1:],duration=times,loop=0)
selection=json.loads((P/'selection.json').read_text());selection['status']='south_supported_contact_production_bound_power_loss_and_index7_continue_verified';selection['productionArtInstalled']=True
selection['productionEvidence']={'nativeChecks':e['checks'],'normalTextures':44,'actualPowerLossCuts':44,'snapshots':44,'freshSceneDiskContinue':'cup-acquire index7','northRegressionChecks':ne['checks'],'ownerVisualAcceptance':False,'strictOwnerProfileUnchanged':v['realProfileUnchanged'],'profileDelta':v['profileDelta'],'remaining':['Other hazards/gear/movement interruptions','Other open-counter placements/rotations/neighbors','Full master/face/anatomy review','Remaining James physical contexts and full-set polish']}
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
active_path=R/'character/ACTIVE_ASSETS.json';active=json.loads(active_path.read_text());active['actionOverrides']['branforth-south-meal']='character/james-meal-service-south-open-v1/handoffs-manifest.json';active_path.write_text(json.dumps(active,indent=2)+'\n')
note=f"""

## James supported South meal production lifecycle — October 1, 2026

Normal branforth_npc controller and grid_canvas loader now bind six South meal/cup
phases plus44 derived source-index returns at the reviewed open prep relative
contact[48,2], rect91.12x50.32, no flip. Other contacts retain prior presentation;
no owner layouts/defaults changed. Existing North activation and implicit North
save shape preserved. Durations/source counts derive from full literal manifests,
so South eight-pose source indices6/7 validate without admitting invalid indices.
Helmet profile loads before padded bare override to preserve equipment validation.
Return rendering invalidates stale idle cosmetic phase, giving exact idle-frame0
join after simulation-owned return instead of resuming old breathing pixels.

{e['checks']} South native checks pass: normal chooser/route and nine-second course,
all44 normal textures, exact five phase joins/full idle;44 actual power-loss cuts
from selected source clocks, exact first pixels/depth, no interrupted hunger credit,
fixed foot/facing, completion/full idle; all44 valid snapshot restores and bounds,
fresh-scene disk Continue/paused actor-clock-pixels at cup-acquire index7.
North existing real return fixture passes{ne['checks']} checks with six fresh-scene
Continues. Engines0/clean/no timeout/scratch APPDATA. Strict profile guards South
{v['realProfileUnchanged']}/North{nv['realProfileUnchanged']}, delta{v['profileDelta']}/
{nv['profileDelta']}; last_session attribution unproven, no owner rollback.
Earlier fixture failures retained: base valid_snapshot missed actor extension;
then old cosmetic idle phase caused44 exact endpoint failures. Actor-specific
validator and actual idle-clock reset solve causes; no art edits or weaker checks.
Production cup4/6 captures visually reviewed. production-course-review.gif uses
actual normal-loader source-event captures at declared nine-second timings, not
direct frame-rate video. Other hazards/gear/movement, contact placements/rotations/
neighbors and full master/anatomy/cross-family polish remain. Full goal active.
"""
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=path.read_bytes()
 if b'## James supported South meal production lifecycle' in old:continue
 data=note.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+note.encode();tmp=path.with_name(path.name+'.james-production.tmp');tmp.write_bytes(data);os.replace(tmp,path)
hand=P/'HANDOFF.md';archive=P/'HANDOFF-before-production.md'
if not archive.exists():shutil.copy2(hand,archive)
hand.write_text('# Project handoff\n\nUpdated:2026-10-01. Objective: full James animation/master consistency set, then cross-family polish. Active.\n\nAccepted constraints: matte neutral master, belt wrench/torch remain attached; whole-source poses and common pivots; preserve North and owner layouts.\n\nChanged: scripts/branforth_npc.gd facing-aware manifest clocks/source-count snapshots and supported South lifecycle; scripts/grid_canvas.gd normal manifest after helmet validation, stale idle reset; ACTIVE_ASSETS; native-handoffs-production.gd plus paired UID, production captures/evidence/review; maintained pipeline/bible/skill notes.\n'+note+'\nNext: additional real hazard/gear/movement cuts and supported open-prep translations/rotation/adjacent-prop clearance, then remaining James contexts/full master/face/anatomy and cross-family polish. See source HANDOFF-before-production.md for authoring provenance.\n')
print(json.dumps({'southChecks':e['checks'],'northChecks':ne['checks'],'productionBound':True,'ownerAcceptance':False,'fullGoal':'active'}))
