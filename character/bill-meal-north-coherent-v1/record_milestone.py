from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;F=P.parent/'bill-meal-east-family-v1'
N=ROOT/'output/bill-meal-north-candidate-native-v1';E=ROOT/'output/bill-meal-east-family-selected-native-v1'
for out,checks in [(N,64),(E,299)]:
 report=json.loads((out/'validation.json').read_text());assert report['passed'] and not report['realProfileChanges']
 assert f'{checks} checks,0 failures' in (out/'native.log').read_text(encoding='utf-8')
assert json.loads((P/'verification.json').read_text())['passed'] and json.loads((F/'verification.json').read_text())['passed']
north='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill north eating candidate

## Objective and acceptance
Complete Bill's master-consistent animation set, then full-set polish. North
eating loop authored and reviewed; pickup/return and normal service pending.

## Accepted decisions and constraints
Selected north idle owns identity, matte materials and standing density.
Rear bowl/spoon remain naturally occluded in front; elbow silhouette carries
gesture. Keep planted boots, upright back and unchanged rear-facing camera.
Current galley_counter_stations selects north/south even for rotated counters.
Do not alter counter geometry to justify an east consumer.

## Current state
Raw built-in exec-a41c92bb-7560-4f69-b472-5400c1373947 and exact prompt retained
in sources. Six source figures 501/501/501/499/499/499px tall. Fixed atlas ruler
[.29,.2955], density1.14, selected north neutral/hair/burgundy grade. Seven slots
960ms, six distinct poses and exact whole-pose closure. 256plane/pivot128,224,
H148, dry0; master sole223. Build, registration, hashes, preview and evidence
retained. Staged candidate only, no normal north meal selection or actor changes.

## Verification
23 package/64 native checks PASS11.94s. Exact loaded pixels, dry/pivot metadata,
pacing, repeated cosmetic cycles and closure. Native148/82 and selected idle
boards visually reviewed. No obvious foot extension, extra hands or prop drawn
through back. Small backpack/detail and silhouette differences remain for full
polish; numerical crown range alone does not establish full identity acceptance.
Scratch APPDATA; all2,914 owner non-log files unchanged. Real counter gesture,
phase handoffs, interruption and disk restore remain pending.

## Next action
Author north drinking and bowl/cup pickup-return families, then south meals.
Integrate actual north/south service clocks with interruption/restore proof.
West meal family, generic rest/dry death and full-set polish remain. Goal active.
'''
family='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill east full bare meal family selected

## Objective and acceptance
Complete Bill's master-consistent animation set, then full-set polish.
Six-state east meal art now normally selected; actual phase integration pending.

## Accepted decisions and constraints
Four source parents retain provenance; family uses whole literal res paths.
580ms finite pickup/return,960ms loops, exact idle/held joins and reverse return.
Preserve original6s eat/3s drink clocks and helmet meal inspection behavior.
Actual galley counter stations choose north/south, including rotated counters.
East belongs in directional art coverage but has no normal galley consumer yet.

## Current state
Family status selected_runtime; grid_canvas._load_major_bill_animations loads
manifest normally and ACTIVE_ASSETS actionOverrides records it. Six states,
42refs/shared256plane/pivot128,224/H148/dry0. Parents remain staged provenance
packages. Current bare action chooser consumes eat/drink cosmetic loops; enter
and exit are loaded but not yet dispatched by the meal activity clock.
No Bill actor, galley geometry or reward changes this turn.

## Verification
39 assembly checks PASS; normal loader299 native checks PASS11.97s without
candidate injection. Exact parent pixels, pacing, joins, reversals, standing
metadata and closures. Fresh native82 family board reviewed. Scratch APPDATA;
all2,914 owner non-log files unchanged. Prior candidate299 PASS retained as
historical evidence; current normal-selection evidence is separate.
Bowl interior crown75–77/headX128–132 and fine suit/emblem/silhouette differences
remain for full polish. Actual activity/contact/interruption/restore unproved.

## Next action
Finish north/south meal source families for the existing actual galley contacts,
then implement and verify meal pickup/core/return phases preserving saved clocks.
East-only actual-counter plan is superseded by inspected current station code.
Continue remaining cardinal meals, generic rest/dry death and full-set polish.
Inspection wider contact/hazard/equipped-drink-boundary audits remain open.
Goal active; no commit/export requested.
'''
(P/'HANDOFF.md').write_text(north,encoding='utf-8');(F/'HANDOFF.md').write_text(family,encoding='utf-8')
note='''
Bill normal east meal art selection and north eating candidate — September30,2026.
East family normally selected through grid_canvas plus ACTIVE_ASSETS;39 assembly/
299 normal-loader native checks PASS11.97s, no candidate injection, native82
family board reviewed. Six states/42refs; enter/exit loaded but meal activity
clock not installed. Helmets retain inspection. Current authoritative galley
counter stations choose north/south even with rotated rooms; do not fabricate an
east consumer or change physical geometry for an art fixture. Earlier east actual
counter next-step is superseded. Finish actual N/S art before service phase work.
North eating exec-a41c92bb-7560-4f69-b472-5400c1373947/exact prompt retained;
six upright rear poses, source heights501/501/501/499/499/499, fixed[.29,.2955]
ruler, selected matte grade, sole223, seven960ms slots/exact closure.23package/
64native PASS11.94s;148/82 and idle boards reviewed. Staged only. Bowl/spoon must
remain occluded in front of rear-view torso; show elbow gesture, never props on
back or a camera turn. Fine backpack/detail/material/proportion polish remains.
Both scratch runs preserve all2,914 owner non-log files. Actual meal contact,
interruptions/restore and phase joins pending; no actor/reward/geometry changes.
Next north drinking/pickup/return, south meals, actual service integration; then
remaining west meals/rest/drydeath/full polish. Full goal active.
Handoffs: character/bill-meal-east-family-v1/HANDOFF.md and
character/bill-meal-north-coherent-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill east meal selection / north eating candidate — September30,2026\n'+note+'\n').encode()+status.read_bytes())
for package,out,checks,status in [(P,N,{'package':23,'native':64},'staged_candidate'),(F,E,{'package':39,'native':299},'selected_runtime')]:
 files=[package/name for name in ['build.py','manifest.json','verification.json','HANDOFF.md','index.html']]+list((package/'sources').glob('*'))+[out/'validation.json',out/'loaded-water-carry.png']
 if package==P:files += [P/name for name in ['source-rulers.json','registration.json','frame-hashes.json','material-grade.json','verify.py','contact-sheet.png']]
 else:files += [ROOT/'scripts/grid_canvas.gd',ROOT/'character/ACTIVE_ASSETS.json',ROOT/'tests/test_bill_meal_east_family_selected.gd']
 evidence={'status':status,'checks':checks,'native':json.loads((out/'validation.json').read_text()),'scope':'normal east art selection / staged north loop only; actual meal phase/contact/interruption/restore pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
 (package/('selected-evidence.json' if package==F else 'candidate-evidence.json')).write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
print('Recorded normal east art selection, actual N/S counter constraint and north eating candidate')
