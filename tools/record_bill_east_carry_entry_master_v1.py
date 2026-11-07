from pathlib import Path
from PIL import Image
import json,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-carry-entry-master-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((D/'review.json').read_text());c=json.loads((D/'contract.json').read_text());v=q['nativeValidation'];assert v['passed'] and v['checks']==249
assert all(sha(R/p)==h for p,h in q['protectedInputs'].items())
for slot,source in [(0,c['pickup']),(4,c['carry']),(5,c['carry'])]:assert Image.open(D/f'frames/{slot:03}.png').convert('RGBA').tobytes()==Image.open(R/source).convert('RGBA').tobytes()
names=['prepare_bill_east_carry_entry_master_v1.py','build_bill_east_carry_entry_master_v1.py','prepare_bill_east_carry_entry_native_v1.py','run_bill_east_carry_entry_native_v1.py','run_bill_east_carry_entry_native_v2.py','publish_bill_east_carry_entry_master_v1.py','record_bill_east_carry_entry_master_v1.py']
for name in names:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
for version in ['v1','v2']:
 uid=(R/f'tools/review_bill_east_carry_entry_native_{version}.gd.uid').read_text().strip();assert sum(p.read_text().strip()==uid for p in (R/'tools').glob('*.gd.uid'))==1
pngs=[p.relative_to(R).as_posix() for p in D.rglob('*.png')];r=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R);items=r.stdout.decode().split('\0');assert all(items[i+2]=='lfs' for i in range(0,len(items)-1,3))
finding='Three whole intermediates visually match the repaired matte carry/warmer face. Height deltas0/1/0, wholeY1/0/2, all original whole-source bottoms retained. Exact whole pickup at0, exact gait0 at4/5. Original320ms entry and .104s production resume retained. Minor hair/patch/case hardware variation remains provisional; no rigid crate/hand-pressure proof. Other selected turns/cardinal banks and normal admission still separate.'
q.update(visualReviewed=True,findings=finding,pythonSyntax=7,pairedUniqueUIDs=2,pngLFS=len(pngs),generationCallsSHA256=sha(D/'generation-calls.json'),browserProof={n:sha(D/n) for n in ['browser-normal.png','browser-quarter.png']});(D/'review.json').write_text(json.dumps(q,indent=2)+'\n')
note=f'''\n\n## Bill East carry entry master match — October 4, 2026

character/bill-east-carry-entry-master-v1: three built-in whole image edits replace
entry1/2/3; six original320ms holds. Entry0 exactly shares repaired pickup10;
entry4/5 exactly share repaired carry0. Actual generation calls, prepared pose
contracts, four-reference hashes, receipts and raw1254square sources retained.
Uniform256 LANCZOS and wholeY only; no local grade, anatomy/prop stamps or pose
stretching. {finding}
Six normal/quarter APNGs validated:60decoded frames with repeated endpoint
coalescing; stationary source chain preserves .104s gait resume. All three raws,
complete six-slot comparison, two complete native boards and normal/quarter
browser snapshots reviewed. NativeV2:249checks0, all6holds plus actual gait resume,
7retained room/source pairs,26.22s,5,288inputs unchanged,2,936owner non-log files
unchanged under scratchAPPDATA, engine0/clean. Selected production actor/player
actually moves on a prescribed legal96-unit East floor segment at5ms steps.
Not natural workshop dispatch/turns, gear, Continue or normal admission.
SevenPython syntax/two paired uniqueUIDs/{len(pngs)}PNG LFS. NativeV1 fixture failed
on JSONfloat-versus-int Array equality and PackedVector2Array.assign; stopped and
maps retained (owner unchanged, concurrent room_content_canvas/room_asset_library
edits detected and preserved). V2 corrects only fixture typing/path construction
and expands freeze to all staged carry/cargo sources. No gameplay changes.
Next: judge remaining turn mismatches at actual station scale, repair only material
join defects, then coherent admission/save-resume. Owner wants closeout soon;
avoid redoing completed sources or expanding polish without demonstrated need.
Full Bill objective incomplete. Preview:
http://127.0.0.1:8791/character/bill-east-carry-entry-master-v1/.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
(D/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October4,2026 · Project: Brine Space · Task: Bill carry entry

## Objective and acceptance
Continue toward Bill closeout. East entry repair and moving proof complete,
provisional; no owner acceptance or normal admission inferred.

## Accepted decisions and constraints
Whole figure sources only; source timing/geometry retained. Exactly reuse
pickup10 at entry0 and carry0 at entry4/5. Existing reversible authorization.
No gameplay edit, commit/export or live-profile test. Keep concurrent room edits.

## Current state
character/bill-east-carry-entry-master-v1: three whole edits, six-slot manifest,
exact aliases, actual generation-calls/receipts/prompts/references/raws, provenance,
six verified APNGs, source comparison, two native boards and browser proof.
Seven tools and two paired native UIDs. All eight maintained records updated.

## Verification
249/0; selected production actor/player physically moves along prescribed legal
East segment, all6 entry holds then .104s gait resume.7retained pairs,26.22s;
5,288inputs/2,936owner files exact, scratchAPPDATA,engine clean.7Python/2UID/
{len(pngs)}PNG LFS. All raw/source/native boards and browser snapshots reviewed.
V1 fixture typing/path errors and two concurrent input edits retained, V2 passed.
Minor identity/case hardware variation provisional, no rigid-contact claim.

## Next action
Assess remaining carry turn mismatches at actual station scale. Repair only
demonstrated joins, then coherent admission and save/resume. Avoid repeated source
work or endless optional polish; owner wants wrap soon. Full Bill still incomplete.
''',encoding='utf-8')
print(json.dumps({'checks':249,'failures':0,'maintainedRecords':8,'pythonSyntax':7,'pairedUniqueUIDs':2,'pngLFS':len(pngs)}))
