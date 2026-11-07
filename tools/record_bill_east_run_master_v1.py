"""Record six authored run sources and scoped native evidence, with historical failure."""
from pathlib import Path
import json,ast,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-run-master-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((D/'native/validation.json').read_text(encoding='utf-8'));review=json.loads((D/'review.json').read_text(encoding='utf-8'));assert v['passed'] and v['checks']==75
assert all(sha(R/p)==s for p,s in review['protectedInputs'].items())
assert all(sha(R/p)==s for p,s in review['inputs'].items())
assert len({r['frameSha256'] for r in review['records']})==6
before=json.loads((D/'native/inputs-before.json').read_text(encoding='utf-8'))
for p in [D/'manifest.json']+list((D/'frames').glob('*.png')):assert before[str(p)]==sha(p)
names=['prepare_bill_east_run_master_v1.py','build_bill_east_run_master_v1.py','prepare_bill_east_run_native_v1.py','run_bill_east_run_master_native_v1.py','prepare_bill_east_run_native_v2.py','run_bill_east_run_master_native_v2.py','publish_bill_east_run_native_v2.py','record_bill_east_run_master_v1.py']
for name in names:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
for name in ['review_bill_east_run_master_native_v1.gd','review_bill_east_run_master_native_v2.gd']:
 uid=(R/'tools'/(name+'.uid')).read_text().strip();assert sum(p.read_text().strip()==uid for p in (R/'tools').glob('*.gd.uid'))==1
pngs=[p.relative_to(R).as_posix() for p in D.rglob('*.png')]
result=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R);entries=result.stdout.decode().split('\0');assert all(entries[i+2]=='lfs' for i in range(0,len(entries)-1,3))
review.update(visualReviewed=True,reviewer='Codex',visualScope='All six full raw sources, complete whole comparison, four full native pages and normal/quarter browser snapshots inspected. APNG frames chronologically decoded and byte/timing checked. No continuously watched native running-route or full world foot acceptance.',findings='Restored matte quilting, silver hardware and warm master face. All six poses stay close to original scale/stride silhouette. Small face/hair/badge variations and phase5 height+3px remain provisional; no normal admission.',browserProof={name:sha(D/name) for name in ['browser-normal.png','browser-quarter.png']},syntaxChecks=len(names),pairedUniqueUIDs=2,pngLFSChecks=len(pngs))
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
note=f'''

## Bill East complete six-pose running master repair — October 4, 2026

character/bill-east-run-master-v1 authors all6 East run figures using built-in
imagegen, after proving whole phases0/3; raw sources, exact prompts, reference
paths/hashes and6generation receipts retained. Each target/currentidle/master
uses matched1024physical profile. Returned raw squares are1254, not displayed1280;
actual file measurements establish density, avoiding a mistaken corrective scale.
Uniform whole raw→256 packing; no local grading, head stamp, anatomical splicing
or per-pose stretching. Disconnected <=3pixel components with maxalpha1 removed
as invisible background dust only. WholeY shifts0/0/0/0/0/-1, lossless alpha contact
registration to each original phase sole; height deltas1/1/1/0/1/3, sole delta0all6.
Original ordered6durations90/80/100/90/80/100 =540ms, loop and run stride.168 intact.
Original selected manifest+6frames remain byte unchanged. Four APNGs each6frames,
normal540/quarter2160ms,24decoded frames byte/timing exact.

NativeV1 preserved:75checks10failures because fixture seeded clock position with
actor.foot/gridCellSize, unlike actual getter's converted position/offset. Captures
repeated phase0. Corrected fixture only, no art workaround; V2 seeds actual
get_test_walker_position/gridCellSize. V2 engine0/noERROR/WARNING,75checks0,
16actual room/source pairs,52.55s,4960inputs unchanged INCLUDING candidate bank
and exact new fixture/runner,2931owner non-log fingerprints unchanged,scratchAPPDATA.
All6run source selections and last→first wrap verified plus current master idle
before/after, both selected/candidate. Explicit phases at fixed foot in default
furnished ColdStore: NOT physical running route, autonomous emergency goals,
moving boot contact or normal admission/full gear/save acceptance.

All6whole raws, full source comparison,4full native pages and normal/quarter
browser snapshots reviewed. Matte fabric/hardware/warm face closer to master;
small face/hair/badge differences andphase5height+3 remain provisional. Normal
selection unchanged. Preview:http://127.0.0.1:8791/character/bill-east-run-master-v1/.
8Python syntax,2paired uniqueGDUID,{len(pngs)}PNG LFS checked. Next: East carry8
and torch6 appearance matching, then moving run/boundary motion and coherent
family admission. Full Bill objective incomplete; no commit/export.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for path in paths:
 with path.open('a',encoding='utf-8') as f:f.write(note)
handoff=f'''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: East running master repair

## Objective and acceptance
Finish consistent Bill animation library soon. Six East run poses now authored
against current matte master; family admission and full gameplay acceptance open.

## Accepted decisions and constraints
Preserve complete poses, narrow build, source registration and original run order/
540ms/.168stride. No head stamping/per-pose stretching. Reversible work authorized;
normal selection unchanged. No commit/export or unrelated crew/gameplay edits.

## Current state
Six raw images/exact prompts/reference and receipt chains; frames/manifest/APNGs,
whole comparison and native four-page review here. tools prepare/build/review/
run/publish/record_bill_east_run* reproduce locally. Prompts:pose-000 through
pose-005/prompt.txt. Built-in imagegen only; no API/key needed.

## Verification
Uniform raw1254→256, wholeY0/0/0/0/0/-1; height deltas1/1/1/0/1/3, sole0all6.
Original selected7inputs unchanged; four6frameAPNGs byte/timing exact. NativeV2
75/0,16pairs,52.55s,4960inputs and2931owner files unchanged,scratchAPPDATA.
All6actual retained sources/wrap/idlebeforeafter. Prescribed fixed-foot phases,
not physical running. FailedV1 wrong clock position75/10 retained, correctedV2.
Six raws/whole board/four native pages/browser snapshots inspected. Small face/
hair/badge variations andphase5height+3provisional.8Python,2UIDpairs,{len(pngs)}PNG LFS.

## Next action
Match East carry8 and torch6 whole poses to current master next; running complete
source bank available, avoid regenerating all6 unnecessarily. Then moving run/
idle/action boundary motion, coherent normal family admission, station jobs/
Save/TitleContinue and remaining cardinal/equipment/water/life/hazard coverage.
Current full Bill objective incomplete.
'''
(D/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (R/'character/bill-east-walk-joins-v1/HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\nOctober4 continuation: six East run master poses now authored and scoped native75/0 in ../bill-east-run-master-v1/HANDOFF.md. Next appearance targets carry8/torch6, then moving/boundary/native family admission.\n')
print(json.dumps(dict(authoredPoses=6,nativeChecks=75,nativeFailures=0,protectedSelectedInputs=7,maintainedRecords=8,pngLFS=len(pngs))))
