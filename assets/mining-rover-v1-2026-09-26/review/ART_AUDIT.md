# Mining rover art and animation audit

The owner-requested repairs are now recorded in [POLISH_CLOSEOUT.md](POLISH_CLOSEOUT.md).
The findings below describe the pre-repair audit; current metrics reflect the repaired pack.

Reviewed September 26, 2026 against the maintained visual bible, same-scale
Construction comparison, eight-heading light/dark board, loaded-direction board,
existing validation records and the live preview at normal/quarter speed.

## Result

Coverage is complete for review. Visual consistency is not yet ready for sign-off.
No artwork was regenerated during this audit.

| Area | Finding |
| --- | --- |
| Theme and perspective | Recognizable grounded four-wheel industrial rover in every heading. Charcoal, steel, exposed processing bay and front drill remain legible. No swimming/hovering motion introduced. |
| Palette and materials | Diagonals have brighter cyan and rounder, glossier highlights than the muted cardinal poses. NE/NW are the strongest outliers. Approximate cyan channel spread is 68–69 there versus 30–38 in cardinals; this supports the visual finding, not a color-acceptance test. |
| Detail density | Common 448-pixel canvas and .34 display scale are consistent. Authored detail density is not: diagonal tyre studs are larger and more widely spaced, and suspension/body details change between headings. Differences remain visible in the native-size insets. |
| Sizing | Overall scale relative to Construction is plausible. Axis-aligned bounds naturally vary with rotation and are not a reason to independently resize each heading. Full alpha bounds in south are 85.68 world units; the UI's 83.64 figure is nominal chassis registration, not total clearance. Gameplay clearance remains untested. |
| Rolling and transitions | Existing checks pass loop seams, exact inverse reverse and connected steering. Rolling frame zero changes 3,559–4,439 opaque pixels by more than eight channel levels from the static pose, with identical alpha. The rolling projection remaps tread even at phase zero. Travel-to-work can therefore change tread appearance despite correct braking and drill timing. A frozen wheel layer shared across travel/work is the preferred follow-up. |
| Cargo | Loaded ore sits in the central bay across all eight headings. Existing cargo endpoint/atlas checks pass. Complete-cycle preview reaches collection, loaded travel, unload and idle with deposited ore retained. |
| Light and power | Existing independent lamp/power checks pass; cyan wheel-side accents are baked artwork, distinct from the animated top light. Bright diagonal accents should not be mistaken for additional status lamps. |

## Evidence and limits

- `directions.png`, `construction-mining-scale.png` and `../completion/loaded-directions.png`: visual comparisons, including native-size light/dark views.
- `art-audit-metrics.json`: current pose bounds, approximate cyan measurements and rolling/static texture differences; reproduced with `python review/audit_registration.py` from the pack root.
- `final-validation.json`: existing unchanged-pack validation of 112 clips and 7,920 body/effect frame references, atlas parity, cargo joins, bounds and source hashes.
- `../tyres-v2/motion-validation.json`: existing tyre loop/reverse/steering checks.
- `movement-transition-checks.log`: existing controller checks, including braking, mine cancellation and cargo persistence.
- `art-audit-browser.png`: current driving viewport capture. The complete-cycle readout also reached idle / Cycle complete. Browser warning/error log was empty during this audit. Full-page captures intermittently cleared the canvas during capture resizing; viewport capture retained the rover. This capture limitation is not evidence of missing animation frames.

These are artwork/preview checks, not live-game acceptance. Continuous held-key
manual driving and gameplay clearance remain unverified. No Godot probe or owner
save access was needed because the chassis and scale were unchanged.

## Next polish pass

1. Match diagonal cyan, matte metal highlights and tyre stud size to the selected cardinal/Construction references, preserving geometry and registered scale.
2. Keep wheel appearance continuous between rolling, braked and work poses; check the joins at native size and quarter speed.
3. Rebuild only affected animation families and rerun their atlas/transition checks, then repeat the same visual comparison before sign-off.
