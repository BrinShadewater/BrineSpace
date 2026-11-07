# Bill west work identity study

Updated: 2026-09-21. Representative source study only; not installed.

## Objective and accepted constraints

Bring the west work body into agreement with connected-source walking and standing.
Preserve complete connected limbs, independent west art, character identity and
existing owner room layouts. Two built-in image_gen calls were used; no Higgsfield
or CLI/API fallback. This is not owner acceptance or completed animation coverage.

## Current state and findings

Sources/prompts/hashes live in
character/major-bill-v3/sources/west-actions-style-2026-09-21/.

First edit used the installed six-pose work source as target and canonical idle as
identity reference. It retained the bulky torso and simplified suit of the target.
`generated-source.png` is rejected; provenance records why. It must not be installed.

Second study used canonical idle alone and requested standing plus settled kneeling.
`pair-source.png` has a substantially closer face, fitted suit, shoulder insignia,
panel detail and boots. Pose silhouettes remain connected. Agent compared it at
the canonical 148-pixel standing height; it is a promising representative source,
not an approved animation. Work uses a two-handed cyan-tipped tool and differs
from the earlier arm pose. Tool clearance and motion must be checked if selected.

`review_pair.py` and `pair-registration.json` retain deterministic extraction:
alpha threshold128, standing box[304,72,570,935], work box[747,240,1340,935],
common scale148/863. The work frame is not independently normalized by height.
Review: output/bill-west-style-2026-09-21/same-scale.png, standing.png, work.png.
Raw alpha and generator outputs are preserved. No live frames/metadata changed.

## Verification and next action

Inspected both full generation results and the equal-scale canonical/study/current
comparison. Source files and exact prompts are saved locally. Technical registration
and pose fit are provisional; no native or release acceptance is claimed.

Build a connected six-stage lowering source with the successful pair as its sole
identity/style reference. Preserve body/helmet scale and planted boot through the
sequence; inspect crossings and endpoints before making work variants. Existing
work body remains live pending a complete, reviewed replacement. Keep this stage
separate from the already-installed walk and three-direction helmet corrections.
