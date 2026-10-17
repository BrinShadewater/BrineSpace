from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
proof=json.loads((P/'verification.json').read_text());assert proof['checks']==30 and proof['failures']==0
manifest=json.loads((P/'bare-manifest.json').read_text());files=manifest['states'][0]['frameFiles']
html='''<meta charset="utf-8"><title>Veld north seated candidate</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:24px}img{object-fit:contain}a{color:#8cc6e7}.row{display:flex;gap:24px;align-items:end}</style>
<h1>Veld - north seated candidate</h1><p>Staged bare source: connected chair-height sitting from the selected rear master. Exact standing entry, six authored positions at one anatomical ruler, pooled matte material grade, reversed rise and held seated endpoint. 30 packaging checks pass. Equipment fitting, actual-player cadence, chair contact and saved interruptions remain; runtime selection is unchanged.</p>
<p><button id="down">Sit down</button> <button id="rise">Rise</button> <button id="hold">Hold seated</button> <label>Frame <input id="slot" type="range" min="0" max="5" step="1" value="0"></label> <span id="status"></span></p>
<div class="row"><div>Selected master<br><img src="frames/bare/sit-down-north/000.png" width="256" height="256"></div><div>Candidate<br><img id="candidate" width="256" height="256"></div><div>82px standing body scale<br><img id="small" width="142" height="142"></div></div>
<p><a href="HANDOFF.md">Scope and remaining work</a> · <a href="../veld-seated-master-audit-v1/">Selected seated source audit</a></p><img src="bare-contact-sheet.png" style="max-width:100%" alt="Candidate poses beside selected master at148 and82body scale">
<script>const files=FILES;const durations=[80,100,140,160,160,160];let order=[0,1,2,3,4,5],time=0,last=performance.now(),playing=true;const slider=document.querySelector('#slot');function render(slot){document.querySelector('#candidate').src=files[slot];document.querySelector('#small').src=files[slot];slider.value=slot;document.querySelector('#status').textContent='Source pose '+slot+' / 5';}document.querySelector('#down').onclick=()=>{order=[0,1,2,3,4,5];time=0;playing=true};document.querySelector('#rise').onclick=()=>{order=[5,4,3,2,1,0];time=0;playing=true};document.querySelector('#hold').onclick=()=>{playing=false;render(5)};slider.oninput=()=>{playing=false;render(Number(slider.value))};function tick(now){if(playing){time+=(now-last)/3;let elapsed=Math.min(time,799.999),i=0;while(i<5&&elapsed>=durations[order[i]]){elapsed-=durations[order[i]];i++}render(order[i]);if(time>=800)playing=false;}last=now;requestAnimationFrame(tick)}render(0);requestAnimationFrame(tick);</script>'''.replace('FILES',json.dumps(files))
(P/'index.html').write_text(html,encoding='utf-8')
handoff='''# Project handoff

Updated: 2026-10-01 · Project: BrineSpace · Task: Veld north seated source

## Objective and acceptance
Full master-matched Veld animation set and cross-animation polish remain active.
North bare chair-height sitting is staged, not normally selected or accepted.

## Accepted decisions and constraints
Selected rear idle owns anatomy, material, scale and handed equipment. Preserve
the exact standing endpoint. Chair-height sitting is distinct from floor rest.
Do not normalise individual pose height. No owner-layout, gameplay or export edit.

## Current state
Seated master audit binds32state rows/128frames, eight bare/helmet directional
sequences. Old seated sources drift in face/build/suit; equipped rows retain
retired hardware. Independent north six-pose source exec13863aad-88c3-42e9-ad58-831fcd78f721
uses current rear master. Flask badge rejected. Badge edit exec46f46718-fd10-4141-9a2f-2bd63b35fadb
restores boxed construction but changes wider source pixels; preserve both sources
and treat v2 as a new complete revision. One148/505 ruler, grounded256/p128,224,
pooled spatial rear ear/brown hair/science/neutral grade applied once. Exact idle
entry,800ms finite down, exact reverse rise, single held seated endpoint: three
bare states/13refs/six exports. Bare held breathing remains polish work.

## Verification
30 packaging checks pass: source/master hashes, exact standing pixels, reverse/
held joins,800ms, opaque floor222-224 and11deterministic files. Ungraded geometry
and graded148/82boards visually reviewed. PNG LFS filter verified. No Godot run,
native player, source-motion/furniture acceptance or real profile claim this turn.
Initial grade failed because hair and skin aliased one NumPy mask; independent
copies fixed it before export. Material masks still require visual polish.

## Next action
Fit selected native rear helmet at tracked neck landmarks, preserving collar and
body. Exercise all three clips and interruption boundaries in actual player,
then real lounge seat contact/cadence/save/Continue. Author other directional
seated/life sources and continue rest/death joins plus full-set polish.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''

## Veld seated audit and north bare candidate — October 1, 2026

Fixed H148/pivot source audit covers32selected idle/down/held/rise rows and128
distinct images across four directions/two gears. Sitting changes face/build,
suit/grade/harness; helmet rows retain retired gold hardware. Independent north
chair-height sitting source exec13863aad-88c3-42e9-ad58-831fcd78f721 follows rear
master and handed tools. Flask badges rejected; authored badge revision
exec46f46718-fd10-4141-9a2f-2bd63b35fadb restores boxed marks but changes wider
pixels, so retain it as a new complete source rather than claim a local pixel
repair. One148/505 anatomical ruler; pooled spatial rear-ear/brown-hair/science/
neutral grade before resampling,256/p128,224/H148. Exact standing entry,800ms
finite sit-down/exact reverse rise/held seat: three bare states/13refs/six exports.
30package checks and11deterministic files pass; graded148/82and raw boards viewed.
Staged only: no selection/native/player/furniture/interrupt/Continue acceptance.
No Godot or owner-profile interval this turn. Initial aliased hair/skin mask
assertion corrected with independent NumPy mask copies before packaging.

Lesson: distinguish chair-height sitting from floor-rest geometry and follow the
direction's master through all interior poses. A badge-only generation request
does not prove protected pixels: inspect changes and retain a complete revision
when they extend outside the requested region. Recalibrate from that revision,
apply one material grade and bind original/edit prompts and sources. Static
seated hold is source coverage, not completed natural breathing/cadence polish.
Next native rear helmet/three-role player proof, lounge contact/interruption/
Continue, other seated/life directions and full-set consistency. Full goal active.
Handoff: character/veld-seated-north-coherent-v1/HANDOFF.md.
'''
for relative in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    path=R/relative;old=path.read_bytes();encoded=note.lstrip().encode('utf-8')
    if encoded not in old:path.write_bytes(encoded+old if relative=='docs/CURRENT_STATUS.md' else old+note.encode('utf-8'))
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode('utf-8') not in installed.read_bytes():
    with installed.open('ab') as output:output.write(note.encode('utf-8'))
paths=[path for path in P.rglob('*') if path.is_file() and '__pycache__' not in path.parts and path.name!='candidate-evidence.json']
paths.extend(path for path in (R/'character/veld-seated-master-audit-v1').iterdir() if path.is_file())
evidence={'normalSelection':False,'packageChecks':30,'nativeChecks':None,'scope':'source/material/geometry/pixel/packaging audit; actual player and furniture distinct','files':{path.relative_to(R).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}}
(P/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print(json.dumps({'boundFiles':len(paths),'packageChecks':30,'normalSelection':False}))
