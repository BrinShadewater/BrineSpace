# Bill locker identity study

Updated September 22, 2026. Broad repair goal remains active.

## Objective and constraints
Replace the mismatched older pickup/don/remove artwork with a coherent Bill
sequence. Preserve handoff timing, owner rooms and current standing endpoints.
One built-in image generation call; no Higgsfield, API fallback or publication.

## Current state
New source, exact prompt, registration and reproducible study builder:
character/major-bill-v3/sources/locker-identity-2026-09-22/.
Current source uses older pickup artwork followed by a separate donning pilot;
removal reverses the pilot and pickup. Both differ from current idle proportions.
The new eight-pose source supports two 12-frame sequences with unchanged event
indices. One scale (148/428), hard alpha, canonical palette and exact padded idle
endpoints. Runtime frames and canonical rebuild remain unchanged.

## Verification
output/bill-locker-identity-2026-09-22 contains source/candidate boards, 24 study
frames, validation.json, two native runs and four-quarter contact sheets.
All study frames have binary alpha, clear borders and exact second-build parity.
Native r2: exit 0, 739 travel samples, eight continuous action traces / 360 images,
fixed feet and completed equipment/return in all four rotations. Contact sheet
and native shelf crop inspected. This is a controlled injected preview, not an
installed or packaged regression. Exact selected-texture checks remain needed.

The initial interpretation that removal still used an old equipment row was
incorrect: grid_canvas._get_human_frame_source handles helmet actions through the
body action row before its ordinary equipment branch. R2 also replaced equipment
rows, but its sampled removal image exactly matches R1. Preserve both runs and
trace the actual selection path instead of inferring it from equipped state.

## Next action
Add selected-texture verification to the preview, finish shelf/endpoint review,
integrate the deterministic extraction in the canonical Bill rebuild, freeze
unrelated-art hashes, then validate installed native actions and reproducibility.
Review the shelf helmet size/appearance separately from character endpoint fit.
Owner motion acceptance and refreshed packaged acceptance remain open.
