from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;e=json.loads((P/'entry-review.json').read_text(encoding='utf-8'));m=json.loads((P/'matte-review.json').read_text(encoding='utf-8'));b=m['browserMotionReview']
assert m['unchangedFrames']==7 and e['decodedFramesExact']==9 and e['finiteLoopCount']==1
heading='Bill South whole crouch matte revisions and sampled motion — October 2, 2026'
body=f"""Sibling character/{P.name} preserves SouthV1 and replaces only complete early
and middle crouch source poses. Built-in edits exec-2b872392-7295-4782-b0a7-f484176f43f2
and exec-873cd810-05ea-463d-8dc1-02aa44a4beac; raw/exact prompts/ordered reference
hashes retained. No new state coverage; original seven authored intermediates,
exact padded selected idle/swim endpoints and five atlas action poses retained.
Nine-pose500ms bare study remains unselected. Existing runtime/owner profile untouched.

Frozen prior original-master anatomical source calibrations remain0.103547459 and
0.092943201, atlas.26. No per-pose occupied-height fit or anatomical fragments.
Early raw neutral-body diagnostic median76.67to64 (bounded neutral-body ROI, not
full material proof). Colour-only request changed early posture too: source opaque
crown42px higher, sole13px higher, roughly3native pixels taller at same density.
Accepted for further review as a complete reauthored candidate, never claimed as
pixel-preserved grading. Seven unaffected registered frames exact; nine decoded
APNG frames and all holds exact, finite loop1. Master-facing width/hardware/limb
segment and matte fidelity remain provisional despite matched hair scale proxies.

Actual source-browser normal/quarter Playonce exercised. {b['samples']}saved advancing
screenshots:33quarter observed labels1..8,6normal labels4..8; paused initial0.
AX label read before screenshot can cross holds; no source-phase pixel binding,
full normal chronology/duration or native contact proof. Fixed common screen crop.
Visual review: {m['visualReview']}

Lesson: material-only generative edit prompts do not establish pose/silhouette
invariants. Inspect actual opaque bounds and anatomical scale before adoption;
retain preceding source, use one frozen source density and evaluate full pose join
if geometry changed. Fewer reference images can reduce pose pull toward standing,
but still require verification. Contrast/raw median improvements cannot establish
complete master grading or smoothness. Scope sampled browser motion separately
from exact APNG decoding, native material/contact and owner acceptance.

Next remaining South shared master/detail/proportion/motion refinement, canonical
helmet and independently authored exit, native contact/guards/restore/Continue,
normal admission/cargo lifecycle and full cross-family polish. Entire Bill goal
active/incomplete. Review: character/{P.name}/index.html.
"""
entry='\n## '+heading+'\n\n'+body+'\n'
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
 with f.open('rb') as stream:stream.seek(max(0,f.stat().st_size-131072));tail=stream.read()
 if heading.encode() not in tail:
  with f.open('a',encoding='utf-8') as stream:stream.write(entry)
(P/'HANDOFF.md').write_text(f"""# Project handoff

Updated: October2,2026 · Project: {R} · Task: Bill South matte source revision

## Objective and acceptance
Full Bill animation set matching masters/camera/proportions/material then full-library
consistency and polish. Goal incomplete; candidate source/motion scope provisional.

## Accepted decisions and constraints
Complete early/middle generated source replacements, prior source scales frozen.
Seven unaffected frames and selected endpoints exact; no per-pose height fitting.
V1 sources and existing normal runtime/owner profile retained; no game access this turn.

## Current state
V2 build.py, nine bare frames/manifest/finite APNG, source prompts/raws/provenance,
matte-review.json, common-scale comparison, browser39screens/metadata/fixed-crop board.
Two whole material edits; no added states. AUTHORING.md links exact prompts/sources.
Six guidance files updated. No helmet or independent exit/native admission yet.

## Verification
Nine APNG RGBA frames/holds exact;loop1; seven unaffected frames exact.
{m['visualReview']}
Browser quarter labels1..8, normal partial4..8, initial0 paused; no phase binding.
No native/profile interval or full master/contact/motion acceptance in this turn.

## Next action
Remaining South master/detail/proportion/motion refinement, canonical helmet,
independent exit and native lifecycle/contact/restore/Continue; normal integration,
cargo lifecycle and full-library consistency/polish. Entire objective active.
""",encoding='utf-8')
print(json.dumps(dict(guidanceFiles=len(paths),frames=9,unchangedFrames=7,browserSamples=b['samples'],goal='active/incomplete')))
