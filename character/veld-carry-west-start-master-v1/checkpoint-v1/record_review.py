from pathlib import Path
import json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[2]
C=R/'output/veld-workshop-motion-checkpoints-v2';O=R/'output/veld-workshop-motion-restore-v2'
cap=json.loads((C/'validation.json').read_text(encoding='utf-8'));e=json.loads((P/'restore-review-evidence.json').read_text(encoding='utf-8'));assert cap['passed'] and e['validation']['passed']
report=json.loads((O/'restore-review.json').read_text(encoding='utf-8'));assert len(report['results'])==10
assert sum(x['comparisonTicks'] for x in report['results'])==600
e['visualReview']='Ten restored native/source comparisons against uninterrupted original route reviewed on two5row boards; full restored helmet stop native viewed. Exact pixels/proportions/helmet/material unchanged. No full continuous cadence or normal freshContinue acceptance.'
(P/'restore-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
block=f"""## Veld staged cargo checkpoint continuity — October 2, 2026

New character/veld-carry-west-start-master-v1/checkpoint-v1 extends the staged
simulation-clock controller. Actor snapshots retain held/start/phase2stop/turn
elapsed clocks, finite duration, gear, goal/cell, route endpoint and arrival flag.
Loaded artwork admission binds the full following master family: heldEast/West,
EWturn, Weststart/stop/carry, WNturn, Northunload/idle, including pixels, dimensions,
pivot/148height/depth/water metadata, timing and carry stride. No raster changes.
Structural/source admission precedes mutation; normal base restore rebuilds current
geometry, clearing private motion when its route/floor no longer survives. Legacy
base checkpoint clears private motion. Normal RunSave and selection remain unchanged.

Actual route captures ten binary checkpoints, five contexts per gear. Capturev2
5775checks0/{cap['seconds']}s/238inputs unchanged; earlier active-clip-only binding
v1 passed but was strengthened because following clips could otherwise change.
Fresh second engine process restores10actors and compares exact first saved pixels,
foot/clocks plus600subsequent60Hz ticks against uninterrupted captured observations.
Restorev2 {report['checks']}checks0/{e['validation']['seconds']}s/249inputs unchanged.
Malformed clock/endpoint/gear/binding/duration/missing-key and changed loaded frame,
timing/missing clip/following action reject; rebuilt invalid floor clears motion,
valid reload succeeds, legacy fields do not retain stale private pose. Both runs
scratchAPPDATA/all2931owner non-log files unchanged. Two5row original/restored/source
boards and full restored helmet stop native reviewed. Whole existing master identity,
registration, shell and grade retained; not new source or continuous cadence proof.

No normal freshContinue/menu/RunSave acceptance, floor-case ownership/lifetime,
real traffic/fire/flood coverage or normal adoption. Next integrate the validated
contract with guarded production selectors/RunSave and real interruption fixtures;
finish other gait phases/cardinalstarts, North fullidle/South masters/furniture/
swimming and whole-library master consistency/polish. Full goal active/incomplete.
Lesson: bind upcoming transitions as well as the displayed clip; checkpoint style
consistency includes timing, registration and stride, not only current image bytes.
Handoff: character/veld-carry-west-start-master-v1/checkpoint-v1/HANDOFF.md.

"""
for p in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 st=p.stat();tmp=p.with_name(p.name+'.veld-checkpoint.tmp')
 with tmp.open('wb') as dst,p.open('rb') as src:dst.write(block.encode('utf-8'));shutil.copyfileobj(src,dst,1024*1024)
 assert p.stat().st_size==st.st_size and p.stat().st_mtime_ns==st.st_mtime_ns,'Concurrent reference update'
 for attempt in range(5):
  try:os.replace(tmp,p);break
  except PermissionError:
   if attempt==4:raise
   time.sleep(.2)
(P/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October 2, 2026 · Project: BrineSpace · Task: Veld cargo checkpoint continuity\n\n## Objective and acceptance\nFull Veld master-matched set, then cross-library consistency/polish. Active/incomplete.\n\n## Accepted decisions and constraints\nWhole unchanged master art, canonical registration/helmet/grade, real route, ordinary update priorities and scratch profile.\n\n## Current state\nStaged checkpoint subclass+UID, capture/restore tests+UIDs and runners, ten real binary checkpoints and comparison boards. Normal controller/RunSave selection unchanged.\n\n## Verification\n'+block+'## Next action\nGuarded normal integration and fresh menu Continue, real traffic/fire/flood, case lifetime/checkpoint ownership; remaining cardinal sources and full-library polish.\n',encoding='utf-8')
(P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Veld checkpoint continuity</title><style>body{background:#202a30;color:#eee;font:18px sans-serif;margin:30px}img{max-width:100%}</style><h1>Veld checkpoint continuity</h1><p>Original route, freshly restored pose and exact master source. Five carrying contexts in each version. Staged restoration.</p><h2>Bare</h2><img src="bare-checkpoint-review.png"><h2>Helmet</h2><img src="helmet-checkpoint-review.png">',encoding='utf-8')
print('Recorded full-family staged checkpoint milestone in five references and handoff')
