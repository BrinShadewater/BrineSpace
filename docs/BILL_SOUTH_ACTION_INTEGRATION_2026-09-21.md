# Bill south action integration

Updated: September 21, 2026 · Project: BrineSpace

## Objective and acceptance
Repair the south-facing kneel/repair/stand identity mismatch while retaining current
walk art, source provenance, timing, pivots and equipment compatibility. Integrated
for playtesting; owner full-motion acceptance and other directions remain open.

## Accepted decisions and constraints
No Higgsfield. Two built-in source generations retained with exact prompts. No owner
room edits. Original source contract remains unchanged. Candidate history and native
reviews are in BILL_ACTION_SEQUENCE_2026-09-21.md.

## Current state
`tools/build_bill_south_actions.py` reconstructs selected source sheets from
`character/major-bill-v3/sources/south-actions-2026-09-21/`. The canonical rebuild
applies the 18 bare and 18 equipped action frames after its original source rebuild.
Kneel/repair endpoints match, stand reverses kneel, and one planted-boot slip is
corrected locally. Helmets use existing authored equipment. Exactly 36 PNGs changed;
all other generated files, clearance, catalogs and playback metadata are unchanged.

The rebuild encountered two write-open errors on different unchanged PNGs. Both
files remained readable and the first could be reopened for writing. Root cause is
not established. PNG output now skips byte-identical files and publishes changed
files via a temporary file and atomic replacement. This is per-file protection,
not a transaction over the entire art library.

## Verification
Canonical helper matched all 36 reviewed bare/helmet candidate frames exactly.
Full rebuild completed: 175 body states/1,134 frames, 168 equipment states/1,080
frames, 504 original source crops reproduced. Validator: zero errors/border touches,
780 original frames and 113 source manifests unchanged. Before/after hashes prove
only the intended 36 PNGs changed. PNG writer checks cover unchanged mtime, failure
preserving the original and cleaning the temporary file, and successful replacement.
Evidence: `output/bill-south-action-integration-2026-09-21/`.

Candidate native approach capture spans 224 frames including west walk to south
kneel; endpoint movement is about 0.28 world units. Equipped candidate capture spans
198 frames. Agent endpoint-board inspection passed the scoped fitting review;
neither capture establishes owner acceptance or all-direction coverage.

Installed-loader native confirmation also completed: 224 frames, zero failures and
no logged errors. Inspected the installed repair capture; all 36 live PNGs match the
reviewed candidate pixels. Evidence: output/bill-south-action-installed-2026-09-21.

## Next action
Continue animation and expedition review
from observed defects; existing Windows/Mac packages predate this integration.
