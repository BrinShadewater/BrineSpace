# Project handoff

Updated: 2026-09-26 · BRINE facial readability and motion polish

## Objective and acceptance
Another polish pass on floating motion with readable facial details, retaining preferred v5/v6 likeness, palette, slim silhouette and scale.

## Accepted decisions and constraints
Head not enlarged; body export remains 45x139 and displayed height unchanged. New art edit targets local feature contrast and noise only. Preserve previous versions, tube, crew and owner saves.

## Current state
Imagegen facial cleanup from v6; exact prompt/provenance in production.json. build.py exports transparent body and hashes. Continuous rig now translates the head/face rigidly, removes differential hair/face deformation, and uses gentler limb lag with smooth spatial envelopes. Existing eight-second clock and power dimming retained. Shared preview launcher selects v7.

## Verification
Native body, full room screenshot and facial crops at four loop phases reviewed. Main facial marks remain distinguishable; face occupies only a small number of native screen pixels, so fine expression detail remains limited. face-review.png is a nearest-neighbor 6x diagnostic enlargement, not extra authored detail.

200 native samples at 25 fps and eight-second endpoint position/velocity continuity assertions passed. Face displacement equality checked throughout all 200 phases. No logged script errors; owner save fingerprints unchanged (session-f86432e0fa54442f9d4c1cd25ed8cd63). GIF uses fixed palette and 40ms frame timing. No direct visual claim of perfect smoothness: nearest texture sampling still yields small raster changes, and the existing bubble clock remains independently timed.

## Next action
Owner review of live preview and GIF. Production installation remains pending; original and previous revision assets untouched.
