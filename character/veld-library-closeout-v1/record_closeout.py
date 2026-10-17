from pathlib import Path
import json,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'turn-body-fix'
report=json.loads((R/'output/veld-turn-body-consistency-v1/validation.json').read_bytes());assert report['passed']
build=json.loads((D/'BUILD_REVIEW.json').read_bytes())
groups={}
for row in build['rows']:groups.setdefault(row['state'],[]).append(row)
durations={s['id']:s['frameDurationsMs'] for f in ['quarter','half'] for s in json.loads((D/f'{f}-helmet-manifest.json').read_bytes())['states']}
items=[dict(state=s,durations=durations[s],rows=rows) for s,rows in groups.items()]
html='''<!doctype html><meta charset="utf-8"><title>Veld — selected turn consistency</title>
<style>body{margin:32px;background:#182329;color:#e3e6e6;font:16px system-ui}h1{font-size:28px}p{max-width:950px;line-height:1.5}button{padding:8px 20px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,720px),1fr));gap:24px}article{background:#202c32;padding:18px}section{display:flex}figure{margin:0;flex:1;min-width:0;text-align:center}img{width:100%;max-width:256px;image-rendering:pixelated}figcaption{color:#adbdc5}small{display:block;color:#adbdc5}</style>
<h1>Veld — selected turn consistency</h1><p>12 helmet turn states now use the same body frames as their bare versions. Existing helmet artwork, poses and timing are preserved. This pass is installed and checked in Godot; the rest of the library still needs master matching and transition review.</p><p><button id="pause">Pause</button> <label>Speed <select id="speed"><option value="1">Normal</option><option value="0.5">Half speed</option><option value="0.25">Quarter speed</option></select></label></p><main></main>
<script>const items=DATA;let playing=true,last=0,clock=0;const main=document.querySelector('main');for(const item of items){const card=document.createElement('article');card.innerHTML='<h2>'+item.state.replace('carry-turn-','').replaceAll('-',' → ')+'</h2><section>'+['Selected bare','Before helmet','Matched helmet'].map(label=>'<figure><img alt="'+label+'"><figcaption>'+label+'</figcaption></figure>').join('')+'</section><small></small>';main.append(card);item.images=[...card.querySelectorAll('img')];item.note=card.querySelector('small');}
document.querySelector('#pause').onclick=()=>{playing=!playing;document.querySelector('#pause').textContent=playing?'Pause':'Play'};
function tick(t){if(last&&playing)clock+=(t-last)*Number(document.querySelector('#speed').value);last=t;for(const item of items){const duration=item.durations.reduce((a,b)=>a+b,0);let pos=clock%(duration+500),i=0;while(i<item.rows.length-1&&pos>=item.durations[i]){pos-=item.durations[i];i++}const row=item.rows[i];['bare','oldHelmet','output'].forEach((key,j)=>{const src='/'+row[key];if(item.images[j].getAttribute('src')!==src)item.images[j].src=src});item.note.textContent='Frame '+(i+1)+' / '+item.rows.length+' · '+duration+' ms turn + preview end hold';}requestAnimationFrame(tick)}requestAnimationFrame(tick);</script>'''
(D/'index.html').write_text(html.replace('DATA',json.dumps(items)),encoding='utf-8')
handoff='''# Project handoff

Updated: October 3, 2026 · Project: Brine Space · Task: Veld library closeout

## Objective and acceptance
Finish the existing selected Veld library against original masters. Coverage alone is not acceptance; character identity, materials, motion, contacts and runtime transitions must match.

## Accepted decisions and constraints
Owner accepted closeout of existing work. Preserve feet-together planted turns, exact authored timing and whole poses. Reuse complete existing helmet equipment without local recolouring or anatomy edits. Do not continue speculative scanner studies as the main objective.

## Current state
Fresh initial inventory: 198 bare / 192 helmet states, 118 manifests, 4804 unique sources, no missing files. Six unpaired states are bare-only helmet fitting/removal and welding. Frozen initial inventory and boundary boards are in this folder.
Installed quarter/half helmet turn manifests under turn-body-fix through scripts/grid_canvas.gd and character/ACTIVE_ASSETS.json. All 96 slots in 12 states now use the selected bare body outside the existing equipment rectangle; complete existing helmet/collar bytes inside it are unchanged. No body pose, pivot, scale or timing changes. Carry-north and all other selections remain unchanged.

## Verification
216 build checks passed. All 12 source before/after boards and both native contact sheets inspected. Normal Godot loader: 567 checks passed across all 96 slots and 24 bare/helmet turn dispatches/exits. Scratch APPDATA; all 2931 owner nonlog files and 393 targeted inputs unchanged. Test report: output/veld-turn-body-consistency-v1/validation.json. Browser comparison is a review aid, not full native continuous-motion/lifecycle acceptance.

## Next action
Compare selected West/North/South interaction and repair families to original masters; address the demonstrated whole-body softness/cooler grade. Then cargo master fidelity and walk/planted transitions, furniture contacts/dispatch, remaining idle/walk/water/death consistency and native controller/new-process Continue checks. Scanner studies remain staged, unfinished. Full animation goal remains active and incomplete.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
(P/'CLOSEOUT.md').write_text('''# Veld finite closeout list

