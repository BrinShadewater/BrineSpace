from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
R=Path.cwd();P=R/'character/bill-east-idle-master-consistency-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();a=json.loads((P/'source-baseline.json').read_text());v=json.loads((P/'validation.json').read_text());assert sha(P/'density-review.png')==v['densitySha256'];v['densityVisualReview']='Current0/18/36 plus originalmaster/action at H148/82/54/27 inspected. Warm detail retained; not full seven-phase density or continuous loop acceptance.'
comparisons=[]
for i,j in [(0,1),(35,36)]:
 for family in ['selected','new']:
  paths=[R/a['rows'][slot]['path'] if family=='selected' else P/f'candidate-frames/{slot:03}.png' for slot in [i,j]];x,y=[np.array(Image.open(p).convert('RGBA')).astype(float) for p in paths];comparisons.append({'pair':[i,j],'family':family,'alphaMaskChanges':int(((x[:,:,3]>127)!=(y[:,:,3]>127)).sum()),'premultipliedMeanAbsoluteRGBChange':float(np.abs(x[:,:,:3]*x[:,:,3:]/255-y[:,:,:3]*y[:,:,3:]/255).mean())})
v['adjacentSourceDiagnostics']=comparisons;v['generationIds']=[json.loads(p.read_text())['generationId'] for p in sorted(P.glob('provenance-*.json'))];assert len(set(v['generationIds']))==7
for file,h in v['protectedInputs'].items():assert sha(R/file)==h,file
v['allCurrentCrownSoleBoundsMatchSource']=all(m['beforeBounds'][1::2]==m['candidateBounds'][1::2] for m in json.loads((P/'review.json').read_text())['metrics']);assert v['allCurrentCrownSoleBoundsMatchSource'];(P/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
lesson='''\n\n## Bill East idle seven-pose expansion and endpoint registration — October 3, 2026

Five new independent whole-pose edits0/1/9/27/35 extend18/36 to7of37unique
breathing poses. A peak-rendering reference plus original master and exact target
replaces the earlier derived endpoint; previous3pose evidence archived intact in
key-pose-evidence-v1. New start and all seven candidates match original crown/sole
bounds, resolving prior seed1pxverticaldifference without local anatomy fitting.
Sidebound0or-1px;bodyIoU.97779-.98790,zerooverflow. Warm angular face/quilt/hardware
more coherent across phase and interaction study. All raws/both full comparison
pages inspected;0/18/36/master/action H148/82/54/27 board reviewed.277normal idle/
inherited closure inputs stable;7exact targets and raw-copy equalities,6Python AST/
34PNG LFS pass. No native/profile run or selection change. Full72slot/3000msloop
still absent;30unique phases remain. Neighbor0/1and35/36pixel diagnostics retained,
not a continuous cadence certificate.

Lesson: retain prior derived provenance when independently reauthoring an endpoint;
current coverage must count actual generation receipts, not the historical seed.
Match unchanged contact to original targets, compare adjacent phases as well as
extremes. Crown/sole equality does not establish anatomical phase amplitude or
worldcontact. Do not silently reduce37unique phases to a few held poses. Full
Bill scope remains active; next missing phases/full loop/interaction join, native
actor contact/cadence and full-library cross-family polish.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:
 for name in ['crew-consistency.md','source-density.md']:paths.append(root/'references'/name)
for path in paths:
 with path.open('a',encoding='utf-8') as f:f.write(lesson)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-03 · Project: Brine Space · Task: Bill East idle master consistency

## Objective and acceptance
Full Bill library faithful to original masters, style/perspective/physical size/proportions/matte grade; complete cross-family polish and normal runtime verification. Goal active/incomplete.

## Accepted decisions and constraints
Original master is identity/material authority. Existing normal assets/runtime unchanged. Built-in whole-pose edits with exact prompt/raw/input hashes; uniform packaging only. H148/p92,172/184canvas; original3000ms breathing cycle preserved as authoring target. No anatomy fit/part splice/source recolor. Scratch APPDATA and owner fingerprints required for future Godot runs.

## Current state
Seven independently authored poses0/1/9/18/27/35/36 of37unique phase sources. Original72slot duplicate groups frozen, current loop not yet packaged. New0 replaces historical derived endpoint; old reviewed3pose evidence and seed provenance preserved in key-pose-evidence-v1. Peak-rendering reference aids new neighboring phases. Sources/prompts/jobs/provenance, candidate-frames, complete review pages, master/action density board,review.json,validation.json. No complete manifest/partial runtime loop/normal selection.

## Verification
All seven raws and both full selected/new/master/action review pages inspected. Warm face/quilt/hardware closer to master and coherent. Every crown/sole bound matches selected original;sideedge0or-1px,bodyIoU.97779-.98790,zerooverflow.0/18/36/master/action density H148/82/54/27 inspected. Neighbor pixel differences saved; no continuous loop/anatomical phase amplitude/native contact acceptance.277normal idle/inherited closure inputs unchanged,7exact target reconstructions/raw-original copies,7distinct generation IDs,6Python AST/34PNG LFS. No native/profile run this interval; prior interaction53checks separate.

## Next action
Author30missing unique phases with exact phase target/master/peak-render reference, inspect adjacent material/body changes, derive exact duplicate slots, build full72slot/3000msloop and idle/interact joins. Native actor floor/contact/cadence before selection. West48phase heads, canonicalhelmet/water, other cardinal/life sources, natural hazards/checkpoint/TitleContinue/full-set polish remain. No blocker/commit/export.
''',encoding='utf-8');print(json.dumps({'authoredUniquePoses':7,'remainingUniquePoses':30,'allCrownSoleMatch':True,'adjacentDiagnostics':comparisons,'guidanceAndProjectRecords':8}))
