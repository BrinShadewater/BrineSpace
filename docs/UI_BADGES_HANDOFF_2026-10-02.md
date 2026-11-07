# UI badges handoff

Updated: 2026-10-02 · Project: BrineSpace · Task: Additional matching badges

## Objective and acceptance
Continue creating badges matching the accepted muted, matte UI. Native-size audition delivered for owner visual review.

## Accepted decisions and constraints
Thin matte rims, petrol interiors, cream uppercase text and softened department paint. Preserve original icon artwork and existing simple badge API. Additive components only; actual state and ownership come from callers.

## Current state
New scripts/ui_badges.gd (+ paired UID): icon/label badge factory, optional inset count segment, compact 28px and standard 36px sizes, muted tone palette and department helper.
New tools/audition_ui_badges.gd (+ paired UID): room, crew, archive/research, alerts/counts, seven department tags and size comparison.
Preview: output/ui-badges-2026-10-02/badges-audition.png.
No live screen replacements in this pass.

## Verification
Godot 4.7.2 native audition: 98 checks, zero failures/errors, exit 0. Board reviewed at 1440x900: no clipping or overlapping captions. Count 0, omitted counts and 99+ cap checked. Scratch APPDATA; all 2,931 owner non-log files unchanged. Logs/guard: output/ui-integration-2026-09-30/ui-badges-audition.log and matching -verification.json. UID helper also isolated and clean.

## Next action
Owner visual acceptance pending. Apply accepted badges to relevant live screens on request, using existing game state; keep the simple badge factory for its current consumers.
