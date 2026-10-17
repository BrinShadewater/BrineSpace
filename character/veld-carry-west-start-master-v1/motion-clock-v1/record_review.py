from pathlib import Path
import json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[2]
e=json.loads((P/'world-review-evidence.json').read_text(encoding='utf-8'));assert e['validation']['passed'];assert sum(x['pairs'] for x in e['boards'])==52
e['visualReview']='Both26pair chronological native/source boards reviewed (52pairs): all East-West half-turn, West start/stop and West-North arrival poses. Original whole master sources and shell/grade remain unchanged. Not continuous travel cadence or new source acceptance.'
(P/'world-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
block="""## Veld cargo transitions use simulation clocks without skipping normal updates — October 2, 2026

Staged character/veld-carry-west-start-master-v1/motion-clock-v1 extends VeldNpc
 directly, replacing the older authoring arrival early-return. East-West and
West-North planted turns, West firststep and phase2 stopping use simulation delta.
Grid action_elapsed selects the exact whole master clip; no frame() side-effect
sampling, new raster, proportion/helmet/grade or normal selection changes.
A consumed real endpoint remains through final stop/arrival hold so inherited
update continues needs, service and safety priority. Start/stop clocks freeze
on blocked attempted travel; full traffic behavior remains to be proven.

Actual main/default workshop fixture5763checks0/104.22s,237targeted inputs unchanged;
all2931owner non-log files unchanged under scratchAPPDATA. Both gears complete
master route, source joins and independent-case departure. Display clock6x,
turn duration follows60Hz simulation; zero delta preserves turn/foot; hunger
advances throughout arrival. Reconstructed actual endpoint service-loss cancels
stale turn through normal controller; gear/medium/death invalidate private pose.
Two26pair native/source boards reviewed,52pairs. These guards are scoped tests,
not full fire/flood/traffic/naturalchooser/checkpoint/freshContinue acceptance.

No normal adoption; new private motion has no checkpoint serialization yet.
Next: guarded checkpoint restoration and real interruption/traffic fixtures,
generic phases/cardinalstarts, North fullidle/case lifetime/South masters,
furniture/swimming and full cross-library consistency/polish. Full goal active.
Lesson: retain normal update priorities during finite visual holds; bind clocks
 to simulation progress and use action_elapsed for authored turns. A passing
paused/needs/service probe does not certify every priority or lifecycle path.
Handoff: character/veld-carry-west-start-master-v1/motion-clock-v1/HANDOFF.md.

"""
for p in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 st=p.stat();tmp=p.with_name(p.name+'.veld-motion-clock.tmp')
 with tmp.open('wb') as dst,p.open('rb') as src:dst.write(block.encode('utf-8'));shutil.copyfileobj(src,dst,1024*1024)
 assert p.stat().st_size==st.st_size and p.stat().st_mtime_ns==st.st_mtime_ns,'Concurrent reference update'
 for attempt in range(5):
  try:os.replace(tmp,p);break
  except PermissionError:
   if attempt==4:raise
   time.sleep(.2)
(P/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October 2, 2026 · Project: BrineSpace · Task: Veld cargo simulation clocks\n\n## Objective and acceptance\nFull master-matched Veld animation set, followed by cross-library polish. Active/incomplete.\n\n## Accepted decisions and constraints\nWhole original staged master sources and unchanged helmets/grade, real room route, normal update priorities, scratch saves.\n\n## Current state\nNew staged direct VeldNpc subclass, actual-route test+UID/runner, native-source boards and review evidence. No normal adoption.\n\n## Verification\n'+block+'## Next action\nCheckpoint serialization/guarded restoration; real fire/flood/traffic and interruption paths; other starts/stops and remaining full visual library.\n',encoding='utf-8')
(P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Veld carrying transitions</title><style>body{background:#202a30;color:#eee;font:18px sans-serif;margin:30px}img{max-width:100%}</style><h1>Veld carrying transitions</h1><p>Simulation-clocked turns, first step and stop. Recorded workshop poses alongside their unchanged master sources. Staged controller.</p><h2>Bare</h2><img src="bare-stop-world-review.png"><h2>Helmet</h2><img src="helmet-stop-world-review.png">',encoding='utf-8')
print('Recorded simulation-clock milestone in five references and handoff')
