from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;F=P.parent/'bill-meal-east-family-v1'
OUT=ROOT/'output/bill-drink-entry-east-candidate-native-v1';NATIVE=ROOT/'output/bill-meal-east-family-candidate-native-v1'
v=json.loads((P/'verification.json').read_text());n=json.loads((OUT/'validation.json').read_text());fv=json.loads((F/'verification.json').read_text());fn=json.loads((NATIVE/'validation.json').read_text())
assert v['passed'] and n['passed'] and fv['passed'] and fn['passed'] and not n['realProfileChanges'] and not fn['realProfileChanges']
assert '87 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8') and '299 checks,0 failures' in (NATIVE/'native.log').read_text(encoding='utf-8')
cup='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill east cup pickup/return candidates

## Objective and acceptance
Complete Bill's full master-consistent animation set,then full-set polish.
East cup pickup/reversed return joins selected idle to the new drinking hold.

## Accepted decisions and constraints
Selected matte idle owns identity; drinking frame000 owns held cup endpoint.
One near connected arm grips cup,far arm remains naturally down;two hands total.
Short empty reach precedes farther reach/grasp/inward draw;upright planted stance.
Equipped meals retain the installed reader,not drinking through a sealed helmet.

## Current state
Raw built-in exec-75c814d9-c88e-49e7-8875-5e4e0585ee84 and exact prompt retained
in sources/pickup-v1.png/prompt-pickup.txt. Six source figures all428px tall.
Five interiors1..5,exact selected idle/current drink hold donors at both ends.
One[.31,.3458] atlas ruler,density1.0,master neutral/skin/hair/burgundy grade,
front-boot/sole223 registration. Two bare states/14refs,seven580ms slots each;
60/80/100/100/100/80/60 timings and exact reverse return. Shared256plane,
pivot128,224/H148/dry0. Source/build/verify/registration/hash/preview retained.
No normal loader,registry,actor or gameplay changes. Assembled east meal family
references this package plus bowl transitions/eating/drinking without image copies.

## Verification
28package/87native PASS11.99s:raw/metadata/frame bindings,five interiors,finite
pacing/endpoint hold,exact idle/held joins,reverse poses and native148/82 board.
Interior headAxes all[130,76]; crown and fore-aft axes are identical in this source.
Full and game-size figures reviewed against selected idle/held cup; no obvious
extra hands,foot steps or chest-rooted arm. Fine insignia/detail and whole-family
material/proportion/pacing polish remain. All2,914owner non-log files unchanged
under scratch APPDATA. Candidate source/player only; actual counter/activity,
interruptions/restore and normal selection remain unproved.

