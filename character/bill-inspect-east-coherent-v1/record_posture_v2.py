from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-inspect-east-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());verification=json.loads((P/'verification.json').read_text());r=json.loads((P/'registration.json').read_text())
assert report['passed'] and not report['realProfileChanges'] and verification['passed']
note='''
Bill east inspection upright correction — September 30, 2026.
Original source exec-650ccea9-8dfa-4a8c-9044-ee5e543f3621 and full original package/
evidence preserved in sources/inspect-v1.png and prior-candidate-v1. Original
461,441,433,437,445,445px figures yielded10px crown change. Targeted correction
exec-0cc94528-fb6b-4436-acce-ff2c84297d5a retained with exact prompt. Corrected
poses1..5 are464–467px tall at one fixed[.27,.3183] ruler,density1,sole223.
Pose0 remains479px and is explicitly excluded; five independent poses plus exact
slot0 closure retain two gear states/12refs/960ms loop. Packaged crownYs
[76,76,76,75,75] reduce prior10px range to1px. Native east helmet/connected body,
reader and matte details retained.43package/81native checks PASS11.34sec; master
and fresh native82 boards reviewed. All2,914 real non-log profile files unchanged.
Candidate source/player/scripted life_inspect evidence only; no normal selection,
actual room clearance or checkpointrestore. Four-direction candidate comparison
now binds8states/48refs and4selected idle masters in cardinal-review.html/png.
Cross-review flags a possible dark west bare face; verify its face ROI grade
before final selection. Cardinal source loops now exist; reader draw/stow all4,
normal family integration/actual services/restore/clearance, meals,generic rest,
dry death and full-set polish remain. Lesson: one source posture repair can leave
an outlier; preserve source and explicit selection, verify actual crown range,
then compare all facings against their own masters. Full goal active.
Handoff: character/bill-inspect-east-coherent-v1/HANDOFF.md.
'''
handoff='''# Project handoff

Updated: September 30, 2026 · BrineSpace · Bill east inspection upright correction

## Objective and acceptance
Complete the full master-consistent Bill set and full-set polish. This milestone
corrects east inspection height and adds an all-cardinal candidate comparison.

## Accepted decisions and constraints
One small reader held by two connected gloves, compact east master proportions,
readable face/brown hair/beard, matte quilted suit/burgundy patch/hardware.
256plane,pivot128,224,H148,sole223; fixed[.27,.3183] ruler,density1; native helmet
anchor19,4/scale1; body below headAxisY+31 protected. No per-pose normalization.

## Current state
Two gear states/12refs,960ms loop. Corrected source poses1..5 plus exact frame0
closure; corrected pose0 remains taller and is excluded with provenance retained.
Original source/package/evidence archived in prior-candidate-v1. Targeted edit
exec-0cc94528-fb6b-4436-acce-ff2c84297d5a reduces crown range10px→1px.
Current crownYs[76,76,76,75,75]. Cardinal review binds8candidate states/48refs
and4selected bare idle masters; interactive controls compare all facings.
No actor/registry/normal loader changes; old inspection remains selected.

## Verification
43package/81native checks PASS11.34sec. Source/master/frame bindings, fixed ruler,
explicit source selection/crown range, closure, soles and body protection pass.
Injected player validates candidate pixels/plane/dry depth0, scripted life_inspect
pose/snapshot and cycles0/1/7. Full-size master/native82 and cardinal boards reviewed.
All2,914 owner non-log files unchanged under scratch APPDATA; LFS source/frame PNGs.
No normal selection, autonomous service, actual clearance, interruption/diskrestore
or final owner/full-set motion acceptance. South/west3px crown range remains.

## Next action
Author cardinal standing reader draw/stow with exact idle/held joins, then normal
family integration and actual activity/restore/clearance. Before final selection,
check west bare face ROI grade: it appears darker than its idle in cardinal review.
Equipped meal consumers intentionally inspect; preserve their service clocks.
Continue meals,generic rest/dry death and full-set final consistency/polish.
Goal remains active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill east inspection height corrected — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=list((P/'sources').glob('*'))+[P/name for name in ['source-rulers.json','build.py','verify.py','bare-manifest.json','helmet-manifest.json','registration.json','material-grade.json','verification.json','HANDOFF.md','cardinal-review-bindings.json','cardinal-master-review.png','build_cardinal_review.py']]+[native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_inspect_east_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':verification['checks'],'native':81},'native':report,'scope':'source/player/scripted stage;no normal selection,world clearance or restore proof','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file()}},indent=2)+'\n')
print('Recorded east1px crown correction and cardinal master comparison')
