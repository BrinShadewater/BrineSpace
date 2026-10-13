"""Record the combined family audit without implying normal admission."""
from pathlib import Path
import json,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-family-review-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((D/'review.json').read_text());v=q['nativeValidation'];assert v['passed'] and v['checks']==374
assert all(sha(R/p)==h for p,h in q['protectedInputs'].items())
names=['build_bill_east_family_review_v1.py','prepare_bill_east_family_native_v1.py','run_bill_east_family_native_v1.py','prepare_bill_east_family_native_v2.py','run_bill_east_family_native_v2.py','publish_bill_east_family_review_v1.py','record_bill_east_family_review_v1.py']
for name in names:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
for version in [1,2]:
 uid=(R/f'tools/review_bill_east_family_native_v{version}.gd.uid').read_text().strip()
 assert sum(p.read_text().strip()==uid for p in (R/'tools').glob('*.gd.uid'))==1
pngs=[p.relative_to(R).as_posix() for p in D.rglob('*.png')]
r=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R);items=r.stdout.decode().split('\0');assert all(items[i+2]=='lfs' for i in range(0,len(items)-1,3))
q.update(visualReviewed=True,reviewer='Codex',visualScope='First/middle/last source comparison for all10banks, ten complete native boundary pages, normal/quarter browser snapshots. Earlier raw/full-pose reviews remain in each repaired bank. No continuously observed native cadence claim.',browserProof={n:sha(D/n) for n in ['browser-normal.png','browser-quarter.png']},syntaxChecks=7,pairedUniqueUIDs=2,pngLFSChecks=len(pngs))
(D/'review.json').write_text(json.dumps(q,indent=2)+'\n')
note=f'''\n\n## Bill East combined family audit — October 4, 2026

character/bill-east-family-review-v1 compares six repaired banks (idle72,
walk48, interact6, run6, carry8, weld6) and four existing handoffs (pickup11,
unload6, torch-draw6, torch-stow6):175total source slots and183protected source
inputs. No new artwork, resampling, recolouring or source manifest changes.
Preview pads whole figures only to common256/p128224/H148. Twenty normal/quarter
movies verified against original RGBA and durations, allowing lossless repeated
frame coalescing; direct idle/action/idle timelines are material comparisons,
not authored tool/cargo appearance/disappearance.

NativeV2:374checks0,175source slot identities,50retained room/source pairs,
{v['seconds']}s;engine0/noERROR/WARNING. {v['inputCount']} frozen inputs unchanged,
including combined review,183source files/manifests and exact fixture. Scratch
APPDATA;{v['ownerNonLogCount']}owner non-log hashes unchanged. All10banks loaded
together with snapshots of their exact rows before later manifests can override
them; each loop wraps, nonloop holds terminal and each returns to current master
idle. Explicit stationary source phases, NOT actual autonomous transitions,
physical run/carry routes, tool/cargo lifecycle, gear/save or normal admission.
V1 retained374/13 failed checks from fixture incorrectly truncating torch-draw
and torch-stow to torch; V2 preserves full state names, artwork unchanged.

{q['findings']}
Source first/middle/last boards, all10native pages and normal/quarter browser
snapshots reviewed. Seven Python syntax checks,two paired uniqueGDUIDs,
{len(pngs)}PNG LFS. Preview:
http://127.0.0.1:8791/character/bill-east-family-review-v1/.
Next narrow scope: master-match four existing pickup/unload/torch-draw/torch-stow
handoffs, preserving selected motion/contact; then real lifecycle/moving and
coherent admission. Normal selection unchanged; full Bill objective incomplete.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
(D/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: Bill East combined family

## Objective and acceptance
Check the repaired East family together before expanding sources or admitting it.
Combined technical/visual audit complete. Four old handoffs still need matching.

## Accepted decisions and constraints
Preserve all existing source pixels, timing, profile and selected metadata.
Reversible review work authorized. No normal admission/commit/export this turn.

## Current state
Ten unchanged source banks,175slots,183protected inputs. Six repaired banks plus
selected pickup/unload/torch-draw/torch-stow. Twenty review movies, five direct
idle/action/idle timelines, source boards, ten native pages and browser proof.
Seven build/native/publish/record tools, paired V1/V2 fixtures and UIDs.

## Verification
NativeV2 374/0,175slot identities,50pairs,{v['seconds']}s;{v['inputCount']}inputs
and{v['ownerNonLogCount']}owner hashes unchanged,scratchAPPDATA. V1 374/13 fixture
name-truncation failures retained; V2 corrected full multiword state names only.
No continuous native cadence, actual controller lifecycle or moving route claim.
All source sample boards/native pages/browser snapshots inspected;7Python/2UIDs/
{len(pngs)}PNG LFS. {q['findings']}

## Next action
Match four old handoffs to master: pickup11,unload6,torch-draw6,torch-stow6.
Keep genuine cargo/tool contact and whole-frame anatomy, preserve motion.
Then real lifecycle/moving boundaries and coherent admission, followed by remaining
cardinal/equipment/water/life/hazard/save/title coverage. Full Bill incomplete.
''',encoding='utf-8')
print(json.dumps(dict(checks=374,remainingHandoffs=4,maintainedRecords=8,pngLFS=len(pngs))))
