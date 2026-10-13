# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: immediate atmosphere-mask invalidation

## Objective and acceptance

Resolve the first-frame completion discrepancy blocking private wall-cache visual
acceptance. Preserve selected default effects and continue the full PC/Mac release
performance plan; no overall FPS or release-certification claim.

## Accepted decisions and constraints

Update the atmosphere's occupied-cell mask when its footprint changes, including
same-count moves; skip unchanged image uploads. Keep current shader pixels, mask
format/dimensions, GPU texture identity and effects settings. No automatic quality
change or reduced effects. Actor/navigation/wall source behavior stays unchanged.

## Current state

Installed `scripts/screen_atmosphere.gd`: replaces eight-frame polling gate with
scene-local occupied-key snapshot equality/initialization; retains existing frame
counter and adds bounded upload counter. Existing script UID preserved. New
`tests/test_atmosphere_mask_invalidation.gd`/UID `uid://bmygl8vw5gpvy`, registered in
`tests/index.json`. Original source/installed hash retained in
`atmosphere-mask-normal-install/`. Wall-context helper remains private.

## Verification

Native per-frame probe showed clock, camera, zoom, pending layers, card layouts,
transition events and environment keys identical in the failing normal-only replay.
Explicit environment-pass repaint (V7) did not resolve the discrepancy. Source audit
found `ScreenAtmosphere._update_mask()` refreshed only when frame%8==1. The snow/post
effects could therefore use different footprint masks on the first completion frame.

Private immediate-mask V8 resolves it:23/23exact native comparisons. Installed source
V9 independently passes23/23:original15settled cases, plus visible rotation/wall
toggle/completed corridor/removal at first rendered and settled frames. Actual station
outside-snapshot neighbor metadata invalidation passes. Actual debug=false executable,
current accepted overlays, frozen clock, normal/global versus private/local walls,
muted secondary display. No FPS/motion/endurance/target1650/M1 certification.

Maintained regression: red reproduces2expected immediate-update failures with old
source; installed green5checks/0failures covers placement, same-count relocation,
removal,32unchanged calls with no new uploads, and ignored out-of-grid cells. New UID
engine-generated in isolated guard; existing UID preserved. Relevant source/index
whitespace check clean. The change removes idle mask uploads (formerly every8calls)
but whole-game performance gain has not been measured or claimed.

All native/headless full owner guards2,938unchanged; jobs terminal and shared runtime
configuration restored. Small overlays/metadata/native captures only, no full package
copies or publication. V6/V7 failures retained as attribution, V8/V9 accepted.

Evidence: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`retained-wall-native-edges-v6-state-control/`, `...-v7-env-sync/`, `...-v8-mask/`,
`...-v9-normal-mask/`, `atmosphere-mask-invalidation-trial/`,
`atmosphere-mask-normal-red/`, `...-green/`, `...-install/`.

## Next action

Keep this fix in future baselines. Finish private wall-cache motion/crew/light/fog
layering and scene-owner/context-release checks before admission; settled and visible
immediate mutation parity is now established within the tested scope. Continue
independent drone uploads, frame pacing, loading/memory, original bug/UI/save/endurance,
native target-PC/Mac certification and release freeze/audit/signing gates. No release.
