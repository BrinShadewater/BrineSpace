"""Record actual-job evidence, preserving the remaining admission boundary."""
from pathlib import Path
import json,ast,subprocess,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-actual-jobs-v1'
q=json.loads((D/'review.json').read_text());v=q['native'];assert v['passed'] and v['checks']==2978
for name in ['prepare_bill_actual_jobs_v1.py','run_bill_actual_jobs_v1.py','publish_bill_actual_jobs_v1.py','record_bill_actual_jobs_v1.py']:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
uid=(R/'tools/review_bill_actual_jobs_v1.gd.uid').read_text().strip();assert sum(p.read_text().strip()==uid for p in (R/'tools').glob('*.gd.uid'))==1
pngs=[p.relative_to(R).as_posix() for p in D.glob('*.png')]
r=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R)
items=r.stdout.decode().split('\0');assert all(items[i+2]=='lfs' for i in range(0,len(items)-1,3))
finding='All six sampled retained review boards visually inspected, plus browser proof. New East pickup/torch handoffs retain matte detail. Existing carry-start/turn and other cardinal banks remain visibly different; coherent normal admission still pending. Weld exits pose2 into stow0 in this job: completion passed, exact loop-to-stow pixel continuity is not claimed. Arrival stow controller presents its North unload through a carry pose; sampled entry/completion captures do not establish every unload-plan source slot or continuous cadence.'
q.update(visualReviewed=True,findings=finding,pythonSyntax=4,pairedUniqueUID=1,pngLFS=len(pngs),browserProofSHA256=hashlib.sha256((D/'browser-proof.png').read_bytes()).hexdigest())
(D/'review.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
note=f'''\n\n## Bill actual construction/workshop jobs — October 4, 2026

character/bill-actual-jobs-v1: selected production Bill actor/player, fixture-only
repaired East idle/walk/reach/carry/weld/draw/stow/pickup/unload staging. Actual
paid corridor dispatched, approached, constructed and reservation released; all
18 draw/weld/stow slots visited. Real authored workshop bench entry followed by
production inspect/work/pickup, generated carrying route, arrival/stow and service
completion; all11 repaired East pickup slots displayed, route standing/segments
checked. Monotonic10ms simulation updates; no source-clock seeding. Other facing
and carry transition banks retain current selection. 2,978checks/0,36retained
room/source pairs,38.09s; engine0/clean,5,482frozen inputs and2,936owner non-log
files unchanged under scratchAPPDATA. FourPython syntax,onepaired uniqueUID,
{len(pngs)}PNG LFS; six complete same-scale review boards and browser proof inspected.

{finding}
First native fixture v1 had21 failures from an invalid East-of-ColdStore build
site; preserved evidence/profile/input maps. Corrected to the actual core East
port for v3. v2 runner stopped before engine launch on output-version assertion.
The initially suspected missing pickup dispatch was disproved: CrewLife.pose and
CrewLife.elapsed already own this phase. No gameplay change was needed or made.
No normal admission, owner acceptance, gear, Continue, autonomous workshop choice
or inventory cargo-ownership assertion. Full Bill objective remains incomplete.
Next: reconcile selected carry entry/turn sources against the repaired family,
then coherent admission and save/resume checks. Review:
http://127.0.0.1:8791/character/bill-actual-jobs-v1/.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
(D/'HANDOFF.md').write_text('''# Project handoff

Updated: October4,2026 · Project: Brine Space · Task: Bill actual jobs

## Objective and acceptance
Wrap Bill through actual job evidence before coherent installation. Actual-job
fixture passed; full animation objective and normal admission remain open.

## Accepted decisions and constraints
Whole artwork preserved. Selected production actor/player, scratch APPDATA,
paid-build/failure flags retained. No live profile test, commit or export.

## Current state
Four tools and paired native fixture UID; character/bill-actual-jobs-v1 contains
review/report/validation, six same-scale native boards and browser proof.
No gameplay/art source changes. v1 invalid build site and v2 pre-launch assertion
retained; v3 fixes the site and completes both jobs. Shared CrewLife handler
already dispatches pickup; initial missing-dispatch concern disproved.

## Verification
2,978/0; all18 torch and11 pickup slots visited; paid completion/reservation and
workshop generated route/arrival/service completion;36retained pairs. Engine
clean;5,482inputs and2,936owner files exact.4Python/1UID/7PNG LFS. Six boards and
browser proof inspected. No continuous cadence, every stow-plan source identity,
inventory ownership, gear or Continue claim. Weld2->stow0 not byte-exact.

## Next action
Existing carry entry/turn sources still differ from repaired East material.
Reconcile these bridges, then coherent admission and save/resume verification.
Do not repeat source repairs or infer full Bill completion from this fixture.
''',encoding='utf-8')
print(json.dumps({'checks':2978,'failures':0,'maintainedRecords':8,'pythonSyntax':4,'pairedUniqueUID':1,'pngLFS':len(pngs)}))
