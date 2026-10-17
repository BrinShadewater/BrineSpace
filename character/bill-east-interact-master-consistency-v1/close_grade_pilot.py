from pathlib import Path
import json,hashlib,ast,subprocess
R=Path.cwd();P=R/'character/bill-east-interact-master-consistency-v1';B=P/'grade-pilot-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((B/'provenance.json').read_text())
for path,h in q['frozenInputs'].items():assert sha(Path(path))==h,path
for r in q['references']:assert sha(Path(r['path']))==r['sha256']
assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256']
assert sha(Path(q['originalPath']))==sha(B/'raw.png')==q['sha256']
(B/'job.json').write_text(json.dumps(q,indent=2)+'\n')
v=json.loads((B/'review.json').read_text());assert sha(B/'comparison.png')==v['comparisonSha256']
v.update(visualReview='Raw and corrected non-overlapping four-column board actually inspected at native density and H82/54/27. Pilot reduces cheek/hair and hardware highlights, but makes face duller than original master. Suit remains detailed and somewhat brighter than current idle. Grade seam reduced, master fidelity not settled.',decision='Do not expand this grade pilot; retain diagnostic/unselected. Prior warmer master-consistency family remains provisional. Repair legacy idle coherently toward original master before whole-family admission.',fullVisualAcceptance=False)
(B/'review.json').write_text(json.dumps(v,indent=2)+'\n')
report=json.loads((P/'family-review.json').read_text());count=0
for path,h in report['frozenInputs'].items():assert sha(Path(path))==h,path;count+=1
a=json.loads((P/'native/corrected-source-audit.json').read_text())
for path,h in a['candidateClosureBindings'].items():assert sha(R/path)==h,path;count+=1
for p in [P/'prepare_grade_pilot.py',P/'save_grade_pilot.py',P/'build_grade_pilot.py',P/'record_native_milestone.py']:ast.parse(p.read_text())
files=[str(x.relative_to(R)).replace('\\','/') for x in P.rglob('*.png')];r=subprocess.run(['git','check-attr','filter','--',*files],text=True,capture_output=True,check=True);assert all(x.endswith(': filter: lfs') for x in r.stdout.splitlines())
lesson='''\n\n## Bill East grade pilot: master authority versus legacy seam — October 3, 2026

One built-in whole-figure extended-arm grade edit binds exact previous candidate,
original East master and current idle, raw output copied with prompt/input hashes.
Common352 target nearest4x; whole raw1254 uniformly resampled then184 returncrop,
no source recolor/splice/anatomical fit. Bounds[136,76,224,225] to[136,76,225,225],
body IoU .97479, zero opaque overflow. Raw and four-column density/head board
actually inspected. Cheek/hair/hardware subdued, but face duller than master.
Do not expand/admit this pilot. Earlier warm detailed six-pose study remains
provisional; current idle itself needs coherent master-consistency repair.

Lesson: continuity to an older selected asset is a supporting constraint, not a
replacement for original-master authority. Reducing a seam by dulling improved
identity can move away from the requested full-set result. Preserve rejected
whole-pose studies and compare master, ownidle and action together at physical
scale; geometry checks cannot establish correct color or facial character.
Evidence:character/bill-east-interact-master-consistency-v1/grade-pilot-v1/.
No native run for this new pilot, no normal selection, commit or export.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:
 for name in ['crew-consistency.md','source-density.md']:paths.append(root/'references'/name)
for path in paths:
 with path.open('a',encoding='utf-8') as f:f.write(lesson)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-03 · Project: Brine Space · Task: Bill East master consistency

## Objective and acceptance
Full Bill animation library faithful to original masters, style, perspective, size, proportions and matte grade; cross-family polish and normal gameplay verification. Goal active/incomplete.

## Accepted decisions and constraints
Original master remains identity/material authority. Existing selected assets/runtime unchanged. Whole-pose built-in edits; uniform canvas packaging only. H148/pivot92,172/184canvas. Native probes isolated in scratch APPDATA with owner fingerprints. No commit/export.

## Current state
Five independent edits plus exact derived endpoint make six-slot provisional East interaction family. Native staged-player V3 reviewed. New grade-pilot-v1 has one complete extended-arm edit, exact provenance/raw/prompt, candidate and four-column comparison. Grade pilot is diagnostic, not a replacement: it makes face duller than master. Earlier warmer family stays provisional. Current idle needs coherent master-consistency repair.

## Verification
Native V3:53 checks/0failures, six source captures at H148/82/54/27, exact source/cursors/restores/finite return.3303inputs and2931owner non-log files unchanged in native interval. Three native pages/current context inspected. No world contact/natural actor/cadence/Continue acceptance. Inherited26manifest loads correct actual normal inventory216bare/198helmet; older212/194literal audit and lifeRows remain historical/limited. New grade pilot IoU.97479,bounds right edge+1px,zerooverflow; raw/board inspected. Frozen family and inherited closure inputs rechecked, Python AST/PNG LFS checks pass. Native result does not cover new grade pilot.

## Next action
Evaluate full current East idle breathing sequence against original master and six-slot interaction endpoints; preserve breathing cadence/geometry while repairing identity/material coherently. Then actual actor/contact joins. West48phase heads, canonical helmet/water sources, other directions/life actions/natural hazards/checkpoint/titleContinue and whole-set polish remain open. No blocker.
''',encoding='utf-8')
print(f'{count} family/closure input hashes stable;4 Python AST;{len(files)} PNG LFS. Pilot review, six guidance references, two project records and handoff saved.')
