"""Record paired source/player scope without silently installing candidate art."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-north-candidate-v1'
verification=json.loads((P/'verification.json').read_text());native=json.loads((O/'validation.json').read_text());log=(O/'native.log').read_text()
assert verification['checks']==58 and verification['failures']==0
assert native['passed'] and native['returnCode']==0 and '233 checks,0 failures' in log and 'ERROR:' not in log
index=R/'tests/index.json';data=json.loads(index.read_text())
group=data['subsystems'].setdefault('veld-seated',[])
if 'test_veld_seated_north_candidate' not in group:group.append('test_veld_seated_north_candidate')
data['lanes']['test_veld_seated_north_candidate']={'lane':'native','reason':'Candidate seated source/controller clocks and paired148/82 render; scratch APPDATA required.'}
index.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
archive=P/'revisions/bare-milestone-v1'
if not archive.exists():
    archive.mkdir(parents=True)
    for name in ['candidate-evidence.json','HANDOFF.md','index.html','browser-review.png']:
        if (P/name).exists():shutil.copy2(P/name,archive/name)
    (archive/'SCOPE.md').write_text('Historical bare milestone metadata and review. Bound files outside this revision can have changed; this is not a complete byte rollback. Original generated sources remain in sources/.\n')
bare=json.loads((P/'bare-manifest.json').read_text())['states'][0]['frameFiles']
helmet=json.loads((P/'helmet-manifest.json').read_text())['states'][0]['frameFiles']
html='''<meta charset="utf-8"><title>Veld north seated paired candidate</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:24px}img{object-fit:contain}a{color:#8cc6e7}.row{display:flex;gap:24px;align-items:end}</style>
<h1>Veld - north seated paired candidate</h1><p>Staged chair-height sitting from the selected rear master. Exact standing entries, one anatomical ruler and pooled material grade. Selected33x35 rear helmet stays at scale1, follows the collar, and preserves body pixels outside the fitted head region. 58 packaging and233 actual-player/controlled Veld checks pass, including interrupted reverse boundaries and paused player snapshots. Scratch native run clean; owner profile unchanged. Normal selection, lounge contact, world service-loss and Continue remain unproven.</p>
<p><button id="down">Sit down</button> <button id="rise">Rise</button> <button id="hold">Hold seated</button> <label>Frame <input id="slot" type="range" min="0" max="5" step="1" value="0"></label> <span id="status"></span></p>
<div class="row"><div>Selected bare master<br><img src="frames/bare/sit-down-north/000.png" width="256" height="256"></div><div>Bare candidate<br><img id="bare" width="256" height="256"></div><div>82px body scale<br><img id="bareSmall" width="142" height="142"></div></div>
<div class="row"><div>Selected helmet master<br><img src="frames/helmet/sit-down-north/000.png" width="256" height="256"></div><div>Helmet candidate<br><img id="helmet" width="256" height="256"></div><div>82px body scale<br><img id="helmetSmall" width="142" height="142"></div></div>
<p><a href="HANDOFF.md">Scope and remaining work</a> · <a href="../veld-seated-master-audit-v1/">Selected seated source audit</a></p>
<h2>Actual player at148 and82body scale</h2><img src="/output/veld-seated-north-candidate-v1/native.png" style="max-width:100%" alt="Paired native seated candidate poses">
<script>const tracks=TRACKS;const durations=[80,100,140,160,160,160];let order=[0,1,2,3,4,5],time=0,last=performance.now(),playing=true;const slider=document.querySelector('#slot');function render(slot){for(const gear of ['bare','helmet']){document.querySelector('#'+gear).src=tracks[gear][slot];document.querySelector('#'+gear+'Small').src=tracks[gear][slot];}slider.value=slot;document.querySelector('#status').textContent='Source pose '+slot+' / 5';}document.querySelector('#down').onclick=()=>{order=[0,1,2,3,4,5];time=0;playing=true};document.querySelector('#rise').onclick=()=>{order=[5,4,3,2,1,0];time=0;playing=true};document.querySelector('#hold').onclick=()=>{playing=false;render(5)};slider.oninput=()=>{playing=false;render(Number(slider.value))};function tick(now){if(playing){time+=(now-last)/3;let elapsed=Math.min(time,799.999),i=0;while(i<5&&elapsed>=durations[order[i]]){elapsed-=durations[order[i]];i++}render(order[i]);if(time>=800)playing=false;}last=now;requestAnimationFrame(tick)}render(0);requestAnimationFrame(tick);</script>'''.replace('TRACKS',json.dumps({'bare':bare,'helmet':helmet}))
(P/'index.html').write_text(html,encoding='utf-8')
note='''

## Veld north seated paired candidate — October 1, 2026

Selected33x35rear helmet stays at native scale1 and zero image-plane rotation
through north chair-height sitting. Manually tracked source collar landmarks
register each component; local18px head erasure stops at neck to preserve suit
collar. Exact equipped standing entry,800msfinite down/exact reverse rise/held
seat pair the bare candidate: six states/26refs/12exports. 58packaging checks
pass, including exact opaque canonical helmet hardware, protected body pixels,
source/master hashes, joints, timing and20deterministic files.

233actual-player/controlled Veld-class checks pass in31.02s, engine0/no errors,
native148/82board reviewed. All2931real non-log profile files unchanged under
scratch APPDATA. Candidate appended only in fixture; normal loader/ACTIVE_ASSETS
unchanged. Tests cover exact source pixels/metadata, role clocks, finite terminals,
paused player snapshot restore, actor snapshot admission and exact interrupted
sit/rise texture at eight phases including half-open boundaries. They do not
prove actual world service-loss, furniture seat/occlusion, fresh Continue or
natural cadence/held breathing. Full goal remains active/incomplete.

First fixture reached233checks but emitted held-pose cell-size errors: detached
grid had no main scene. Fixed fixture subclass supplies the384world ruler and
inherits production loader/source selection. A subsequent native launch exited1
before assertions, retained; clean check-only compile then corrected native run
passed. Original failed interval changed last_session.json; no attribution or
retroactive clean guard. Later clean interval proves only its own scope.

Lesson: finite actor clocks can avoid scene-bound renderer helpers while held
poses take their regular playback path. A controlled fixture must supply the
same world ruler for both; assertion count and engine return0 alone cannot
certify a clean run when script errors appear. Bound head fitting preserves
hardware scale and suit pixels but is not chair-contact or motion acceptance.
Next real lounge contact/seat depth, actual interruption/Continue, held breathing,
other directional seated/life sources and whole-set consistency polish.
Handoff: character/veld-seated-north-coherent-v1/HANDOFF.md.
'''
for relative in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    path=R/relative;old=path.read_bytes();encoded=note.lstrip().encode('utf-8')
    if encoded not in old:path.write_bytes(encoded+old if relative=='docs/CURRENT_STATUS.md' else old+note.encode('utf-8'))
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode('utf-8') not in installed.read_bytes():
    with installed.open('ab') as output:output.write(note.encode('utf-8'))
handoff='''# Project handoff

Updated: 2026-10-01 · Project: BrineSpace · Task: Veld north seated paired candidate

## Objective and acceptance
Full master-matched Veld set and whole-set polish remain active. Paired north
chair-height sitting staged; native source/controller clock proof complete,
furniture/world/owner motion acceptance unproven.

## Accepted decisions and constraints
Selected directional masters own scale, palette and equipment. Exact standing
entries; one148/505 body ruler and pooled semantic grade. Native rear33x35helmet,
collar-tracked scale1 fitting. Six paired states/26refs/12exports,800ms finite
lower/exact reverse rise/held seat. No normal selection, room layout or export edit.

## Current state
build_helmet.py, paired manifests/registration/board, expanded verify.py, new
test_veld_seated_north_candidate.gd/.uid and scratch runner. Browser syncs both
gears with their masters. Bare milestone metadata retained under revisions/;
not a full historical byte rollback. Pipeline/bible/skill/current status updated.

## Verification
58package/20deterministic files and233actual-player/controlled Veld checks pass.
Native148/82board reviewed;31.02s engine0/no errors, all2931real non-log files
unchanged under scratch APPDATA. Exact exported pixels/timing/reverse/held joins,
opaque native hardware and protected suit; eight interrupted clock boundaries,
paused player restore/actor admission. Failed detached-grid/script-error interval
and unexplained native early exit retained; fixed fixture384ruler, clean compile
and later clean native. No actual furnishing/service-loss/Continue acceptance.

## Next action
Actual lounge seat contact/occlusion/depth for both gears; actual service-loss,
fresh-scene Continue and cadence/held breathing. Then independently author other
cardinal seated/life sources, finish rest/death joins and full-set polish.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
paths=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='candidate-evidence.json']
paths.extend(p for p in O.iterdir() if p.is_file())
paths.extend([R/'tests/test_veld_seated_north_candidate.gd',R/'tests/test_veld_seated_north_candidate.gd.uid',R/'tools/run_veld_seated_north_candidate.py'])
paths.append(index)
evidence={'normalSelection':False,'packageChecks':58,'nativeChecks':233,'nativeRunner':native,'scope':'paired source/native player/controlled Veld clocks; no furniture/world service-loss/Continue/owner acceptance','files':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(P/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print(json.dumps({'boundFiles':len(paths),'packageChecks':58,'nativeChecks':233,'normalSelection':False}))
