"""Record the scoped context correction without converting it into library acceptance."""
from pathlib import Path
import ast,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-walk-joins-v1/context-review-v1'
review=json.loads((D/'dispatch-review.json').read_text(encoding='utf-8'))
assert review['dispatchChecksPassed'] and review['checks']==82 and not review['fullProjectFreezePassed']
for name in ['prepare_bill_join_context_review_v1.py','run_bill_walk_join_context_native_v1.py','build_bill_join_family_review_v1.py','publish_bill_join_context_review_v1.py','record_bill_join_context_milestone_v1.py']:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
uid=(R/'tools/review_bill_walk_join_context_native_v1.gd.uid').read_text().strip()
assert sum(p.read_text().strip()==uid for p in (R/'tools').glob('*.gd.uid'))==1
paths=[p.relative_to(R).as_posix() for p in D.glob('*.png')]
result=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(paths)+'\0').encode(),capture_output=True,check=True,cwd=R)
entries=result.stdout.decode().split('\0')
assert all(entries[i+2]=='lfs' for i in range(0,len(entries)-1,3))
family=json.loads((D/'family-review.json').read_text(encoding='utf-8'))
family.update(visualReviewed=True,reviewer='Codex',findings='Whole source and native boundaries reviewed: selected run/carry/weld are darker, face and suit detail coarser than current idle/walk/reach. Running lean and low gait height intentional; do not normalize pose bounds. Full sequences not visually accepted.')
(D/'family-review.json').write_text(json.dumps(family,indent=2)+'\n',encoding='utf-8')
review.update(visualReviewed=True,reviewer='Codex',nativeCrop=[315,155,820,310],familyBoardSha256=hashlib.sha256((D/'family-comparison.png').read_bytes()).hexdigest(),nativeBoardSha256=hashlib.sha256((D/'native-boundaries.png').read_bytes()).hexdigest(),browserProofSha256=hashlib.sha256((D/'browser-review.png').read_bytes()).hexdigest(),pythonSyntaxChecks=5,newPairedUniqueGDUIDs=1,pngLFSChecks=len(paths))
(D/'dispatch-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
note='''

## Bill walking joins: actual activity dispatch correction — October 4, 2026

Optional provider reset now occurs before gear/water/direction/other-state/action
early returns in scripts/grid_canvas.gd, and explicitly on death/inspection/meal
texture overrides. This closes stale walking/settle after special activity bypass.
Normal provider remains null; no loader/art admission or actor movement change.
Actual native getter checks:82/0,engine0/noERROR/WARNING,9 prescribed contexts
(helmet,water,West,run,carry,weld,construction entry,inspection,meal),12 retained
room/source captures,87.44s. Every special source equals provider-free control;
each dry East idle return equals current idle without stale gait. Scratch APPDATA,
all2931owner non-log hashes unchanged. NOT natural context choice/full gear/water
loops/death transition acceptance. Grid/helper frozen bytes unchanged during run.
Whole-project freeze FAILED: concurrent scripts/main.gd edit and two review-only
artifact additions. Raw failed validation preserved; no clean full-project claim.
New fixture omitted from broad runner input map; exact current fixture copied,
not asserted before/after-frozen. FivePython syntax/onepaireduniqueGDUID and PNG LFS.

context-review-v1 contains ten common-H148 source samples, native boundaries and
browser proof, all full boards visually inspected. Selected run/carry/weld remain
darker with coarser face/suit detail than current master idle/walk/reach. Physical
registration is declared whole-scale/pivot only; lean/gait bounds not forced.
First native review crop hid upper character, caught in image review and corrected
to315,155,820,310 without altering native captures. Review scope only; full loops
not accepted. Next concrete matching target is these three East activity banks,
then native boundary motion and family admission. No additional walk regeneration.
Current normal selection unchanged, full Bill objective incomplete; no commit/export.
Handoff:character/bill-east-walk-joins-v1/HANDOFF.md.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for path in paths:
 with path.open('a',encoding='utf-8') as f:f.write(note)
handoff='''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: Bill walking and activity boundaries

## Objective and acceptance
Finish Bill’s consistent animation library soon. Current idle/walk/reach and authored
walking joins staged; full normal family and station behavior acceptance remains open.

## Accepted decisions and constraints
Preserve master matte material, warm face, whole-source detail and 48 walking poses.
No anatomical stamping, ghost crossfades or forced gait bounds. Reversible work
authorized; no commit/export. Normal provider stays null pending coherent selection.

## Current state
grid_canvas optional join reset now handles early-return activity/equipment paths.
context-review-v1: nine-context report, twelve native/source pairs, ten-source board,
native board, browser proof and exact current fixture copy. Native-motion-v2 retains
same-source joined/unjoined walking review; source art/timing unchanged this turn.

## Verification
Actual dispatch 82/0, nine contexts,87.44s,engine0/noERROR/WARNING. All special
sources and dry East idle returns equal provider-free controls. Scratch APPDATA;
2931 owner files unchanged. Grid/helper bytes stable; whole-project freeze failed
on concurrent main.gd edit plus review additions. New fixture not in harness freeze.
No full native context loop/death acceptance. Prior4064 walking and536 helper checks
retain their tested revision/scope. Current whole source/native/browser boards reviewed.
5 Python syntax,1 paired unique GDUID,27 PNG LFS checks.

## Next action
Match East selected run/carry/weld source banks to current master idle/walk/reach:
observed darker suit/face and coarser detail persist, confirmed at source and native
scale. Preserve current normal selection until family boundaries hold. Then normal
admission, full station jobs/save/TitleContinue and remaining cardinal/equipment/
water/life/hazard/cargo master closeout. Do not regenerate accepted walking bank.
'''
(R/'character/bill-east-walk-joins-v1/HANDOFF.md').write_text(handoff,encoding='utf-8')
print(json.dumps(dict(dispatchChecks=82,fullProjectFreeze=False,maintainedRecords=8,pythonSyntax=5,pairedUniqueGDUID=1,pngLFS=len(list(D.glob('*.png'))))))
