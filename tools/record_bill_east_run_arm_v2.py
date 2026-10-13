"""Record owner-reported anatomical repair separately from technical source acceptance."""
from pathlib import Path
import json,ast,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-run-master-v2';A=R/'character/bill-east-run-master-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((D/'native/validation.json').read_text(encoding='utf-8'));review=json.loads((D/'review.json').read_text(encoding='utf-8'));assert v['passed'] and v['checks']==75 and v['inputCount']==4962
assert all(sha(R/p)==s for p,s in review['protectedInputs'].items())
assert all(sha(R/p)==s for p,s in review['inputs'].items())
for slot in [1,2,3,4]:assert (D/f'frames/{slot:03}.png').read_bytes()==(A/f'frames/{slot:03}.png').read_bytes()
inherited=json.loads((D/'inherited-sources.json').read_text(encoding='utf-8'))
assert all(sha(Path(item['path']))==item['sha256'] for files in inherited.values() for item in files.values())
names=['prepare_bill_east_run_arm_v2.py','build_bill_east_run_arm_v2.py','prepare_bill_east_run_native_v3.py','run_bill_east_run_master_native_v3.py','publish_bill_east_run_arm_v2.py','record_bill_east_run_arm_v2.py']
for name in names:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
uid=(R/'tools/review_bill_east_run_master_native_v3.gd.uid').read_text().strip();assert sum(p.read_text().strip()==uid for p in (R/'tools').glob('*.gd.uid'))==1
pngs=[p.relative_to(R).as_posix() for p in D.rglob('*.png')];result=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R);entries=result.stdout.decode().split('\0');assert all(entries[i+2]=='lfs' for i in range(0,len(entries)-1,3))
review.update(visualReviewed=True,reviewer='Codex',ownerComplaint='His arm looks messed up in the previous running candidate.',newAuthoredSlots=[0,5],byteIdenticalInheritedSlots=[1,2,3,4],sourceGeneration='Two new built-in whole-source image edits; four prior sources explicitly inherited.',findings='Backward shoulder patch/sleeve now follow one connected upper arm, elbow, forearm and glove. Duplicate vertical chest sleeve removed. Whole raws, all-frame comparison, neighboring seam4/5/0/1, four native pages and browser normal/quarter snapshots inspected. Current small face/hair/badge and height+3px variations provisional. No moving-route, continuous native cadence or owner acceptance claim.',browserProof={name:sha(D/name) for name in ['browser-normal.png','browser-quarter.png']},syntaxChecks=6,pairedUniqueUIDs=1,pngLFSChecks=len(pngs))
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
old=json.loads((A/'review.json').read_text(encoding='utf-8'));old.update(ownerFeedback='Arm looks messed up; backward poses0/5 show disconnected patch/sleeve.',supersededBy='character/bill-east-run-master-v2/manifest.json',visualAcceptance=False)
(A/'review.json').write_text(json.dumps(old,indent=2)+'\n',encoding='utf-8')
note=f'''

## Bill East backward-running arm repair — October 4, 2026

Owner reported messed-up arm in the prior master-running candidate. Source review
found near shoulder patch pinned to a spare vertical chest sleeve while the
backward arm was drawn separately, especially phases0/5. V1 technical passes
did NOT establish anatomy acceptance; V1 review records complaint/supersession.
character/bill-east-run-master-v2 repairs two COMPLETE figures with built-in imagegen;
exact prompts, four reference hashes/roles, raw sources and receipts retained.
Patch now belongs to upper-arm sleeve; one chain shoulder→elbow→cuff→glove,
without duplicate chest arm. Four frames1/2/3/4 explicitly inherited and
byte-identical toV1. Uniform raw→256 and whole contact registration only,
no arm stencil/head stamp/local grading/per-pose stretching. Height deltas
3/1/1/0/1/3, sole0all6; original540ms/.168stride and selected7inputs unchanged.
APNG24decoded frames exactRGBA/timing. Original V1 raws/provenance preserved.

NativeV3 engine0/noERROR/WARNING,75checks0,16world/source pairs,54.93s,
4962inputs frozen unchanged INCLUDING revised bank/fixture,2931owner non-log
hashes unchanged,scratchAPPDATA. All6source phases and clock wrap plus master
idle before/after. Prescribed fixed-foot sources, NOT physical running route,
natural emergency choice, full gear/save or normal admission acceptance.
Two full raw edits, whole6pose board,4/5/0/1neighbor seam board,4native pages,
normal/quarter browser proof inspected. Direct playback compares reportedV1
against repairedV2. Small face/hair/badge andheight+3variations remain provisional;
no continuously watched native/full-world foot or owner acceptance claim.
6Python syntax,1paired uniqueGDUID,{len(pngs)}PNG LFS. Preview:
http://127.0.0.1:8791/character/bill-east-run-master-v2/.
Normal selection unchanged; coherent family admission and East carry/torch
matching remain next. Full Bill objective incomplete; no commit/export.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for path in paths:
 with path.open('a',encoding='utf-8') as f:f.write(note)
handoff=f'''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: Bill running arm alignment

## Objective and acceptance
Repair owner-reported messed-up arm before continuing Bill master consistency.
Two backward-swing poses repaired; current bank remains unselected review version.

## Accepted decisions and constraints
Near shoulder patch must travel with a continuous arm, not attach to the chest.
Preserve matte finish, whole poses, original540ms/.168stride. No isolated arm
stencil or anatomical stamping. Reversible repair authorized; no commit/export.

## Current state
Two new whole raw edits in pose-000/005 with exact prompts/refs/receipts.
Four prior sources explicitly inherited; frames1/2/3/4 byte-identical toV1.
Manifest/4APNGs/source+arm-seam boards/native4pages/browser snapshots here.
V1 retains reported defect and now records supersession. Tools prepare/build/
publish/record_bill_east_run_arm_v2 and native_v3 reproduce current review.

## Verification
Source scale uniform; wholeY0/0/0/0/0/-1; heights+3/+1/+1/0/+1/+3,sole0all6.
Original7selectedinputs intact;24APNG decoded frames exact. NativeV3 75/0,
16pairs,54.93s,4962inputs and2931owner hashes unchanged,scratchAPPDATA.
Prescribed stationary phases/wrap/idlebeforeafter, NOT physical running route.
Both whole raws, six-pose and4/5/0/1arm boards, four native pages and browser
snapshots inspected; anatomy reads connected.6Python,1GDUIDpair,{len(pngs)}PNG LFS.

## Next action
Current arm correction available for review; carry8/torch6 master matching next.
Then moving run/family boundaries/admission, station jobs/save/TitleContinue and
remaining cardinal/equipment/water/life/hazard coverage. Small head/badge and
height variations provisional; full Bill objective remains incomplete.
'''
(D/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (A/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\nOctober4 owner reported arm defect; backward poses0/5 repaired in ../bill-east-run-master-v2/HANDOFF.md. V1 technical source checks remain historical; V1 anatomy not accepted.\n')
print(json.dumps(dict(newWholeEdits=2,unchangedFrames=4,nativeChecks=75,maintainedRecords=8,pngLFS=len(pngs))))
