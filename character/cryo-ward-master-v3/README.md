# Cryo ward masters — September 30, 2026

Owner requested rebuilding the correct closed idle master and both broken pods
for art style, theme, density, relative size and consistency. **Staged master
review**, not installed animation. Prior live artwork and code remain unchanged.

Five true-alpha masters: two distinct broken human capsules with skeletons and
unlit inserts, occupied closed pet capsule, empty closed pet capsule, and empty
open pet capsule with the full door translated upward on rails. Quiet matte cream,
blue-grey seals, graphite upholstery and restrained cyan lights follow the selected
human chamber. Margot retains her tabby/white body and olive frog bonnet.

References by role:
- `character/cryo-layered-v1/closed.png`: selected medical material/casing family.
- `character/margot-polish-v1/sources/canonical-directions.png`: cat identity.
- `character/margot-v1/sources/pods-v2.png`: original encounter layout only in
  rejected first study; deliberately excluded from the cleaner redesign.

`sources/` preserves three generated originals and exact prompts. First study
retained as rejected for old scratch noise and lid construction. V2 establishes
the clean designs; V3 centres Margot and darkens failed human cyan inserts.
`masters/` contains isolated components. `frames/` packages 512px canvases,
pivot256,448 and common standingHeight148/linear sampling. Human closed height
264px (116.45 world units); pet closed height160px (70.57 world units). One frozen
scale per family; the raised door does not shrink the open chassis.

Rebuild: `python character/cryo-ward-master-v3/build.py`. Connected alpha components
and their dilated edge ownership remove exterior fragments. Raw sources remain
unchanged. Registration records source hash, bounds, scales and export hashes.
Five-component, nonclipping canvas, floor-pivot and transparent-corner assertions
passed. Raster paths covered by Git LFS. No Godot run or owner-save access.

Agent reviewed the source and density/scale boards. `master-review.png` shows the
five masters; `scale-review.png` is an honest static comparison with selected
Bill and Margot, not a gameplay capture. Master camera matches the accepted cryo
reference's elevated view; this is not evidence for a four-direction prop family.
Generated pet states have small casing differences. For the corrected animation,
use the closed empty chassis as authority and separately register its full door;
do not crossfade whole independently generated states or reintroduce an open start.

Next: owner master review, then corrected closed-to-open layering and native
found/repaired ward checks. No commit, export or runtime bindings changed.
