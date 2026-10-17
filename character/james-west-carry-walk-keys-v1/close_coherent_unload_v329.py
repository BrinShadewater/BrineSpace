from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1]
sheet=p/'north-unload-coherent-v327';endpoint=p/'north-unload-coherent-video-v328';motion=p/'north-unload-coherent-motion-v329'
inputs=json.loads((sheet/'generation-inputs.json').read_bytes())
for item in inputs['refs']:assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256']
inputs['preparationPromptSha256']=inputs.pop('promptSha256')
inputs['submittedPromptFile']='submitted-prompt.txt';inputs['submittedPromptSha256']=hashlib.sha256((sheet/'submitted-prompt.txt').read_bytes()).hexdigest()
inputs['generatedFile']='exec-5fad3b59-2b66-4b41-8ef9-add7e6e096be.png'
(sheet/'generation-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
review=json.loads((sheet/'review.json').read_bytes())
review['findings'].append('first row spills boots across equal cell boundaries; middle-row alpha heights include preceding-row fragments, not anatomical heights')
review['status']='rejected_before_native_scale_registration_cell_spill_and_stance'
(sheet/'review.json').write_text(json.dumps(review,indent=2)+'\n')
job=json.loads((motion/'generation.json').read_bytes())
assert job['task_id']=='448620884267478'
all_pngs=[f for folder in [sheet,endpoint,motion] for f in folder.glob('*.png')]
raw=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in all_pngs)
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=raw,cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
section='''### James coherent unload source and endpoint pilot — October 3, 2026

V327 built-in nine-pose whole-sheet trial preserves source refs/submitted prompt/raw.
Raw1254square inspected; whole uniform nearest to768 then equal256 cells, no fitting.
REJECTED before native: enlarged figures, altered row floor registration, boots
spilling into neighboring cells, deep/wide knees, coarse cloth. Cell alpha heights
242 include preceding-row fragments and are not anatomical measurements. All nine
source/endpoint comparison cells viewed. Do not fit each pose to disguise this.

V328 endpoint pilot edits whole original turn endpoint to arms-down/case-floor,
preserving narrow stance. Raw and corrected three-column H148/82/54/27 review
viewed. Turn bounds96,76,159,224; trial94,75,161,224; current final97,76,160,224.
Candidate crown1up, sole unchanged,4px broader overall. Body/gear pixels redrawn;
case broad/outside boots and original-master material still provisional/unselected.
Endpoint geometry qualifies only for a temporal study, not adoption.

V329 direct Hailuo02 first/last trial submitted exactly once, task448620884267478,
6s768P, estimatedUSD0.28/billing unverified. Equal768whole3x sources on flat48,59,64;
exact old turn entry and provisional328end, prompt/input hashes retained. Inspect
generation.json/provider poll for current authoritative status, not this note.
Normal sources/controllers/saves unchanged; no native runs. Full goal incomplete.

Lesson: generated row topology can invalidate deterministic equal slicing before
motion review. First/last video constraints must use compatible support/stance;
the old final endpoint already widened boots, so it was not submitted unchanged.
Review the whole temporal source, case placement and master fidelity before any
helmet extension, normal admission or retiming; retain rejected trials.
Handoff: character/james-west-carry-walk-keys-v1/north-unload-coherent-motion-v329/HANDOFF.md.
'''
guides=record_guides(r,section,'### James paired arrival pacing diagnosis — October 3, 2026')
handoff='''# Project handoff

Updated: October 3, 2026 · James coherent North unload repair

## Objective and acceptance
Full James set following original masters and whole-family consistency/polish.
Current studies are provisional; full goal active, no external blocker.

## Accepted decisions and constraints
Master material/proportions, fixed support, belt wrench, tablet diagnostics and
forward torch. No normal adoption until complete motion/source fidelity review.

## Current state
327 nine-cell sheet rejected for scale/floor/cell spill/stance. 328 whole endpoint
pilot arms-down/case-floor, close crown/sole registration, pending prop/material.
329 first/last Hailuo02 job448620884267478 submitted exactly once. Read provider
status via tools/minimax_video.py poll --output this folder; never blindly resubmit.
Sources/prompts/raw/results/review helpers and five guides retained. Normal art,
controllers and owner saves unchanged. No native runs.

## Verification
327 refs unchanged; raw/full comparison viewed. 328 raw and all three sources
H148/82/54/27 viewed. Original turn endpoint versus new sole224/crown75 vs76.
Bounded inputs/hashes and LFS attributes checked. Endpoint geometry is not prop,
material, anatomy or full motion acceptance. Estimated jobUSD0.28, unverified bill.

## Next action
Poll SAME job, retain entire downloaded source. Review complete bend/rise and floor
case against master/entry/exit, no per-frame fitting/regrading or omitted failures.
Only then matching helmet and normal integration if source fidelity warrants it.
Carry/turn/all-family consistency and ordinary gameplay/interruptions open.
'''
(motion/'HANDOFF.md').write_text(handoff)
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
print(f'Recorded rejected sheet, provisional endpoint and same live video job; {len(all_pngs)} LFS PNGs, {guides} guides.')
