from pathlib import Path
import json,os,hashlib,shutil
from PIL import Image,ImageDraw,ImageChops
P=Path(__file__).resolve().parent;R=P.parents[1]
runs={}
for name in ['native-handoffs-production','native-placements']:
 e=json.loads((P/(name+'-evidence.json')).read_text());v=json.loads((P/(name+'-validation.json')).read_text())
 assert e['failures']==0 and v['exitCode']==0 and not v['timedOut'] and 'ERROR:' not in (P/(name+'.log')).read_text()
 runs[name]={'checks':e['checks'],'failures':0,'strictOwnerProfileUnchanged':v['realProfileUnchanged'],'profileDelta':v['profileDelta'],'scratch':v['scratch']}
package=json.loads((P/'skin-grade-package-evidence.json').read_text());assert package['alphaAllExact'] and package['standingHeldAllExact'] and package['all50StateFramesClocksMetadataExact'] and package['cupRulersAnchorsExact']
e=json.loads((P/'native-placements-evidence.json').read_text());rows=[]
for x in e['depthSamples']:
 a=Image.open(R/x['selected'].removeprefix('res://')).convert('RGB');b=Image.open(R/x['reference'].removeprefix('res://')).convert('RGB');roi=(198,160,237,232)
 diff=ImageChops.difference(a.crop(roi),b.crop(roi));changed=sum(max(v)>0 for v in diff.get_flattened_data());assert changed==0
 rows.append({'key':x['key'],'roi':roi,'changedPixels':changed})
(P/'placement-depth-audit.json').write_text(json.dumps({'contexts':16,'southContexts':8,'northContexts':8,'depthSamples':32,'sameROI':32,'samples':rows,'scope':'Current corrected production source-event captures; contact ROI49 versus64, not a full anatomical or scene-acceptance proof.'},indent=2),encoding='utf-8')
m=json.loads((P/'handoffs-manifest.json').read_text());states={s['id']:s for s in m['states']};views=[];times=[]
for action,repeats,budget in [('meal-acquire',1,900),('eat',3,1400),('meal-deposit',1,900),('cup-acquire',1,900),('drink',1,1200),('cup-deposit',1,900)]:
 ds=states[action+'-south']['frameDurationsMs'];durations=[round(d*budget/sum(ds)) for d in ds];durations[-1]+=budget-sum(durations)
 for repeat in range(repeats):
  for index,duration in enumerate(durations):
   im=Image.open(P/'production-captures'/f'{action}-{index:02d}.png').convert('RGB');view=Image.new('RGB',(432,458),'#303b40');view.paste(im,(0,26));ImageDraw.Draw(view).text((8,8),'Corrected production source / '+action+f' {index}',fill='white');views.append(view);times.append(duration)
