from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OUT=ROOT/'output/bill-meal-entry-north-candidate-native-v1'
v=json.loads((P/'verification.json').read_text());n=json.loads((OUT/'validation.json').read_text())
assert v['passed'] and n['passed'] and not n['realProfileChanges']
assert '87 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
handoff='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill north bowl pickup/return candidate

## Objective and acceptance
Complete Bill's full master-consistent animation set, then full-set polish.
North bowl pickup/return joins exact selected idle to current eating hold.

## Accepted decisions and constraints
Selected rear idle owns identity, matte suit, perspective and standing density.
Front bowl/hands remain physically occluded from rear camera; show progressive
connected elbows/forearms, no back-mounted props or extra hands. Planted stance.
Current galley contacts N/S; no geometry or service-clock changes for art tests.

## Current state
Raw built-in exec-0a407c91-0ad9-491d-b6e9-3c8bd720f376/exact prompt retained.
Six source heights420/420/420/416/416/416. Interiors0..4, primary5 redundant
low hold retained unused; exact master idle and eating000 donors own endpoints.
Fixed[.337,.3527] atlas ruler,density.95, selected north neutral/hair/burgundy
grade, sole223 and master front-boot registration. Two bare staged states/14refs,
seven580ms slots60/80/100/100/100/80/60; exact whole-pose reverse return.
Shared256plane/pivot128,224/H148/dry0. Source/build/verify/preview/registration/
hashes/evidence retained. No normal selection, actor, reward or geometry changes.

## Verification
28package/87native checks PASS12.00s: raw and donor bindings, exact loaded pixels,
dry finite metadata, pacing/endpoint hold, exact idle/held joins and reversals.
Native148/82 and idle boards reviewed. Interior head axes Y76–77, X127–129.
No obvious foot steps, back props or detached arms. Fine backpack/suit detail,
interior silhouette alignment and return/contact readability remain for polish.
All2,914 owner non-log files unchanged under scratch APPDATA. Source/native
loading only; actual worktop reach/contact, interruption and disk restore pending.
Exact endpoint joins do not establish physical counter contact.

## Next action
Author north cup pickup/return with exact idle/drink-held donors; assemble full
north meal family, then south meals. Prove actual N/S service contact and saved
pickup/core/return phases. West meals, generic rest/dry death, wider inspection
contact/hazard/drink boundary audits and full-set polish remain. Goal active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''
Bill north bowl pickup/return candidate — September30,2026.
Built-in exec-0a407c91-0ad9-491d-b6e9-3c8bd720f376/exact prompt retained.
Six source heights420/420/420/416/416/416; interiors0..4 include relaxed first
bend/forward reach/grasp/inward hold. Source5 redundant low hold retained unused.
Exact selected idle/current eating000 donors, fixed[.337,.3527] ruler,density.95,
selected north matte grade, sole223. Two bare states/14refs/seven580ms slots,
exact whole-pose reverse return. Interior headY76–77/X127–129.28package/87native
PASS12.00s; native148/82 and idle boards reviewed. All2,914 owner non-log files
intact under scratch APPDATA. No normal selection/actor/reward/geometry changes.
Lesson: maintain distinct short-bend and full-reach stages even when rear camera
occludes hands/bowl; preserve source and exact endpoint donors. Source joins and
native pacing are not evidence of actual worktop contact. Fine detail/interior
silhouette/contact and reversed-return readability remain for full-set polish.
Next north cup transitions/full family, south meals, actual N/S phase/contact/
interruption/restore proof, remaining west/rest/drydeath and full-set polish.
Full goal active. Handoff:character/bill-meal-entry-north-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill north bowl pickup/return candidate — September30,2026\n'+note+'\n').encode()+status.read_bytes())
files=[P/name for name in ['build.py','verify.py','build_preview.py','manifest.json','verification.json','HANDOFF.md','index.html','source-rulers.json','registration.json','frame-hashes.json','contact-sheet.png']]+list((P/'sources').glob('*'))+[OUT/'validation.json',OUT/'loaded-water-carry.png',ROOT/'tests/test_bill_meal_entry_north_candidates.gd',ROOT/'tools/run_bill_meal_entry_north_candidate_validation.py']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':28,'native':87},'native':n,'scope':'staged pickup/reversed return source and native joins only; real service contact/interruptions/restore pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded north bowl transitions, native joins and remaining service/contact work')
