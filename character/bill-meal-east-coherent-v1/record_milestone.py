from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OUT=ROOT/'output/bill-meal-east-candidate-native-v1'
verification=json.loads((P/'verification.json').read_text());native=json.loads((OUT/'validation.json').read_text())
assert verification['passed'] and native['passed'] and not native['realProfileChanges']
assert '64 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
handoff='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill east bareheaded eating candidate

## Objective and acceptance
Complete Bill's full master-consistent animation set, then cross-animation polish.
New east eating loop authored and packaged; normal service selection remains old.

## Accepted decisions and constraints
Selected east matte idle owns face/hair, suit details, height and proportions.
No helmet meal artwork: equipped meals retain the installed reader behavior.
One bowl supported at waist, one spoon, two connected arms/hands, stable narrow
stance; an upright torso rather than a whole-body bow toward the bowl.

## Current state
sources/eat-v1.png and exact prompt-eat.txt retain built-in generation
exec-aa6f79a3-e611-4539-bf50-d6e2bc79c557. Six authored source figures with heights
429/429/430/427/427/427px. Fixed whole-atlas ruler[.31,.345],density1.0;
selected master neutral/hair/skin/burgundy grading and front-boot sole registration.
One bare eat-east candidate,seven slots/six authored poses;960ms duration
[140,120,140,180,140,120,120]. Slot6 copies exact slot0 for whole-figure closure.
Native256 plane/pivot128,224/H148,dry depth0. index.html compares loop to master.
build.py,verify.py,source-rulers/registration/material-grade/frame hashes retain
reproducible packaging. No normal loader/ACTIVE_ASSETS/actor changes for this art.

## Verification
23package/64native checks pass11.56s. Raw/source/master bindings, shared density,
six distinct poses, authored pacing, loop repeat/closure and planted sole pass.
Crown headAxesY[76,76,76,77,77,77],X[129,129,129,128,129,129]. Full148/native82
boards visually reviewed against selected idle. Source supports bowl while spoon
scoops/lifts/touches lips/lowers; no extra hands or foot steps observed.
Initial[.285,.345] ruler was too narrow: native crown span116–138 vs master114–140,
leg band175–195 span114–138 vs111–138,boots113–145 vs110–149. Shared x.31 improves
those bands to114–138,112–138 and112–146. It preserves one ruler for every pose;
no independent frame width/height adjustments. Remaining small silhouette/detail
differences belong to later family/full-set comparison,not hidden by per-frame fit.
Scratch APPDATA;2,914owner non-log files unchanged. Candidate injection/source
playback evidence only; no meal entry/exit, actual counter/world or restore proof.

## Next action
Author east drink and bowl/cup pickup/return transitions with exact selected idle
and held prop joins. Preserve original6s eating/3s drink clocks and bare/equipment
behavior,then normal install/actual counter/interruptions/disk restore evidence.
Continue west/north/south meals,generic rest/dry death and full-set polish.
Inspection broader contact/clearance/hazard/drink-boundary audits remain open in
bill-inspect-family-v1/HANDOFF.md. Full goal active; no commit/export requested.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''
Bill east bareheaded eating candidate — September30,2026.
Built-in source exec-aa6f79a3-e611-4539-bf50-d6e2bc79c557/exact prompt retained.
Six authored429/429/430/427/427/427px figures: waist-supported bowl, spoon scoop,
lift/lips/lower, two connected hands and planted feet. Fixed[.31,.345] atlas ruler,
selected matte master neutral/skin/hair/burgundy grade, sole223/pivot128,224/H148.
Seven slots/six authored poses,960ms,exact whole closure;crownY76–77/X128–129.
23package/64native PASS11.56s;148/82boards compared to idle;2,914owner files intact.
Lesson: compare source ruler against independent head/leg/boot bands, not height
alone. Initial x.285 was too narrow; shared x.31 improves proportions without
independent pose scaling. Keep bowl at waist and spine upright through the spoon
arc; a six-pose gesture can use a seventh exact closure slot with authored timing.
Source/player candidate only; old normal meal selection remains. Next east drink,
pickup/return then actual service/normal install;other cardinal meals/rest/drydeath
and full-set polish remain,as do inspection broader contact checks. Goal active.
Handoff: character/bill-meal-east-coherent-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill east bareheaded eating candidate — September30,2026\n'+note+'\n').encode()+status.read_bytes())
files=list((P/'sources').glob('*'))+[P/name for name in ['build.py','verify.py','manifest.json','source-rulers.json','registration.json','material-grade.json','verification.json','frame-hashes.json','HANDOFF.md','index.html','contact-sheet.png']]+[ROOT/'tests/test_bill_meal_east_candidates.gd',ROOT/'tools/run_bill_meal_east_candidate_validation.py',OUT/'validation.json',OUT/'loaded-water-carry.png']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':23,'native':64},'native':native,'scope':'source/master ruler/grade/candidate loop only; full meal transitions and normal activity installation pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded Bill east eating candidate and remaining full-set work')
