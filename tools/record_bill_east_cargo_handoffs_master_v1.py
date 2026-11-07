"""Record the completed East cargo material repair and contextual work still open."""
from pathlib import Path
import json,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-cargo-handoffs-master-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((D/'review.json').read_text());v=q['nativeValidation'];assert v['passed'] and v['checks']==157;assert all(sha(R/p)==h for p,h in q['protectedInputs'].items())
names=['prepare_bill_east_cargo_handoffs_master_v1.py','build_bill_east_cargo_handoffs_master_v1.py','prepare_bill_east_cargo_handoffs_native_v1.py','run_bill_east_cargo_handoffs_native_v1.py','publish_bill_east_cargo_handoffs_master_v1.py','record_bill_east_cargo_handoffs_master_v1.py']
for name in names:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
uid=(R/'tools/review_bill_east_cargo_handoffs_native_v1.gd.uid').read_text().strip();assert sum(p.read_text().strip()==uid for p in (R/'tools').glob('*.gd.uid'))==1
pngs=[p.relative_to(R).as_posix() for p in D.rglob('*.png')];r=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R);items=r.stdout.decode().split('\0');assert all(items[i+2]=='lfs' for i in range(0,len(items)-1,3))
q.update(visualReviewed=True,reviewer='Codex',visualScope='All15 selected whole raws,17slot complete original/candidate boards, six complete native pages covering25slots plus idle, normal/quarter browser snapshots. No continuously observed native cadence claim.',browserProof={n:sha(D/n) for n in ['browser-normal.png','browser-quarter.png']},syntaxChecks=6,pairedUniqueUIDs=1,pngLFSChecks=len(pngs))
(D/'review.json').write_text(json.dumps(q,indent=2)+'\n')
note=f'''\n\n## Bill East master pickup/unload — October 4, 2026

Current review: character/bill-east-cargo-handoffs-master-v1. Fifteen unique
built-in whole edits cover pickup11/unload6, each original520ms/nonloop.
Shared original ground/held crate endpoints remain two exact whole aliases.
Uniform raw1254square->256 LANCZOS, only disconnected<=3px/maxalpha1 cleanup;
wholeY registration to each original complete-source bottom. No pose stretch,
local grade, head/body/crate stamp or invented pixel interpolation. Crouches keep
their own height. Unique height deltas1/0/1/0/0/0/-1/0/-1/1/0/0/-2/-1/0;
wholeY0/1/0/1/-8/0/1/1/1/1/1/1/2/1/0, bottom deltas0. The -8 shift registers
an entire correctly sized but lowered authored crouch, not a local body/foot edit.
Six first generation geometry mismatches retained with raws/receipts/prompts and
rejection notes: pickup1/4/8/9,unload3/4. Selected retries restore motion depth.
Ten normal/quarter APNGs verified against RGBA/clocks,150decoded frames including
lossless repeated endpoint coalescing; full pickup/carry/unload material sequence.

Native:157checks0,25source slots (pickup11,unload6,current carry8),27retained
ColdStore room/source pairs,{v['seconds']}s. Production workshop unload state and
action_elapsed used; pickup/carry explicit stationary phases. Exact endpoint
aliases, original clocks and loop/nonloop terminals pass. Engine0/clean;
{v['inputCount']}frozen inputs unchanged,29explicit protected originals/current
carry inputs, scratchAPPDATA and{v['ownerNonLogCount']}owner non-log files unchanged.
All15raws,17slot boards,six native pages,normal/quarter browser snapshots reviewed.
Six Python syntax checks,one paired uniqueGDUID,{len(pngs)}PNG LFS.

{q['findings']}
This closes the family audit's four darker East handoff source-repair TODOs,
alongside bill-east-torch-handoffs-master-v1. It does not close actual cargo/tool
dispatch/ownership/completion, moving contact, coherent admission or gear/save.
Normal selected bank remains unchanged; no owner acceptance inferred. Next:
exercise actual production jobs and moving carry with the repaired family together,
then coherent admission and remaining cardinal/equipment/water/life/hazard/save/
title review. Full Bill objective incomplete. Preview:
http://127.0.0.1:8791/character/bill-east-cargo-handoffs-master-v1/.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
(D/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October4,2026 · Project: Brine Space · Task: Bill East cargo handoffs

## Objective and acceptance
Match pickup/unload to repaired idle/carry. Source material repair and stationary
native review complete, provisional; no owner acceptance or normal admission.

## Accepted decisions and constraints
Preserve pickup11/unload6 at520ms each, crouch depth, attached hands and cargo grip.
Identical original endpoints share whole sources. Reversible work authorized.
No anatomy/prop stamps, per-pose stretching, commit/export or live profile tests.

## Current state
character/bill-east-cargo-handoffs-master-v1:15whole edits,17slots/two aliases,
prompts/references/raws/receipts/provenance/manifest,ten verified movies,source
boards,six native pages,browser proof. Six tools and paired fixtureUID. Six rejected
first sources retained. Normal selection unchanged; four East old material TODOs
now repaired across this bank and prior torch draw/stow bank.

## Verification
157/0,25slots,27pairs,{v['seconds']}s;{v['inputCount']}inputs and{v['ownerNonLogCount']}
owner files exact, scratchAPPDATA,engine clean. Production workshop unload clock;
other phases explicitly prescribed. 6Python/1UID/{len(pngs)}PNG LFS.
All selected raws,source boards,native pages and browser snapshots reviewed.
Minor hair/patch/case hardware variation provisional; no rigid-case/contact proof.

## Next action
Actual construction/tool and cargo jobs/moving contact using repaired banks together,
then coherent normal admission and remaining directional/equipment/water/life/
hazard/save/title coverage. Full Bill objective incomplete; no new source work
needed for the four old East material handoff TODOs unless review finds a defect.
''',encoding='utf-8')
print(json.dumps(dict(checks=157,remainingOldEastMaterialHandoffs=0,maintainedRecords=8,pythonSyntax=6,uniquePairedUID=1,pngLFS=len(pngs))))