assert sum(times)==9000
views[0].save(P/'production-course-review.gif',save_all=True,append_images=views[1:],duration=times,loop=0)
selection=json.loads((P/'selection.json').read_text());selection['status']='south_supported_meal_skin_grade_corrected_production_verified';selection['skinMaterialCorrection']={'cause':'Legacy trim-height classifier included lowered facial skin and applied1.359 blue gain. Raw sources already warm. Ochre chroma selection now excludes red-dominant skin.','changedExportFrames':12,'uniqueExportFrames':28,'alphaAllExact':True,'standingHeldExact':True,'all50StatesMetadataExact':True,'sourceRulersExact':True,'faceReview':'skin-before-after-review.png','normalProductionReview':'production-course-review.gif','nativeRuns':runs,'ownerVisualAcceptance':False}
selection['contextEvidence']['materialDefect']='Localized purple deep-face cast corrected in build material selection; current source/native review confirms warm skin. Full head identity/anatomy and cross-family polish remain.'
selection['contextEvidence']['remaining']=[x for x in selection['contextEvidence']['remaining'] if not x.startswith('Deep contact skin')];selection['contextEvidence']['remaining'].insert(0,'Full head identity/anatomy/perspective consistency review')
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n',encoding='utf-8')
proof={'runs':runs,'package':'skin-grade-package-evidence.json','skinColorDefectCorrected':True,'fullGoal':'active','generatedNewSource':False,'normalTextures':44,'actualPowerLossReturns':44,'translatedRotatedCourses':16,'currentDepthComparisons':32,'sourceManifestSha256':hashlib.sha256((P/'handoffs-manifest.json').read_bytes()).hexdigest()}
(P/'skin-material-milestone.json').write_text(json.dumps(proof,indent=2),encoding='utf-8')
note="""

## James deep South face material classification corrected — October 1, 2026

Full James/master/style/perspective/size/height/proportion/grade and later full-set
cross-family polish goal active. Raw whole-contact sources already have warm skin.
Root cause was shared meal grade(): a y band measured from backpack/crown catches
the lowered face; loose gold thresholds then apply South trim gain B1.359, making
skin purple. Require ochre green-blue gap >1.2 red-green gap, with R>G, before trim
gain. Warm red-dominant skin now receives chroma-preserving matte luminance only.
Source authoring/art/anatomy/positions unchanged. Re-register fresh-contact directly
from raw v4 inside reach builder so rebuild cannot reuse stale already-graded PNG.

Targeted South rebuild changes12 of28 unique export frames. All28 alpha silhouettes,
exact standing/held endpoints, all50 state frame orders/clocks/depths/pivots and cup
rulers/anchors exact. Before-skin-material-fix archives old exports/builds/manifest
and hashes. Fixed face ROI formerly magenta skin23/8/19 pixels in empty/bowl/cup
now all R>G>B; corrected medians162,116,91 /154.5,106,82 /167,119,91. Broad whole-ROI
median originally obscured this defect with hair/collar/background pixels; material
semantic selection plus magnified face/source/native review is required.
Whole eight-pose bowl/cup board and before/after faces reviewed; current native
meal-acquire4 confirms warm face at worktop. No image generation needed for an
exporter bug; shared helper fixed, only this South package rebuilt. Other existing
family PNGs not regenerated and do not inherit a blanket new visual acceptance.

Current corrected normal production checks5446pass: all44 source textures/phase
joins,44 actual power-loss returns/snapshots/bounds, index7 fresh-scene disk Continue
and paused pixels/clock.16 translated/rotated South/North courses18308pass,32 current
South contact-depth ROI49/64 pairs exact. Engines0/clean/no timeout/scratch APPDATA;
both strict real-profile guards false,last_session.json only, attribution unproven.
Prior hazard/context policy evidence remains scoped to unchanged silhouettes/metadata;
those systems were not rerun for RGB-only grading. Review GIF assembles source-event
captures at nine-second clocks, not direct frame-rate video.

Current literal-source inventory refreshed:329 body states/4216 frame references,
239 equipped states/3700 references, zero retained-source status. These include
source-index derived returns and equipment substitutes, not that many newly authored
motions; not whole-set runtime/fidelity acceptance. Six meal family first/middle/end
source comparison boards refreshed. Board renderer now resolves whole res:// frame
paths, including shared North cup endpoints, instead of treating them as relative
filesystem names. Full pose/motion, head identity/anatomy/material and cross-family
consistency remain; North open-prep physical hand/contact, arbitrary scales/flips/
off-grid/neighbors, actual locker/crowd and further disk contexts remain open.
"""
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=path.read_bytes()
 if b'## James deep South face material classification corrected' in old:continue
 data=note.encode('utf-8')+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+note.encode('utf-8');temp=path.with_name(path.name+'.james-skin.tmp');temp.write_bytes(data);os.replace(temp,path)
hand=P/'HANDOFF.md';archive=P/'HANDOFF-before-skin-correction.md'
if not archive.exists():shutil.copy2(hand,archive)
hand.write_text('# Project handoff\n\nUpdated:2026-10-01. Full James/master consistency set and later full cross-family polish remain active.\n\nAccepted: matte neutral master, warm skin, attached belt wrench/torch; original whole sources, fixed density/pivots and exact endpoints; preserve owner layouts and North behavior.\n\nChanged: shared character/james-meal-family-v1/build.py ochre classifier; build_reach.py registers raw contact directly; build_handoffs.py current production status;12 South export PNGs and reviewed artifacts; skin package/native evidence; literal source inventory and six family boards, res:// review resolver; pipeline/bible/skill notes.\n'+note+'\nNext: North open-prep actual hand/worktop contact review, then remaining physical furniture/gear/crowd/Continue contexts and full head/face/anatomy/perspective/motion consistency. No owned native job remains live.\n',encoding='utf-8')
print(json.dumps({'skinDefectCorrected':True,'changedFrames':12,'currentNativeChecks':sum(x['checks'] for x in runs.values()),'allMetadataAndAlphaExact':True,'fullGoal':'active'}))
