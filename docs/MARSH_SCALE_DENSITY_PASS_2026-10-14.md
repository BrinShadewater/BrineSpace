# Marsh size, density and polish pass

Updated: October14,2026 · BrineSpace · whole selected library

## Objective and acceptance

Owner accepted the remaining-animation review, asked whether the library is
covered and requested a size, pixel-density and polish pass. All228selected
states are accounted for. Current selection has1,198holds (the older1,190count
predates the four six-pose swimming loops). There are986unique source paths.
Owner can review the cross-family pass in
`character/marsh-scale-density-review-2026-10-14/review/index.html`.

## Accepted decisions and constraints

Preserve the accepted strokes, east-run registration, gestures, work, seated
poses, meals and cargo motion. Marsh remains sealed/helmet-free. Corner lounge
armchairs stay excluded. Compare natural anatomy and pixel detail using the
current directional idle references; do not resize crouching/prone/swimming
silhouettes to standing height. Canvas padding does not define body size.

## Current state and findings

- All228states declare standingHeight148; all1198holds fit their original
  canvases and the common review canvas after pivot registration. There are
  three pivot profiles and seven canvas sizes, appropriate to tools, loaded
  swimming, transitions and bunk poses. No missing or blank source image found.
- Every selected manifest specifies nearest sampling or inherits its nearest
  default. The runtime renderer uses nearest. At384world units per room, the
  standing ruler corresponds to65.28world units and2.267source pixels/world unit.
  Actual screen height follows the current720px base room, camera zoom and
  viewport scaling. The viewer's65.28px thumbnail is a reading aid, not a claim
  that every camera zoom displays that height.
- All15common-scale representative atlases inspected, covering one middle
  hold of every state against four idle references. Earlier reviews retain
  full motion coverage within their documented scopes. Here every hold receives
  numerical/pixel/registration checks; not every hold has fresh manual visual
  acceptance. Crouches and swimming foreshortening remain natural; no clear
  common-ruler size correction was identified in the representative review.
- Independently authored poses retain small shading/detail differences. Colour
  count and partial-alpha fraction are descriptive statistics, not measurements
  of anatomical size or proof of density mismatch. Most opaque cores in newly
  sampled drawings have alpha253vs255; preserve their antialiasing. Exploratory
  warm-colour connected components also join skin, gloves, collar and other
  regions and are not dependable head-size measurements. No automatic body/
  head scaling, palette reduction, alpha hardening or local anatomy patches.

No selected art, manifest, runtime code, timing or owner layouts changed in
this pass. `tools/audit_marsh_scale_density.py` freezes source contracts, measures
every hold and builds the review. `tools/marsh_scale_density_review.html` provides
all228clips, source/2× views, a same-scale directional idle reference, station-size
reading aids, pause/frame stepping and background controls. Original PNGs are
referenced directly, preserving pixels and alpha. Finite clips hold their final
frame before viewer replay, which is not an in-game action restart.

## Verification

`tools/review_marsh_scale_density.gd` checks the actual main scene's loaded
Marsh player: all1198frame pixels, clocks, loop flags, pivots and rulers against
the frozen selection. It captures fit/default/maximum allowed close zooms using
runtime idleSouth, eatSouth and carrySouth textures over current galley art.
These are prescribed texture scale comparisons, not autonomous NPC/furniture
placement, actual actor motion or all-actions native gameplay acceptance.

The first comparison fixture applied root viewport scaling twice when placing
CanvasLayer overlays. Its captures correctly exposed the review defect; they
are retained under `output/marsh-scale-density-2026-10-14/first-transform/`.
Corrected fixture supplies logical canvas coordinates and lets CanvasLayer apply
the viewport transform once. Fit/default/maximum zooms use actual allowed values.
No game art was changed in response to a capture error.
An intermediate corrected set overlapped the back counters; final overlays sit
on the open central floor. Intermediate files remain under `counter-overlap/`.
Final scale checks:4,071checks/zero failures; nominal standing screen heights
32.64px fit,45.35px current default and81.76px maximum close. Thus148px-source
standing detail already exceeds the largest normal game-screen ruler; wholesale
upscaling would not recover missing source detail or improve that calibration.

All1198local viewer frame links and durations resolve, generated JavaScript
passes Node syntax checking. Browser interaction has not been automated; those
checks do not claim a browser visual/UI test. Native screenshots are inspected
separately. All Godot invocations use isolated scratchAPPDATA, with owner profile
fingerprints before/after. Evidence and logs:
`output/marsh-scale-density-2026-10-14/` and the versioned review's `native/`.
All2,948owner non-log files remain unchanged. The audit rebuild rechecks every
source/manifest contract against the initial freeze.

## Next action

October15 continuation: the three semantic gaps below now have implemented
four-facing source sequences and bounded native integration checks. Owner visual
review remains pending; see [water actions handoff](MARSH_WATER_ACTIONS_2026-10-15.md).
The following diagnosis records why that follow-up was needed.

Later owner question exposed semantic gaps not represented by catalog counts:
the runtime swim-start/stop clips handle tread↔swim, not dry standing↔buoyancy;
only loaded airlock drainage has a water-clock rising sequence; empty-handed
drainage changes to dry idle without a dedicated settling clip. Underwater
expedition salvage reuses the standing tablet-work salvage pose. Dedicated
underwater working and empty-handed water-level transition art remain open.
The size/density checks above do not establish those actions are fully authored.

Owner reviews the common-scale viewer. No further mandatory artwork correction
was identified by this bounded pass. Broad route/hazard/release validation is
separate from complete selected-library source coverage. The earlier disclosed
historical shutdown rebaker mismatch remains outside this pass and is not a
claim of a newly failing selected animation. No export, commit or upload.
