# Project handoff

Updated: 2026-10-03 · Project: BrineSpace · Task: Kris transparent standing references

## Objective and acceptance
Continue owner-selected Cognitive Concordance Specialist / Intent Harmonisation
into four transparent static standing sources. Preserve hat-free likeness and
unique suit. Owner visual acceptance remains pending.

## Accepted decisions and constraints
Kris Krüg, AI & Robotics. Long beard, bold glasses, septum ring, tied hair,
asymmetric charcoal wrap/harness, pale collar, muted cyan left shoulder.
Flat right-hip wafer pouch replaces erroneous rear cylinders. Left-hip tablet.
No gameplay perk specified; no normal roster or actor selection changed.

## Current state
`source-atlas.png`: intact built-in transparent generation; exact `prompt.txt`
and reference/source hashes in `provenance.json`. Four candidate PNGs in
`rotations/`; 184×184, pivot(92,172), one front-derived scale0.1880559085.
Actual opaque heights south/east/north/west148/147/146/147. No per-view stretching.
`build_masters.py`, manifest, `review.png`, standalone `index.html`, validation
record, `package_review.py` and 8-file preview ZIP. No helmet or motion generation.

## Verification
Real RGBA alpha0–255, all four canvases decode, hashes match manifest, clear
canvas margins/no clipping. Agent reviewed raw atlas and native/enlarged board,
Bill/earlier-concept same-scale comparison and labelled historical room composite.
Beard/glasses, tied hair, wrap silhouette, subdued marks and correct wafer pouch
remain visible. South face/body still slightly three-quarter; precise cardinal
camera and motion compatibility remain unproven. No native runtime tests needed
for source-only work; real save folder untouched.

Initial extraction rejected alpha>0 bounds because near-transparent generator
speckles cross gutter boundaries. Corrected to whole-body alpha>32 bounds plus
3px margin; retained RGBA inside crop and intact raw source. No anatomy/RGB edit.
Pixel checks certify packaging, not body/animation/owner acceptance.

## Next action
First motion studies now exist in `kris-krug-motion-pilot-v1` and corrective v2;
all five completed sources remain unselected. Canonical-led east tablet keys in
`kris-krug-tablet-east-v1` are the next continuity foundation. Read their handoffs.

Use this identity/suit source to establish representative idle, walk and alignment
tablet action, refining front cardinal view before expanding all directions.
Select closest existing motion/body family by actual proportions and registration;
never replace the unique suit with another actor's default uniform. Helmet fit,
full action matrix, normal NPC behavior and station testing remain separate work.
Shared CURRENT_STATUS.md was previously581041392bytes, beyond patch read limit;
local handoffs record this milestone without rewriting that oversized document.
