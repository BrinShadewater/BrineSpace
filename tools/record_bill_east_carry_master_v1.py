"""Record the provisional carry bank and scoped native evidence."""
from pathlib import Path
import ast,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-carry-master-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((D/'native/validation.json').read_text());q=json.loads((D/'review.json').read_text())
assert v['passed'] and v['checks']==90 and v['captures']==20
assert all(sha(R/p)==s for p,s in q['protectedInputs'].items())
assert all(sha(R/p)==s for p,s in q['inputs'].items())
names=['prepare_bill_east_carry_master_v1.py','build_bill_east_carry_master_v1.py','prepare_bill_east_carry_native_v1.py','run_bill_east_carry_master_native_v1.py','publish_bill_east_carry_native_v1.py','record_bill_east_carry_master_v1.py']
for name in names:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
uid=(R/'tools/review_bill_east_carry_master_native_v1.gd.uid').read_text().strip()
assert sum(p.read_text().strip()==uid for p in (R/'tools').glob('*.gd.uid'))==1
pngs=[p.relative_to(R).as_posix() for p in D.rglob('*.png')]
r=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R)
items=r.stdout.decode().split('\0');assert all(items[i+2]=='lfs' for i in range(0,len(items)-1,3))
findings='All eight full raws, complete source comparison, five native pages and browser normal/quarter snapshots inspected. Near shoulder, elbow and glove form a connected arm holding the case. Small case hardware/corner, hair/face/badge variation remains provisional; pose3 has visible far-side fingers. No physical cargo route, pickup/turn/unload or owner acceptance claim.'
q.update(visualReviewed=True,reviewer='Codex',findings=findings,normalAdmission=False,syntaxChecks=6,pairedUniqueUIDs=1,pngLFSChecks=len(pngs),browserProof={n:sha(D/n) for n in ['browser-normal.png','browser-quarter.png']})
(D/'review.json').write_text(json.dumps(q,indent=2)+'\n')
note=f'''\n\n## Bill East carrying master pass — October 4, 2026

character/bill-east-carry-master-v1 contains eight complete built-in imagegen
edits, with exact prompts, three reference roles/hashes, saved raws and receipts.
Selected source is bill-carry-east-gait-v3/bare-manifest.json from the current
full closure. Matte suit detail and warm face restored against current idle and
original master. Whole raw resampling to256 and whole contact registration only;
no arm/head stamps, local grade or per-pose stretching. Height deltas0/1/0/1/0/2/1/2,
wholeY1/0/1/1/1/0/0/0, sole0all8. Original840ms/.12stride preserved, nine selected
inputs unchanged; four APNGs/32 decoded frames exactRGBA/timing.

Native carry player dispatch:90checks0,20world/source pairs,{v['seconds']}s,
engine0/noERROR/WARNING,{v['inputCount']}frozen inputs unchanged including exact
bank and fixture;{v['ownerNonLogCount']}owner non-log hashes unchanged, scratchAPPDATA.
All8sources, loop wrap and master idle before/after checked through the retained
furnished-room renderer. Prescribed stationary phases, NOT a physical cargo route,
pickup/turn/unload, autonomous job, save or normal-admission acceptance.
{findings}
6Python syntax,1paired uniqueGDUID,{len(pngs)}PNG LFS. Preview:
http://127.0.0.1:8791/character/bill-east-carry-master-v1/.
Normal selection unchanged. Next East torch6 master matching, then coherent family
boundaries/admission and real gameplay coverage. Full Bill objective incomplete.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
handoff=f'''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: Bill East carry master

## Objective and acceptance
Continue Bill closeout by matching the East carrying loop to the master.
Eight-pose bank prepared for review; owner acceptance and normal admission pending.

## Accepted decisions and constraints
Whole connected figures; matte suit and warm face; original840ms/.12stride.
No anatomical stamping or individual-pose stretching. Reversible work authorized.

## Current state
Eight raw edits, prompts/reference hashes/receipts, packed frames, manifest,
four APNGs, whole-source board, five native pages and browser proof in this bank.
Six carry-specific prepare/build/native/publish/record tools reproduce evidence.

## Verification
90/0 renderer checks,20pairs,{v['seconds']}s,{v['inputCount']}inputs and
{v['ownerNonLogCount']}owner hashes unchanged; scratchAPPDATA. Source height0–2px
above original, all soles aligned;32decoded APNG frames exact.6Python/1UIDpair/
{len(pngs)}PNG LFS. All raw/source/native pages visually inspected.
{findings}

## Next action
East torch6 master matching, then moving/family boundaries and coherent admission.
Continue station job/save/title and cardinal/equipment/water/hazard coverage.
Full Bill objective incomplete; normal selection unchanged; no commit/export.
'''
(D/'HANDOFF.md').write_text(handoff,encoding='utf-8')
print(json.dumps(dict(nativeChecks=90,maintainedRecords=8,pngLFS=len(pngs))))