- [x] Freeze actual selected library inventory and inspect turn boundaries.
- [x] Correct body differences between selected bare/helmet turns: 12 states / 96 slots.
- [x] Install and verify normal runtime turn selection, timing and return to carrying.
- [ ] Match interaction/repair directions to original master identity, detail and materials.
- [ ] Resolve cargo master fidelity and walk/planted transitions while preserving approved feet-together turns.
- [ ] Review furniture finish, contact and actual dispatch.
- [ ] Finish idle/walk/water/death consistency; resolve North quiet idle.
- [ ] Verify full controller lifecycle and new-process Continue; obtain final full-library visual acceptance.

198/192 states is broad coverage, not a percentage complete. No full-set completion claim.
''',encoding='utf-8')
title='## Veld existing-library closeout and installed turn body consistency — October 3, 2026'
note=title+'''

Owner accepted switching focus to finishing the existing selected library, rather
than accumulating scanner studies. Fresh normal-loader inventory: 198 bare/192
helmet states, 118 manifests, 4804 unique selected sources, zero missing files.
Coverage is not original-master visual acceptance.

Confirmed all96 selected helmet turn slots differed from their bare bodies outside
the registered equipment region. Installed12 quarter/half turn states using whole
selected bare poses and complete existing helmet/collar plate (96,65)-(169,109).
Body outside region is exact bare art; equipment region exact previous helmet art.
No local grade/anatomy/scale/pivot/pose/timing changes. Carry-north unchanged.
Only two loader paths and their registry entries changed. 216 buildchecks0;
all12 before/after boards and2 native sheets inspected. Normal installed Godot
loader567checks0: all96 slots, metadata/timing,24 bare/helmet dispatches/exits.
Scratch APPDATA,2931 owner nonlog files and393 targetedinputs unchanged.

Lesson: validate bare/equipment body consistency using the actual final override,
not just master helmet registration. Do not force planted turn endpoints to match
walking carry framezero: their feet-together stance is an accepted owner choice.
This fix preserves existing helmet design; it does not solve remaining bare-body
master drift or establish full continuous native/play/save acceptance.

Next: selected directional interaction/repair master matching, cargo joins/materials,
furniture contacts/dispatch, idle/walk/water/death and final native lifecycle.
Scanner studies remain staged/unfinished. Full goal active/incomplete.
Handoff: character/veld-library-closeout-v1/HANDOFF.md.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(20):
  with path.open('r',encoding='utf-8') as f:head=''.join(next(f,'') for _ in range(120))
  if title in head:break
  before=path.stat();tmp=path.with_name(path.name+'.veld-'+uuid.uuid4().hex+'.tmp')
  with tmp.open('wb') as dest,path.open('rb') as source:dest.write(note.encode('utf-8'));shutil.copyfileobj(source,dest,1024*1024)
  after=path.stat()
  if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):tmp.unlink();time.sleep(.5);continue
  try:tmp.replace(path)
  except PermissionError:tmp.unlink();time.sleep(.5);continue
  print(path.name,'updated');break
 else:raise RuntimeError('Concurrent updates prevented guarded prepend: '+str(path))
