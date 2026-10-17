from pathlib import Path
import json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1]
native=json.loads((R/'output/veld-carry-west-start-master-v2/validation.json').read_text(encoding='utf-8'));world=json.loads((P/'world-review-evidence.json').read_text(encoding='utf-8'));assert native['passed'] and world['validation']['passed']
world['visualReview']='Both9pair native/source boards reviewed: actual turn terminal,4start poses,3firstcarry poses and arrival turn entry,18pairs. Progressive first step/held case remains coherent; material/grip/foot contact and continuous cadence remain polish. Stop not coordinated in controller.'
(P/'world-review-evidence.json').write_text(json.dumps(world,indent=2)+'\n',encoding='utf-8')
for n in ['registration.json','execution-start-v1.json','native-review-evidence.json']:
 d=json.loads((P/n).read_text(encoding='utf-8'));d['visualReview']='Raw4pose source and8paired exports reviewed against exact West held/gait0 and original master. All48standalone native/source pairs reviewed in4boards, plus full helmet-stop0native. Correct West asymmetric device retained; wholebody continuity improves first step, material/head/grip/foot cadence remains scoped polish.'
 (P/n).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
block='''## Veld West first carrying step on the actual workshop route — October 2, 2026

Actual default workshop carries WEST immediately after East pickup/half-turn;
East start source is valid coverage but does not fix this route. New staged
veld-carry-west-start-master-v1 has whole authored West intermediates, correct
near hip teal device, exact master turn-held and West carry0 endpoints. Builtin
44cfbd36-4ed4-4024-8209-e5732727ebdf raw/prompt/refhashes retained, no mirror.
One148standing ruler .22255639097744362, whole body head-axis134/boot floor224
translation, natural leg swing and unchanged original44x46West shell. Shared
material recipe and protected case/grip; bounded head fitting/body outside exact.
Four80ms poses320msfinite start and reversed stop; original6pose840carry unchanged.
52buildchecks0; standalone317checks0/48native samples5.87s/41inputs stable, all48
pairs seen/decoded exact. Initial harness stale East key failed, process stopped
after confirmed script error, exact sources/failed interval retained; v2 passes.
Fourfinite browser completions and paused helmet firststep seen/saved.

Authoring-only subclass adds simulation-delta-clocked West firststep after planted
turn, holds initial80ms physically stationary then ramps speed over240ms. Exact
terminal source joins distance gait0 with fresh phase. Actual main-scene/default
workshop normal vs staged5289checks0/100.9s/233inputs stable; both gears4poses seen,
20firststep records and5.3718maximum world-unit travel. Both native/source boards
18pairs reviewed, not wholecontinuous cadence. ScratchAPPDATA/all2931owner files
unchanged. No normal selections/controller/room edits; stop source not coordinated.

Remaining: phase-aware actual stopping, East/cardinal starts and new North/South
coverage, material/grip/foot-contact/full cadence polish, full North idle, case
ownership/checkpoint and guarded needs/safety/service/medium/gear/death/Continue.
Authoring arrival hold still skips ordinary update; start clock alone does not
certify traffic/interruption handling. Furniture/swimming/full-library consistency
remain; full goal active. Lesson: inspect the actual route before choosing direction;
do not invent an East waypoint to exercise an East-only repair. New start is clocked
by simulation delta; planted older turns still use authoring visual clock.
Handoff: character/veld-carry-west-start-master-v1/HANDOFF.md.

'''
for p in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 st=p.stat();tmp=p.with_name(p.name+'.veld-west-start.tmp')
 with tmp.open('wb') as dst,p.open('rb') as src:dst.write(block.encode('utf-8'));shutil.copyfileobj(src,dst,1024*1024)
 now=p.stat();assert (st.st_size,st.st_mtime_ns)==(now.st_size,now.st_mtime_ns)
 for attempt in range(5):
  try:os.replace(tmp,p);break
  except PermissionError:
   if attempt==4:raise
   time.sleep(.2)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld West firststep route

## Objective and acceptance
Full Veld master-matched animation library and cross-library consistency/polish.
Active/incomplete; scoped staged West firststep sources and route progression.

## Accepted decisions and constraints
Original West identity/asymmetric device, whole authored body, one148ruler,
exact held/gait0 endpoints and unchanged carry. Original shell unchanged. No
mirror/anatomy strips. Scratch APPDATA, owner saves/concurrent work preserved.

## Current state
This folder: raw4pose source/prompt/execution/refhashes, build/registration/paired
start-stop manifests/APNGs, native/world/browser evidence, fixture-only actor
subclass. Two new tests+UIDs and runners. Route uses West, not new East start.
No normal adoption/controller/room changes. Stop source remains uncoordinated.

## Verification
52build0;317standalone0/48samples5.87s/all48pairs seen +fullhelmetstop0.5289world0/
100.9s/233inputs stable;18native/source pairs seen. All4start poses,80msplanted,
speed ramp/max5.3718world travel and exact actual distance-gait0 join checked.
41standaloneinputs stable; scratchAPPDATA/2931owner files unchanged. First failed
standalone interval preserved with exact sources. Browser4finite completions,
helmetfirststep seen/saved. Not full continuous cadence/safety/checkpoint evidence.

## Next action
Actual phase-aware stop before arrival turn, preserve route and correct finite
simulation clock/traffic handling. Guard controller interruptions/needs/service/
medium/gear/death/fresh Continue before normal adoption. Other cardinal starts,
North fullidle/case lifecycle/South masters/furniture/swimming/full-library polish
remain. Parent arrival hold still skips normal update; do not infer safety pass.
''',encoding='utf-8')
print('Recorded West firststep source and route milestone in five maintained references.')
