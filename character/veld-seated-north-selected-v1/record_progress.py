from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-north-selected-v1'
validation=json.loads((O/'validation.json').read_text(encoding='utf-8'))
assert validation['passed']
log=(O/'native.log').read_text(encoding='utf-8')
match=re.search(r'VELD NORTH SELECTED: (\d+) checks,(\d+) failures; (\d+) fresh restores',log);assert match
checks,failures,restores=map(int,match.groups());assert failures==0 and restores==8
review=json.loads((P/'room-crop-review.json').read_text(encoding='utf-8'))
equal=sum(d['roomCropEqual'] for d in review['comparisons'])
delta=max(d['maximumChannelDelta'] for d in review['comparisons'])
title='Veld selected North seated/breathing family - October 1, 2026'
note=f'''## {title}

Normal grid loader and ACTIVE_ASSETS now select veld-seated-north-selected-v1
paired composition: exact tested North down/rise and six-phase held breathing,
three states/18refs per gear, six states/36refs/24source PNGs total. Whole literal
res paths, fixed256/p128224/H148 and original directional matte head/helmet/body
pixels; no duplicated/regraded/resized source.77composition checks0failures,
three deterministic files,28immutable source bindings. Existing candidate source
status retained; wrapper installed locally, owner motion acceptance open.

Actual normal-loader main/loungeseat lifecycle:{checks}checks0failures,
{validation['seconds']}s engine0/no errors. Eight real disk writes/reads/fresh-scene
staged Continue at interior/second-cycle held elapsed.8/1.4/2.2/4.6s,both gears;
no fixture artwork injected. Each fresh normal loader independently compared
all six states/36source slots with composed authority and calibration/depth marker.
Exact displayed source/action/gear/timer/physical foot/furniture contact/depth
and paused clock restored.16actual power/suspend service guards dispatch rise,
only bounded local breath relaxes to exact neutral; head/helmet/body supports
protected. Actual lowering->held->rise timers have exact neutral joins.
All{validation['realProfileFileCount']}owner non-log files unchanged/scratch APPDATA.
Watched dependencies/source hashes stable across this interval.

Eight unmodified before/after room-crop pairs reviewed;{equal}/8byte equal,
maximum channel delta{delta}/255. Exact source/contact/depth assertions are
separate from whole-room shade; no blanket equality claim beyond measured crops.
Native real lounge occupant remains visibly seated with fixed scale/contact;
browser source loop/contact board reviewed separately. First2.41sec fixture
parse failed on mixed indentation; fixed new test only, retained archive.
Prior four-rotation/natural-approach candidate proofs remain dated; this normal
selected interval prescribes one actual clear chair and tests two power/suspend
guards, not natural chooser/all rotations/hazards or full-set owner acceptance.

Lesson: installing a previously tested source is a new consumer milestone;
prove actual normal loader after removing every candidate injection, compare
all selected slots, and repeat fresh-scene lifecycle at nonneutral/second-cycle
phases. Preserve source and room-shading evidence separately. No furniture,
economy, actor decision, gameplay timer or save-schema change for selection.
Remaining: independent side furniture/lifecycle/adoption, inherited rest/death
and full-set perspective/proportion/grade/detail/motion polish. Full goal active.
Handoff/evidence: character/veld-seated-north-selected-v1.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
 old=target.read_bytes()
 if title.encode() not in old:
  addition=note.encode('utf-8');target.write_bytes(addition+b'\n'+old if target.name=='CURRENT_STATUS.md' else old+b'\n\n'+addition)
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 1, 2026. Project: BrineSpace. Task: selected North seat/breath.

## Objective and acceptance
Full master-consistent Veld set and cross-family polish remain active. Install
tested North down/held/rise composition and prove actual normal-loader lifecycle.
Local installation complete; final owner motion acceptance open.

## Accepted decisions and constraints
Exact immutable current North sources; fixed256/p128224/H148 matte calibration.
Whole literal paths, no new art/grade/scale or furniture changes. Do not normalize
North seated107height to South126; actual perspective/contact govern silhouette.

## Current state
New build/verify/manifests/source-bindings; six states/36refs/24source PNGs.
grid_canvas normal paired loader and ACTIVE_ASSETS key/bindings installed.
New normal-loader native test+UID/isolated runner derived from candidate guards
with all candidate injections removed. review/index/source-room evidence saved.

## Verification
77composition checks0failures,three deterministic output files/28source bindings.
{checks}native checks0failures/{validation['seconds']}s engine0,8actual disk/fresh-scene
held restores,16actual power/suspend interruptions, complete selected-slot pixel/
calibration checks in9independent scenes; neutral timer joins and paused source
clock/contact/depth retained. Watched source hashes stable during run.
All{validation['realProfileFileCount']}owner non-log files unchanged, scratch APPDATA.
Eight native crop pairs reviewed;{equal}byte equal,maxdelta{delta}/255. Source and room
shade scoped separately. New fixture first mixed-indent parse failure archived;
corrected only test indentation. No natural chooser/all hazards/facings claim.

## Next action
Prove side furniture/service contact and interruption/Continue before adoption;
continue inherited rest/death and full cross-animation master/motion polish.
Current default observation North reader remains dormant/staged: no real North
desk-chair station, never invent furniture to integrate that source.
''',encoding='utf-8')
files=[f for f in P.iterdir() if f.is_file() and f.name!='evidence.json']
files += [f for f in O.iterdir() if f.is_file()]
files += [R/f for f in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json','tests/test_veld_seated_north_selected.gd','tests/test_veld_seated_north_selected.gd.uid','tests/test_veld_seated_north_continue.gd','tools/run_veld_seated_north_selected.py']]
bindings={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
bindings.update(json.loads((P/'source-bindings.json').read_text(encoding='utf-8'))['bindings'])
(P/'evidence.json').write_text(json.dumps({'bindings':bindings,'scope':'actual selected North lounge held disk Continue/power-suspend/source-join proof, prescribed chair; natural chooser/all rotations/hazards/owner acceptance separate','native':validation,'checks':checks,'restores':restores,'interruptions':16,'visualReview':review},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'notes':len(targets),'checks':checks,'bindings':len(bindings),'goalComplete':False}))
