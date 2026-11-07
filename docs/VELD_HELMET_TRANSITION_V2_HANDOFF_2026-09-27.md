# Veld helmet fitting/removal study

Updated: September 27, 2026. Project: Brine Space.

## Objective and acceptance
Continue after owner accepted the matching helmet idles. Rebuild fitting/removal against current masters; owner explicitly stresses preventing lighter suit drift.

## Accepted decisions and constraints
Keep dark graphite, blue patches, silver fittings, neutral white lamp and anatomical equipment sides. Preserve body scale and author actual motion. Deterministic palette correction remains authorized. Existing runtime actions remain installed until a complete replacement is ready.

## Current state
`character/veld-helmet-transition-v2/` contains endpoint inputs, two raw videos, prompts, repeatable extraction/colour recipes and `fit-remove-review.gif`. The manifest contains 48 poses each for removal-to-hands and reverse fitting-from-hands. These are explicitly incomplete locker-action studies, NOT runtime equip/remove overrides. Source frames after98 are excluded: the helmet disappears instead of being physically returned to a locker.

Hailuo2.3Fast rejected end_image before submission despite family-level catalog support. Its start-only trial (4 estimated credits) changed the revealed hairstyle and retained the brighter helmet-master suit. Rejected. Hailuo2 Fast (`minimax-fast`,6 estimated credits) accepted both endpoints and preserved the low bun/silver streak better. Total generation estimate10 credits; both prompts used optimizer=false. See generation JSON for IDs and exact prompts.

## Verification
Raw second trial:142 frames, no source clipping. Fixed body-calibrated export184x208,pivot92,196,standingHeight148; no per-frame geometry rescaling.48 selected authored poses, reversed for fitting. Nominal removal2240ms/fitting2140ms, but these are partial-action studies, not complete game events.

The helmet reference's fixed shin fabric sample was RGB95,94,93.5 vs bare78,77,77. A neutral-midtone correction matches that reference sample while retaining bright silver and chromatic details. Second video varied around76–81. Small per-frame colour gains match the selected fabric sample to78,77,77 exactly. This is a diagnostic region, not proof of exact colour/material segmentation everywhere. Original source preserved. Export clipping0; contact sheets visually inspected. No game code or real save touched.

## Next action
Review the shortened lift/lower motion. Author a physically credible pickup/return join at the actual locker before installing. Check hairstyle and all suit regions at joins, particularly because previous helmet idles/walks still use the brighter uncorrected helmet master. Apply a consistent reviewed neutral-material correction to those candidates before coherent runtime integration. Do not silently replace approved bare pixels or install these partial study IDs as complete equipment actions.
