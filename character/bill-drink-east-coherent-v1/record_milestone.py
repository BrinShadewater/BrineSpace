from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OUT=ROOT/'output/bill-drink-east-candidate-native-v1'
v=json.loads((P/'verification.json').read_text());n=json.loads((OUT/'validation.json').read_text())
assert v['passed'] and n['passed'] and not n['realProfileChanges']
assert '71 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
handoff='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill east bareheaded drinking candidate

## Objective and acceptance
Complete Bill's full master-consistent animation set,then cross-animation polish.
East drinking and eating loops now authored; both remain source candidates.

## Accepted decisions and constraints
Selected matte east idle owns proportions,face/hair,suit and colour authority.
Eating frame000 is a secondary cross-action reference,not a new identity master.
Exactly one small dark steel cup,two connected arms/hands,upright head/spine,
planted feet. Equipped meals retain the installed standing reader sequence.

## Current state
Built-in source exec-833c490a-21ec-4b29-96a3-d5d7021474bb saved as sources/drink-v1.png
with exact prompt-drink.txt. Six source figures443/443/443/445/445/444px tall.
Fixed atlas ruler[.31,.3325],density1.0; selected neutral/skin/hair/burgundy grade.
One bare drink-east candidate,seven slots/six poses: waist/lower chest/mid-lift/
lips/mid-lower/waist/exact first-pose closure.960ms durations140/120/140/180/140/120/120.
Plane256/pivot128,224/H148/dry0; build/verification/registration/source-rulers and
frame hashes retained. prepare_tools initially clones eating tools; build.py,
verify.py and native fixture are the current maintained drink versions.
Cross-action-review.html/png compare drink,eat and selected idle with file hashes.
No normal loader/registry/actor change; full meal family integration remains pending.

## Verification
24package/71native checks PASS11.61s. Exact source pixels,drink/east identity,
dry metadata,H148 plane,authored timing,loop repeats and exact closure verified.
Native148/82 board and full-size cross-action board visually reviewed. Crown
Y77/77/77/76/76/76 and X129/129/129/130/129/130 retain upright one-pixel variation.
Independent master/head/leg/boot bands compared: master114–140/111–138/110–149,
eat114–138/112–138/112–146,drink114–139/111–139/111–148. No per-pose scaling.
No obvious extra hands,steps,bright gloss or whole-body bow in the gesture.
Fine emblem/detail and small silhouette differences remain for full-set polish.
All2,914owner non-log files unchanged under scratch APPDATA. Candidate injection
and playback only; no cup pickup/return,actual counter/normal install/restore proof.

## Next action
Author east bowl/cup pickup/return and food-to-drink handoff with exact idle/held
joins,then install full east meal service retaining original6s/3s clocks.
Prove actual counter contact,interruptions and disk restore. Continue cardinal
meals,generic rest/dry death and cross-family material/detail/proportion/pacing
polish. Inspection broader contact/hazard/equipped-drink-boundary audits remain
open in bill-inspect-family-v1/HANDOFF.md. Goal active; no commit/export requested.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''
Bill east bareheaded drinking candidate — September30,2026.
Built-in source exec-833c490a-21ec-4b29-96a3-d5d7021474bb/exact prompt retained.
Selected idle is identity authority; eating frame000 provides cross-action style.
Six443/443/443/445/445/444px figures,one steel cup and connected two-arm gesture.
Fixed[.31,.3325] ruler,master matte neutral/hair/skin/burgundy grade,sole223,
plane256/pivot128,224/H148/dry0. Seven slots/six authored poses,960ms/exact closure.
Crown Y76–77/X129–130.24package/71native PASS11.61s;native148/82 and source-bound
drink/eat/idle boards reviewed. Owner2,914non-log files unchanged under scratch.
Lesson: keep idle as authority when referencing another action; that action is
a consistency comparison. Check head/leg/boot bands separately: drinking114–139/
111–139/111–148 vs idle114–140/111–138/110–149. Distinct waist/chest/mouth cup poses
retain a planted upright figure. Validate action metadata when cloning tooling;
dry clips still carry kind/facing tags. Fine emblem/detail/silhouette polish remains.
Source/player candidate only; no normal selection. Next bowl/cup pickup/return,
food-to-drink handoff and actual service integration,then remaining cardinals,
rest/drydeath/full-set polish. Inspection wider contact audits remain. Goal active.
Handoff: character/bill-drink-east-coherent-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill east bareheaded drinking candidate — September30,2026\n'+note+'\n').encode()+status.read_bytes())
files=list((P/'sources').glob('*'))+[P/name for name in ['build.py','verify.py','manifest.json','source-rulers.json','registration.json','material-grade.json','verification.json','frame-hashes.json','HANDOFF.md','index.html','contact-sheet.png','build_cross_review.py','cross-action-review.html','cross-action-review.png','cross-action-bindings.json']]+[ROOT/'tests/test_bill_drink_east_candidates.gd',ROOT/'tools/run_bill_drink_east_candidate_validation.py',OUT/'validation.json',OUT/'loaded-water-carry.png']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':24,'native':71},'native':n,'scope':'source/master cross-action grade/ruler/candidate loop; cup transitions and normal service integration pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded drinking candidate/cross-action review and remaining full-goal work')
