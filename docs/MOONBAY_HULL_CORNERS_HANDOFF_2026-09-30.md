# Project handoff

Updated: 2026-09-30 · Project: BrineSpace · Task: Full submerged sub and wall-top corners

Latest owner correction: corner caps should blend seamlessly with the walls. The separate shaded plates, dark diagonal seams and extra fasteners were replaced by mitered crops of the actual horizontal/vertical engineering wall skins, at the same texel scale and top registration. Only Moonbay's corner drawing and its card changed. Four native rotation views reviewed; scoped Moonbay baker exits zero and whitespace check passes. Scratch-profile fingerprints show zero changes across 2,924 owner files. Evidence: output/moonbay-seamless-corners-20260930/. This supersedes the plate/fastener styling below; hull and pressure behavior remain unchanged. Reload source for owner review.

## Objective and acceptance
Owner accepted the pressure layout, then reported a missing lower sub hull and excessive transparency and requested wall-top corner pieces. Corrected and reviewed in native room/station captures; owner hands-on visual acceptance remains open.

## Accepted decisions and constraints
Keep the full sub silhouette solid under water with a restrained blue tint. The bay remains permanently flooded and the pressure/door cycle is unchanged. Add fitted matte corner plates to the Moonbay bay, airlock and outer hull wall tops, with miter seams and recessed fasteners. Preserve all floor contacts, collision and doorway geometry.

## Current state
rooms/large-rooms/common.gd accepts an optional underwater modulation while preserving the existing default for other equipment. Moonbay uses opaque RGB (0.78,0.90,0.92); the old 28% underwater alpha made the lower hull nearly disappear. rooms/large-rooms/moonbay.gd draws bay water before the sub to avoid double tinting and adds registered procedural corner caps. scripts/moonbay_missions.gd uses the same solid modulation for launch/return docking. assets/large-room-cards/moonbay.png rebaked through the maintained native baker. Source artwork unchanged.

## Verification
Godot 4.7.2 large-room art and revision checks PASS. Native alpha comparison checks all four rotations: zero missing opaque hull pixels; negative control using the original fade rejects 3,076–10,388 pixels per rotation. Four native room rotations and fourteen station mission views refreshed. Reviewed all four room orientations plus station gate-opening and return captures. Full lower hull and fitted corner caps read at game/card scale. Whitespace check passes. Every test/probe ran with scratch APPDATA; 2,924 owner files fingerprinted with zero changes. Initial corner-variable type inference error was corrected before final passes; revision test has shutdown-only resource leak noise.

Evidence: output/moonbay-hull-corners-20260930/ (before card, alpha frames, logs, runner and fingerprints), output/large-room-review/moonbay-r*.png and output/moonbay-review/.

## Next action
Reload source game or Studio for owner review. No export or publication performed. Pressure-cycle evidence remains in MOONBAY_PRESSURE_HANDOFF_2026-09-30.md.
