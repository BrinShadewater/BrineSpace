from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;e=json.loads((P/'entry-review.json').read_text(encoding='utf-8'))
assert e['decodedFramesExact']==9 and e['endpointExact'] and e['finiteLoopCount']==1
heading='Bill South authored water-entry source study — October 2, 2026'
body=f"""New character/{P.name} has nine320x352/p160224/H148 bare source frames,
finite500ms. Exact padded selected South dry idle and swim endpoints; seven new
complete intermediates from six-cell atlas (standing study+five actions), original-
master early crouch and original-master middle crouch. Three built-in generations,
exact prompts/ordered references/raws/hashes/execution identifiers retained.
Atlas exec-618c4264-bb20-4644-9063-27256558e2aa; early single
exec-d2f67ae8-e264-4ce6-bd02-e021c9d0d457; middle single
exec-d8e63537-4571-43b9-87c8-b70f958fae4a. Source-only unselected candidate.

Atlas uses existing South swim anatomical drawing density.26 across five poses;
standing ruler opaque span483 becomes125.58native, too short as148height authority.
Excluded ruler retained, not forced to148 by occupied-height scaling. Two same-
canvas master edits changed drawing density despite prompt: original semantic hair
component135, early149, middle166. Fixed complete-source scales0.103547459 and
0.092943201 follow original master148/1295 and hair component ratios; no posed
bounding-height/width fitting, limb rotations or fragmented anatomical replacement.
These hair proxies do not certify total head, hardware or limb-segment dimensions.

Initially reused selected South crouch002 widened notably between neighbours;
retained rejected-context-comparison.png, replaced with whole new middle pose.
Existing selected pose untouched. Nine APNG RGBA frames and holds decode exact,
loop1; exact padded idle/swim source pixels; no new Godot interval/owner profile
access. Native North results do not cover this South source bank.
Visual review: {e['visualReview']}

Lesson: same canvas dimensions and requested density are not generated invariants.
Use anatomical features and shared neutral/source scale comparisons; reject a short
neutral ruler instead of fitting every occupied pose to equal height. A previously
accepted whole pose can still break build/camera continuity with another family;
compare registered neighbours before reuse. Hair-colour connected components need
saturation/ROI protection against warm metal, and are diagnostics rather than full
proportion approval. Record reuse/rejection and new pose counts separately.

Next shared master matte/detail/head/segment and chronological pose-join refinement,
then South canonical helmet, independent exit, native contact/guards/restore/Continue,
normal admission/cargo lifecycle and entire-library consistency/polish. Full Bill
objective active/incomplete. Review: character/{P.name}/index.html.
"""
entry='\n## '+heading+'\n\n'+body+'\n'
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
 with f.open('rb') as stream:stream.seek(max(0,f.stat().st_size-131072));tail=stream.read()
 if heading.encode() not in tail:
  with f.open('a',encoding='utf-8') as stream:stream.write(entry)
(P/'HANDOFF.md').write_text(f"""# Project handoff

Updated: October2,2026 · Project: {R} · Task: Bill South water-entry source study

## Objective and acceptance
Full master-matched Bill animation set and final consistency/polish. Incomplete.

## Accepted decisions and constraints
Independent South artwork, complete figures, exact selected endpoints. Same fixed
atlas drawing density; two fixed source calibrations based on master anatomical
hair proxy, not occupied pose height. Full anatomical acceptance provisional.
Existing selected art/runtime/owner profile untouched.

## Current state
Three generated raws/exact prompts/provenance retained in sources; build.py
packages nine bare frames, manifest, finite APNG, registered whole sheet and review.
Seven newly authored intermediates; widened reused crouch removed/rejection retained.
Unselected candidate; no helmet/native/independent exit yet. Six guidance updated.

## Verification
Nine decoded APNG frames/holds exact; loop1; idle/swim padding byte-exact.
{e['visualReview']}
No native interval, profile access or production selection in this source turn.

## Next action
Master matte/head/segment/joins refinement and actual chronological review, South
helmet/independent exit, native lifecycle/contact/restore/Continue, normal integration,
cargo lifecycle and full-library consistency/polish. Full objective active.
""",encoding='utf-8')
print(json.dumps(dict(guidanceFiles=len(paths),frames=9,newWholePoses=7,sourceOnly=True,goal='active/incomplete')))
