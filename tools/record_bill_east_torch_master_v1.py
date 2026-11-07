"""Record scoped torch master consistency evidence and continuation."""
from pathlib import Path
import ast,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-torch-master-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((D/'native/validation.json').read_text());q=json.loads((D/'review.json').read_text())
assert v['passed'] and v['checks']==75 and v['captures']==16
assert all(sha(R/p)==s for p,s in q['protectedInputs'].items())
assert all(sha(R/p)==s for p,s in q['inputs'].items())
names=['prepare_bill_east_torch_master_v1.py','build_bill_east_torch_master_v1.py','prepare_bill_east_torch_native_v1.py','run_bill_east_torch_master_native_v1.py','prepare_bill_east_torch_native_v2.py','run_bill_east_torch_master_native_v2.py','publish_bill_east_torch_native_v1.py','record_bill_east_torch_master_v1.py']
for name in names:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
for version in [1,2]:
 uid=(R/f'tools/review_bill_east_torch_master_native_v{version}.gd.uid').read_text().strip()
 assert sum(p.read_text().strip()==uid for p in (R/'tools').glob('*.gd.uid'))==1
pngs=[p.relative_to(R).as_posix() for p in D.rglob('*.png')]
r=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R)
items=r.stdout.decode().split('\0');assert all(items[i+2]=='lfs' for i in range(0,len(items)-1,3))
findings='Six complete raws, all-pose source comparison, four native pages and normal/quarter browser screenshots inspected. Shoulder sleeve, elbow, cuff and torch grip remain connected. Matte quilting and warmer face approach the master. Small head/hair/patch, nozzle and flame-shape differences remain provisional; no exact pixel preservation or continuous native cadence claim.'
q.update(visualReviewed=True,reviewer='Codex',findings=findings,normalAdmission=False,syntaxChecks=8,pairedUniqueUIDs=2,pngLFSChecks=len(pngs),browserProof={n:sha(D/n) for n in ['browser-normal.png','browser-quarter.png']},failedNativeV1='Startup deferred method incorrectly renamed weld; zero captures. Concurrent grid_canvas.gd also changed during that freeze. Original failed fixture/report retained. V2 fixes only startup method, artwork unchanged.')
(D/'review.json').write_text(json.dumps(q,indent=2)+'\n')
note=f'''\n\n## Bill East torch master consistency — October 4, 2026

Prepared character/bill-east-torch-master-v1: six complete built-in image edits,
each retaining its prompt, three reference roles/hashes, raw source and receipt.
The selected source remains bill-torch-actions-v1/weld-east, previously accepted
for directional torch action. The new candidate restores master matte quilting,
hardware and warm face while maintaining a connected bent arm and East-facing tool.
Original six timings140/160/180/160/180/140 (960ms), loop, pivot128224 and H148
preserved. Uniform raw-to256 resampling and whole contact registration only;
heights+3/+1/+1/+1/0/+2, wholeY0/0/-1/-1/0/0, sole0all6. Seven selected inputs
unchanged. Four APNGs:24decoded frames verified exactRGBA/timing.

NativeV2 renderer evidence:75checks,0failures;16world/source pairs;{v['seconds']}s;
engine0/noERROR/WARNING. {v['inputCount']} frozen inputs unchanged, including exact
bank and fixture. Scratch APPDATA; {v['ownerNonLogCount']} owner non-log hashes
unchanged. All six source slots, loop wrap and master idle before/after verified
in the furnished ColdStore. These are prescribed fixed-foot phases, not a physical
repair/install job, tool draw/stow, autonomous goal, equipment/save or normal
admission acceptance. {findings}
FailedV1 retains wrong deferred startup method (zero captures) and concurrent
grid_canvas.gd freeze change. V2 repairs fixture startup only; artwork unchanged.
Eight Python syntax checks, two paired unique Godot UIDs, {len(pngs)} PNG LFS checks.
Preview: http://127.0.0.1:8791/character/bill-east-torch-master-v1/.

Next: exercise repaired East idle/walk/reach/run/carry/torch family boundaries
together and review admission, before further source expansion. Normal selection
is unchanged. Full Bill objective remains incomplete; no commit or export.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
(D/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: Bill East torch consistency

## Objective and acceptance
Continue Bill closeout by matching the East torch action to the master.
Six-pose candidate reviewed; owner acceptance and normal admission pending.

## Accepted decisions and constraints
Preserve connected whole figure, matte suit, warm face, East-directed torch,
original960ms timing and fixed contact. No anatomy stamping or per-pose stretching.
Reversible continuation authorized; no commit/export requested.

## Current state
Six raw edits, prompts/reference hashes/receipts; packed frames and manifest;
four APNGs, source board, four native pages and browser proof in this bank.
Eight torch-specific preparation/packing/native/publishing/recording tools.
FailedV1 fixture and report retained: startup method typo, zero captures; concurrent
grid change. V2 fixes only fixture startup. No artwork edited for a test pass.

## Verification
75/0 native checks;16pairs;{v['seconds']}s. {v['inputCount']} inputs frozen,
{v['ownerNonLogCount']} owner files unchanged, scratchAPPDATA. Seven old selected
inputs unchanged;24APNG decoded frames exact. Eight Python/twoUIDpairs/{len(pngs)}PNG LFS.
Whole-contact shifts0/0/-1/-1/0/0; original-source height differences0–3px.
{findings}
Prescribed stationary source phases only; actual job/tool lifecycle not exercised.

## Next action
Exercise repaired East family idle/walk/reach/run/carry/torch boundaries together,
then review coherent admission and actual jobs/save/title. Remaining cardinal,
equipment/water/life/hazard coverage stays open. Full Bill objective incomplete.
''',encoding='utf-8')
print(json.dumps(dict(nativeChecks=75,maintainedRecords=8,pngLFS=len(pngs))))