## Next action
Normally install bill-meal-east-family-v1 for bare east activities with unchanged
6s eat/3s drink clocks;test actual counter contact,interruptions/disk restore.
Continue remaining cardinal meals,generic rest/dry death and full-set polish.
Inspection broader contact/hazard/equipped-drink-boundary audits remain open.
Goal active;no commit/export requested.
'''
family='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill east full bare meal candidate family

## Objective and acceptance
Complete Bill's full master-consistent animation set,then full-set polish.
Six-state east meal family assembled and native-loaded;normal integration pending.

## Accepted decisions and constraints
Four independent source parents retain generation/grade/ruler provenance.
Family references whole literal res paths;no duplicate image copies. Selected
idle/master matte/standing density and exact empty/held joins govern all parents.
580ms pickup/return,960ms eat/drink loops. Preserve6s eat/3s drink service clocks.
Helmet meals keep the reader; bare new meal gestures are east only at this stage.

## Current state
manifest.json six bare states/42refs ordered eat-enter/eat/eat-exit/drink-enter/
drink/drink-exit. Parent packages:bill-meal-entry-east-v1,bill-meal-east-coherent-v1,
bill-drink-entry-east-v1,bill-drink-east-coherent-v1. All use seven slots/shared
256plane/pivot128,224/H148/dry0. build.py/verification bind parent manifest/pixels.
index.html previews full meal at original6+3s duration beside selected idle.
No normal loader/ACTIVE_ASSETS/actor changes; old bare meals remain normally active.

## Verification
39assembled source/pacing/metadata/join checks and299native candidate checks
PASS11.72s. All42references load exact parent pixels;whole literal paths,standing
plane/dry metadata,finite timing/endpoint holds,loop repeats/closure,all five
adjacent joins,full idle closure and both whole-pose reversals verified.
Native82 six-row family board reviewed;parent148/82 boards separately reviewed.
Scratch APPDATA;2,914owner non-log files unchanged. Preview service duration is
presentation evidence only;actual activity counter/interruption/restore pending.
Bowl interior crown75–77/headX128–132 and fine suit/emblem/silhouette differences
remain for source/family/full-set polish. Exact endpoints do not prove interior
registration. Current boot anchoring should also be cross-checked independently
of the full silhouette when arms extend; no anchoring change made here.

## Next action
Install normal bare east family selection,then actual galley eat/drink phase
selection preserving original clocks,rewards,cleanup and snapshot behavior.
Prove normal loaded pixels/actual East counter contacts/interruption/disk restore.
Continue west/north/south meals,generic rest/dry death and full-set polish.
Inspection wider contact/hazard/equipped-drink-boundary audits remain open.
Full goal active; no commit/export requested.
'''
(P/'HANDOFF.md').write_text(cup,encoding='utf-8');(F/'HANDOFF.md').write_text(family,encoding='utf-8')
note='''
Bill east cup transitions/full meal candidate family — September30,2026.
Built-in cup source exec-75c814d9-c88e-49e7-8875-5e4e0585ee84/exact prompt retained.
Six428px figures;five interiors1..5 include short empty reach/full reach/grasp/
inward draw/low hold. Fixed[.31,.3458] ruler,density1.0,selected matte grade,
exact idle/drink-held donors. Two bare states/14refs,seven580ms slots/exact reverse.
All interior headAxes[130,76].28package/87native PASS11.99s;148/82 board reviewed.
Full east meal family assembled:sixstates/42refs,whole literal res paths,no copies.
39assembly/299native PASS11.72s;all parent pixels,pacing,finite endpoints,loop
repeat/closure,five adjacent joins,both reversals and full idle closure. Native82
family board reviewed;all2,914owner files intact in both scratch profile runs.
Lesson: specify short and farther empty reaches before grasp in the primary
source to avoid an abrupt initial pickup. Keep idle/held donors exact and review
all adjacent joins across actions,not just each isolated loop. Family preview's
6s eat/3s drink clocks are presentation only until actual consumer integration.
Fine detail/body/pose consistency remains for full-set polish; bowl headX128–132
and crown75–77 remain pending. No normal actor/loader/registry changes. Next
normal east meal install/actual counter/interruption/diskrestore,then remaining
cardinal meals/rest/drydeath/full polish. Inspection wider contact audits remain.
Full goal active. Handoffs:character/bill-drink-entry-east-v1/HANDOFF.md and
character/bill-meal-east-family-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill east full meal candidate family assembled — September30,2026\n'+note+'\n').encode()+status.read_bytes())
for root,report,counts,output,extra in [(P,n,{'package':28,'native':87},OUT,['source-rulers.json','registration.json','frame-hashes.json','verify.py','build_preview.py','contact-sheet.png']),(F,fn,{'package':39,'native':299},NATIVE,[])]:
    files=[root/name for name in ['build.py','manifest.json','verification.json','HANDOFF.md','index.html']+extra]+list((root/'sources').glob('*'))+[output/'validation.json',output/'loaded-water-carry.png']
    (root/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':counts,'native':report,'scope':'source/candidate native loading/finite joins only;normal meal service/contact/interruptions/restore/full polish pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded cup transitions/full east meal candidate assembly and normal integration next')
