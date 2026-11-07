"""Record verified torch handoffs and remaining cargo matching work."""
from pathlib import Path
import json,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-torch-handoffs-master-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((D/'review.json').read_text());v=q['nativeValidation'];assert v['passed'] and v['checks']==156
assert all(sha(R/p)==h for p,h in q['protectedInputs'].items())
names=['prepare_bill_east_torch_handoffs_master_v1.py','build_bill_east_torch_handoffs_master_v1.py','prepare_bill_east_torch_handoffs_native_v1.py','run_bill_east_torch_handoffs_native_v1.py','publish_bill_east_torch_handoffs_master_v1.py','record_bill_east_torch_handoffs_master_v1.py']
for name in names:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
uid=(R/'tools/review_bill_east_torch_handoffs_native_v1.gd.uid').read_text().strip();assert sum(p.read_text().strip()==uid for p in (R/'tools').glob('*.gd.uid'))==1
pngs=[p.relative_to(R).as_posix() for p in D.rglob('*.png')];r=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R);items=r.stdout.decode().split('\0');assert all(items[i+2]=='lfs' for i in range(0,len(items)-1,3))
q.update(visualReviewed=True,reviewer='Codex',visualScope='Eight complete raw whole figures, both all-slot original/candidate/idle source boards, four complete native source/boundary pages, normal and quarter browser snapshots. No continuously observed native cadence claim.',browserProof={n:sha(D/n) for n in ['browser-normal.png','browser-quarter.png']},syntaxChecks=len(names),pairedUniqueUIDs=1,pngLFSChecks=len(pngs))
(D/'review.json').write_text(json.dumps(q,indent=2)+'\n')
note=f'''\n\n## Bill East master torch draw/stow — October 4, 2026

Current torch handoff review: character/bill-east-torch-handoffs-master-v1.
Eight built-in whole image edits replace the intermediate sources of two selected
six-slot520ms nonloop clips. Four endpoints reuse current idle/weld whole pixels
exactly (idle padded36,52 into256). Raw1254square uniformly packed to256;
height deltas+1/0/+2/+2/+2/+2/+1/+1, original intermediate sole deltas0;
wholeY0/0/-1/-1/-1/-1/-1/-1. No per-pose scaling, tone masks or part stamping.
Ten normal/quarter APNGs preserve RGBA/durations,106decoded frames including
lossless repeated-endpoint coalescing. Full material sequence idle/draw/weld/stow/idle.
Original selected bank remains unchanged; new candidate is unselected.

Native:156checks0,18source slots, five production construction timer boundaries,
25retained ColdStore world/source pairs,{v['seconds']}s. Production Bill
animation_state/action_elapsed verifies draw<.52, weld .52..9.48 and stow>=9.48.
Stationary prescribed timers/main disabled; not autonomous construction completion,
tool ownership, moving routes, gear/save or normal admission. Engine0/clean;
{v['inputCount']}frozen inputs unchanged,21explicit protected source inputs,
scratchAPPDATA and{v['ownerNonLogCount']}owner non-log files unchanged.

{q['findings']}
All eight raw images,both full source boards,four native pages and normal/quarter
browser snapshots inspected. Six Python syntax checks,one paired uniqueGDUID,
{len(pngs)}PNG LFS. Preview:
http://127.0.0.1:8791/character/bill-east-torch-handoffs-master-v1/.
This supersedes the family audit's torch draw/stow repair TODO only.
Pickup11/unload6 still need master matching; then real cargo/tool/moving lifecycle
and coherent admission. Other cardinal/equipment/water/life/hazard/save/title
coverage remains. Full Bill objective incomplete; no new owner acceptance inferred.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
(D/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October4,2026 · Project: Brine Space · Task: Bill East torch handoffs

## Objective and acceptance
Match old draw/stow to repaired idle/weld. Review bank and production clock/source
checks complete; provisional visual review, not owner acceptance or normal admission.

## Accepted decisions and constraints
Keep original520ms nonloop timing, whole figure anatomy and intermediate foot contact.
Exact current whole idle/weld endpoints; reversible work authorized, no commit/export.

## Current state
character/bill-east-torch-handoffs-master-v1: eight whole edits,12slots including
four exact endpoints. Prompts,references,raws,receipts,provenance,manifest,ten verified
movies,source boards,four native pages,browser proof. Six preparation/build/native/
publish/record tools and one paired fixtureUID. Normal selection unchanged.

## Verification
156/0 checks,18slots,five production timer boundaries,25retained pairs,{v['seconds']}s.
{v['inputCount']}inputs and{v['ownerNonLogCount']}owner files unchanged; scratchAPPDATA,
engine clean. Eight raw/all-slot boards/native pages/browser snapshots reviewed.
6Python/1UID/{len(pngs)}PNG LFS. Small hair/head/patch/tool variation provisional.
No autonomous completion, moving route, tool ownership or gear/save acceptance.

## Next action
Master-match pickup11/unload6 while preserving cargo/hands/contact/timing.
Then actual tool/cargo/moving lifecycle and coherent admission; remaining cardinal,
equipment,water,life,hazard,save/title coverage. Full Bill objective incomplete.
''')
print(json.dumps(dict(checks=156,remainingEastMasterHandoffs=2,maintainedRecords=8,pythonSyntax=6,uniquePairedUID=1,pngLFS=len(pngs))))
