from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OUT=ROOT/'output/bill-drink-north-candidate-native-v1'
v=json.loads((P/'verification.json').read_text());n=json.loads((OUT/'validation.json').read_text())
assert v['passed'] and n['passed'] and not n['realProfileChanges']
assert '71 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
handoff='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill north drinking candidate

## Objective and acceptance
Complete Bill's full master-consistent animation set, then full-set polish.
North drinking loop authored and native reviewed; cup pickup/return pending.

## Accepted decisions and constraints
Selected north idle owns design, perspective, standing density and matte finish.
Right hand holds cup in front, physically occluded from rear camera. Left arm
hangs naturally. Read action through right elbow/forearm silhouette, not through
props drawn on back or a camera twist. Current actual galley contacts are N/S.
Preserve original service clocks and helmet inspection meal behavior.

## Current state
Raw built-in exec-0cb0a4fb-fda7-4d2e-8bcf-d63d5cb68a71/exact prompt retained.
Six figures405/404/404/404/404/404px tall. Fixed atlas ruler[.35,.3658],density.92,
selected north neutral/hair/burgundy grade. Segmented figures retain alpha;
low-opacity source glow outside figure components excluded from exports.
One bare staged drink-north state, seven slots960ms, six distinct whole figures,
exact first/last pose. 256plane/pivot128,224/H148/dry0/master sole223.
Build, verify, registration, source/grade/hash evidence and animated previews
retained. No normal north selection, actor, galley geometry or reward changes.

## Verification
24 package/71 native checks PASS12.97s. Exact source binding and loaded pixels,
direction/drink metadata, planted sole, shared density, authored pacing,
repeated cosmetic cycles and whole-pose closure. Native148/82/idle boards reviewed.
Cross-action-review.png/html/json compares selected idle, north eating and drink
with hash-bound alpha-band diagnostics. Drinking crown76 in every frame equals
master76; eating76–77. Frame0 head bounds113–142 vs master112–143; legs/boots
108–148 vs master108–147 and eating108–148. No per-frame scaling/warp added.
Fine backpack/panel/suit-texture differences remain for full-set polish.
Scratch APPDATA; all2,914 owner non-log files unchanged. Actual counter gesture,
pickup/return, interruption/restore and autonomous service unproved.

## Next action
Author north bowl and cup pickup/return with exact idle/current held-loop donors,
short reach before full reach, rear occlusion and fixed planted body. Complete
south meals, then actual N/S phase-clock integration and checkpoint/contact proof.
West meal family, generic rest/dry death, inspection wider contact/hazard and
equipped-drink-boundary audits, full-set polish remain. Goal active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''
Bill north drinking candidate / cross-action master comparison — September30,2026.
Built-in exec-0cb0a4fb-fda7-4d2e-8bcf-d63d5cb68a71/exact prompt retained.
Six rear upright405/404/404/404/404/404px source figures, fixed[.35,.3658] atlas
ruler,density.92, selected north matte neutral/hair/burgundy grade and sole223.
Right hand/cup stay in front and naturally occluded; free left arm stays down.
One bare staged state/seven960ms slots/exact whole-pose closure.24package/
71native PASS12.97s; native148/82 and idle boards reviewed. All2,914 owner non-log
files unchanged under scratch APPDATA. No normal loader/actor/geometry changes.
Cross-action PNG/HTML/JSON bind selected idle/north eat/drink pixels and compare
independent alpha bands: drinking crown76 equals master76, eating76–77;
drink head113–142 vs master112–143; legs/boots108–148 vs master108–147.
Lesson: explicitly separate one cup arm from the free arm in rear gesture
authoring, preserve physically correct prop occlusion, compare head/leg/boot bands
across actions in addition to whole-body bounds. Fixed registration metrics support
visual review; they do not prove fine backpack/panel/suit detail is identical.
Low-opacity raw source glow outside segmented figure components is excluded while
raw source remains untouched. Fine design/material/proportion polish pending.
Next north bowl/cup pickup-return, south meals, actual N/S service phase/contact/
interruption/restore proof, remaining west/rest/drydeath and full-set polish.
Full goal active. Handoff:character/bill-drink-north-coherent-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill north drinking candidate / master cross-check — September30,2026\n'+note+'\n').encode()+status.read_bytes())
files=[P/name for name in ['build.py','verify.py','manifest.json','verification.json','HANDOFF.md','index.html','source-rulers.json','registration.json','frame-hashes.json','material-grade.json','contact-sheet.png','cross-action-review.png','cross-action-review.json','cross-action-review.html','build_cross_review.py']]+list((P/'sources').glob('*'))+[OUT/'validation.json',OUT/'loaded-water-carry.png',ROOT/'tests/test_bill_drink_north_candidates.gd',ROOT/'tools/run_bill_drink_north_candidate_validation.py']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':24,'native':71},'native':n,'scope':'staged drinking loop and visual cross-action comparison only; actual meal phases/contact/interruption/restore pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded north drinking loop, native proof, cross-action metrics and remaining meal work')
