from pathlib import Path
import json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[2]
e=json.loads((P/'world-review-evidence.json').read_text(encoding='utf-8'));assert e['validation']['passed'];assert len(e['boards'])==2
e['visualReview']='Both chronological native/source boards reviewed: last carry pose, four stop poses and arrival turn entry (12 pairs). Paired source board also reviewed. Whole source aliases retain registered identity, master helmet and material recipe. Continuous cadence, generic phase coverage and production safety remain unaccepted.'
(P/'world-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
v=e['validation']
block=f"""## Veld West phase-aware stop on actual workshop route — October 2, 2026

Staged character/veld-carry-west-start-master-v1/stop-route-v1 reuses whole
accepted carry2, start2, start1 and canonical held sources in both gears.
No raster/anatomy/helmet/grade changes. Four80ms finite source poses; simulation
remaps first240ms to remaining real waypoint distance and holds final80ms.
Read existing player.phase through frame_at_elapsed: sampling frame() here
mutated gait with a different coordinate input and broke admission. Failed
v1 harness parse and v2 no-stop intervals retained with their exact sources.
Arrival retains consumed real waypoint through planted hold; no invented route.

Build20checks0. Actual main/default workshop normal vs staged {v['seconds']}s,
{v['targetedInputCount']} targeted inputs unchanged; all {v['realProfileFileCount']} owner non-log files unchanged
with scratch APPDATA. v3 native fixture passed; both gears four stop poses,
nonincreasing travel speed, real endpoint, final hold and exact stop/turn body
join checked. Two6pair native/source boards and paired source board reviewed.
No normal controller/selection changes. Phase2 default-route scope only; full
continuous cadence, other phases, traffic/interruption/needs/service/medium/gear/
death/Continue still pending. Parent arrival hold skips normal update and uses
visual clock; this authoring preview is not production adoption.

Next: generic phase-aware stops and cardinal starts, guarded integrated clocks,
North idle/case lifecycle/South matching/furniture/swimming and full-library
master consistency/polish. Full goal active/incomplete. Handoff in stop-route-v1.

"""
for p in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 st=p.stat();tmp=p.with_name(p.name+'.veld-west-stop.tmp')
 with tmp.open('wb') as dst,p.open('rb') as src:dst.write(block.encode('utf-8'));shutil.copyfileobj(src,dst,1024*1024)
 assert p.stat().st_size==st.st_size and p.stat().st_mtime_ns==st.st_mtime_ns,'Concurrent reference update; preserve both versions'
 for attempt in range(5):
  try:os.replace(tmp,p);break
  except PermissionError:
   if attempt==4:raise
   time.sleep(.2)
(P/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October 2, 2026 · Project: BrineSpace · Task: Veld West stop\n\n## Objective and acceptance\nFull master-matched Veld animation set and cross-library polish; active/incomplete.\n\n## Accepted decisions and constraints\nWhole accepted source aliases, original helmet/materials, unchanged real route, scratch profile.\n\n## Current state\nChild build/manifests/APNGs, fixture-only actor stop subclass, source/world review, new test+UID and runner. No normal adoption.\n\n## Verification\n'+block+'## Next action\nGeneric gait phase admission, guarded simulation controller clocks and interruption/Continue integration; remaining full library and polish.\n',encoding='utf-8')
(P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Veld West stop review</title><style>body{background:#202a30;color:#eee;font:18px sans-serif;margin:30px}img{max-width:100%}</style><h1>Veld West stopping</h1><p>Whole master sources; actual workshop stop and arrival joins. Staged preview.</p><h2>Bare</h2><img src="bare-stop-phase2-west.apng"><h2>Helmet</h2><img src="helmet-stop-phase2-west.apng"><h2>Sources</h2><img src="paired-stop-source-review.png"><h2>Actual workshop — bare</h2><img src="bare-stop-world-review.png"><h2>Actual workshop — helmet</h2><img src="helmet-stop-world-review.png">',encoding='utf-8')
print('Recorded scoped stop milestone in five references and handoff')
