from pathlib import Path
import json,hashlib,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[2];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();v=json.loads((R/'output/veld-west-unload-source-v1/validation.json').read_text());assert v['passed'] and not v['realProfileChanges']
hand="""# Project handoff

Updated: October 4, 2026 · Brine Space · West unloading and reversed pickup source

## Objective and acceptance
Continue Veld original-master closeout. Whole unloading/reversedpickup motion is staged at source clock, not installed or final game-timing acceptance. Full library unfinished.

## Accepted decisions and constraints
Original-master cargo key starts; original complete neutral standing is reused for the deposited endpoint. One isolated-case builtinimagegen edit reconstructs occluded case edges from held high-resolution master, not a regenerated body. Fixed whole-canvas768-to256 extraction, no per-pose scaling/recentering, grading or anatomy stencils. Original rigid West shell follows source head; outside-shell body exact. Preserve old selected520ms action timing and accepted gait/turns until whole-family cadence/joins pass.

## Current state
One directMiniMax Hailuo02 task448731366560219 succeeded,6s768P24fps, estimatedUSD0.28/billingunverified; first/last conditioned. Exactprompts, images, case source and fullvideo retained. Firstconditioning nativekey exact; finalconditioning complete originalstanding pixels exact plus32x18 matching reconstructed case at72,206. Actualgenerated output is not identical to those controls. All142source slots5917ms retained; paired source-unload-west and source-pickup-west manifests use fullsourceclock; pickup exactreverse, no new images. Four APNGmotionpreviews,12bare/helmetchronologyboards, endpointboard and rawvideo in index.html. Viewer repeats are replay, not a game transition. No normal loader/controller change or livejob.

## Verification
3endpoint packaging/284rawAPNG/1278familyAPNG+outsidebodychecks0.149family outputs rebuild byte-exact.3438nativeplayer checks0,568three-scale presentations(47/93/148px): allsource slots/pixels/pivot/density/dry state, finiteentry/terminal/idle return and freshplayer snapshot clocks. Fourrepresentative nativeframes viewed, all142barechronology and142helmethead/neck views inspected; browserpreview visibility verified.923inputs/2936owner nonlogfiles unchanged in scopednativeinterval. Selected ending-West722PNGs/38manifests unchanged. Native evidence output/veld-west-unload-source-v1; tests/test_veld_west_unload_source_v1.gd+UID and tools/run_veld_west_unload_source_v1.py.

## Limits and remaining work
Standing generated headtop76/width26..28 vs27master. Top16row width26..45 during bend includes shoulder/backpack; not anatomical head growth (HEAD_METRIC_NOTE). Boots change lower-outline bounds(left105..111,right142..148); alpha128 floor223..224 while alpha200globalfloor222..223. Do not claim exact plantedfoot geometry/worldroot from playerfixture. Stable depositedcase96..141 has bbox72..103,top205,floor223; earlier broadROI mixed glove/toe during rise and is corrected. Actual grip/rigidprop geometry still visually scoped, not certified. Helmet staysupright while translating, no tilted-neck/controller worldcontact acceptance. No continuously watched nativevideo, actualNPC/cargo route/return/service-loss/Continue proof.

## Next action
Choose an action phase/timing compatible with inherited520ms selected actions and actual controller contexts without hiding source movement or altering gameplay casually. Check whole carry/unload/pickup and plantedturn joins, slightfoot/head differences and case disposition. Source rawaction ends around95 then holds; no retiming done. Then controllerinterruption/freshprocessContinue and broader directional/furniture/water/death work before coherent normaladmission. No approvalgate.
"""
(P/'HANDOFF.md').write_text(hand,encoding='utf8');(P/'SOURCE_VERDICT.md').write_text('# Staged whole-source verdict\n\nAll142bare poses and142helmet head/collar views inspected. Connected whole-body lowering/release/rise is substantially closer to original master; pickup is exact reversal. Source-clock nativepixel/state checks pass. Keep all poses; no new source retry or anatomy/RGB/per-frame positioning correction. Staged for timing/contact/fullfamily review, not owner acceptance or normal admission. Small footoutline/headwidth differences and uprighthelmetfit remain disclosed.\n',encoding='utf8')
title='## Veld West unload and reversed pickup source staged — October 4, 2026';note=title+'\n\nOriginal-master cargo key to exact originalstanding+matchingdepositedcase endpoints, oneHailuo02 first/last job448731366560219 succeeded (6s768/24fps, USD0.28estimate/billingunverified). Full142source slots5917ms staged in character/veld-library-closeout-v1/west-unload-source-v1/, pairedhelmet and exactreversedpickup; source-prefixedkeys only, old520ms actions/normalselection unchanged.3endpoint/284rawAPNG/1278family checks0,149byte-exact rebuildoutputs,3438nativechecks0/568presentations. Allbare142chronology/helmet142headneck views+4nativeframes reviewed, visiblepairedbrowserpreview.923inputs/2936ownerfiles and ending-West722PNGs/38manifests unchanged. Footoutline/1pxalphaedge variance remains; topband45pxduringbend includesbackpack, notmeasuredheadgrowth. Stablecasebbox72..103/top205/floor223 after96. Sourceclock only, no controller/root/rigidprop/diskContinue or normaladmission proof. Next compatibleactiontiming/carry/turnjoins and controller gates; full Veldunfinished. No livejob or approvalgate.\n\n'
p=R/'docs/CURRENT_STATUS.md'
for attempt in range(20):
 before=p.stat();tmp=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp')
 with p.open('r',encoding='utf8') as f:
  if title in ''.join(f.readline() for _ in range(120)):break
 with tmp.open('wb') as out,p.open('rb') as src:
  out.write(note.encode())
  while chunk:=src.read(1024*1024):out.write(chunk)
 after=p.stat()
 if (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns):
  try:tmp.replace(p);break
  except PermissionError:pass
 tmp.unlink();time.sleep(.5)
else:raise RuntimeError('Concurrent status updates prevented guarded prepend')
parent=P.parent/'HANDOFF.md';heading='## West unload and reversed pickup whole source — October 4, 2026'
if heading not in parent.read_text(encoding='utf8'):
 with parent.open('a',encoding='utf8') as f:f.write('\n\n'+heading+'\n\nFull142source/5917ms bothgears+exactreverse staged in west-unload-source-v1. OneHailuo02job448731366560219 (USD0.28estimate/billingunverified), exactconditioningbody endpoints and allraw retained. Allbare/helmet chronology reviewed;3438nativechecks0/568presentations,923inputs/2936ownerfiles unchanged; oldending-West722PNGs/38manifests unchanged.149outputs rebuildexact; bootoutline/head/helmet/prop limits in localHANDOFF. Source-prefix keys only, no selected520ms timing/controller/normaladmission change. Next action-phase timing and carry/turn/controller joins; no livejob/approvalgate.\n')
files=[f for f in P.iterdir() if f.is_file() and f.name!='FINAL_REVIEW.json']+[R/'tests/test_veld_west_unload_source_v1.gd',R/'tests/test_veld_west_unload_source_v1.gd.uid',R/'tools/run_veld_west_unload_source_v1.py',R/'output/veld-west-unload-source-v1/validation.json'];(P/'FINAL_REVIEW.json').write_text(json.dumps({'scope':'Staged complete source-clock unload/reversepickup, not normal timing or controller admission','failures':0,'bindings':{f.relative_to(R).as_posix():sha(f) for f in files}},indent=2)+'\n',encoding='utf8');print('Recorded source milestone with',len(files),'bound deliverables.')
