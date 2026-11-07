# Room-facing repair handoff

Updated: September 12, 2026 · BrineSpace

## Objective and acceptance
Continue room-art improvements and correct confusing asset facings. Review actual
room rotations; preserve owner layouts and existing art sources.

## Accepted decisions and constraints
South-wall machinery faces inward and is viewed top-down. North banks sit flush
and overlap the riser slightly when overheight; side banks may be flush, with
every embedded appliance facing the center. Keep matte departmental
materials and sparse compositions. Preserve concurrent gameplay/character edits.

## Current state
Captured 47 current room identities and reviewed a six-room rotation comparison.
Integrated one Tidal Condenser south-wall top-down revision showing vessel lids
and pipework. The owner clarified the camera after a rear-elevation study; that
study is retained but no longer active. One earlier candidate also rejected.
[Source/provenance](../assets/room-facing-repair-v1/README.md).
Changed that active registration plus new art/provenance, the visual bible,
current status, the full-wall skill reference (installed mirror synced), and this handoff.
No owner layout changes, executable rebuild, commit, push or publication.

## Verification
Native south-room review complete; other three rotations pixel-identical in RGB.
Preferred layouts: 176 orientations pass crew collision and port routes.
Side-wall regression passes source hashes, library/state and saved-draft checks.
New PNGs have LFS filter coverage.
release must regenerate it against the final integrated checkout.
Review: `output/room-facing-2026-09-12/tidal-topdown-comparison.png`.

## Next action
Owner review of the top-down construction. Continue through remaining room
families; this bounded pass does not certify every asset facing. New native
captures and comparisons remain under `output/room-facing-2026-09-12/`.
