# Project handoff

Updated: October 1, 2026 · Project: BrineSpace · Task: UI inset edges and layout refinement

## Objective and acceptance
Implement the owner's latest card, inspector, utility-control, icon, lighting and
automatic graphics requests in the game. Native rendering reviewed at 1600x900
and 1280x720. Owner visual acceptance of this revision remains pending.

## Accepted decisions and constraints
Keep illustrated gunmetal hull buttons and previous panel frames. Department paint
is an inset line underneath the metal; preserve room art and card content. Utility
hand controls and 1x/2x/4x return to simple frameless faces, with active speed fill.
Inspector card stays right; left shows placement/readiness or live status/location.
Avoid repeated base resources, build cost and description below the card.
Normal gameplay, portraits, saves and owner layouts retain their existing behavior.

## Current state
- `scripts/card_art.gd`, `draft_card.gd`, `main.gd`: visible inset paint, content
  margins 12px horizontal/10px vertical, department ribbon 24px with contained
  16px emblem. Paint retains department color even when unaffordable; selection
  lightens it. Smaller utility spacing and 40px control rows, 30px glyphs.
- `title_button_style.gd`: scoped plain utility styling. `ui_hull_style.gd`:
  blue catch light illuminates on hover and press. Door/action hulls retained.
- `main.gd`: Recenter inside View options/ZoomControls, resource icon brightness
  1.18, inspector contextual content and duplicate resource/story sections removed.
- `ui_icons.gd`, `brineui/hull-ui-v2/`: eight generated 128px transparent masters,
  full source atlas, registry and Godot remaps. Archived Data shared by resource UI.
- `exterior_lamps.gd`: independent 512px smooth radial halo; existing room halo art
  remains intact. `drone_animation.gd`: anti-aliased pulsing status lamp.
- `title_settings.gd`, `settings_panel.gd`: persisted Auto-detect graphics toggle
  under Display. Detects effects preset now and at startup using adapter name and
  CPU cores; manual Low/Medium/High disables it. Existing manual default retained.
  Hardware heuristic, not a performance benchmark or automatic resolution change.
- Fixtures: `test_hull_ui.gd`, `test_card_art.gd`, `test_ui_workspace.gd` updated
  for owner-requested behavior. No commit, export, upload or unrelated refactor.

## Verification
175 native UI checks, 34 card checks, title regression, UI workspace regression,
and two native gradient/hover-light checks pass, with zero final engine errors.
Native game captures and light comparison reviewed; new PNGs use Git LFS.
All runs use scratch APPDATA. Each final wrapper's strict real-profile guard
FAILED: 2,931 real non-log files fingerprinted; `last_session.json` changed during
concurrent live activity. Earlier failed UI assertion run also observed live loop
save/backup/report changes. Preserve original reports; no real file restored,
no retries just to obtain a clean interval, and no claim of unchanged live profile.
Initial stale fixture assertions (resource repetition, build-cost ordering) were
updated to this owner's instruction. Initial light assertion sampled the metal
instead of the catch; corrected to x14 at 2x density, original failed log retained.

## Next action
Owner review in game, especially inset edge strength, new utility glyphs and
inspector density. Automatic setting is available in Settings > Display and
starts off to preserve the current manual choice. No executable release produced.

Evidence: `output/ui-refinement-2026-10-01/`, with full original logs/guards in
`output/ui-integration-2026-09-30/ui-refinement-*`.
