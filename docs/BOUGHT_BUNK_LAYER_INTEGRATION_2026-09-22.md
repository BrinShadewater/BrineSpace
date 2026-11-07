# Bought bunk foreground integration

Updated September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Support believable crew occlusion by the bought bunk's ladder, left post and front
rail. Preserve empty-room artwork, owner placement and ordinary actor depth. Full
bunk sleeping behavior remains a separate unfinished requirement.

## Accepted decisions and constraints
No owner layout/source pixel changes, Higgsfield, publication or commits. Split
only library/tileset-mb2-14 in Crew Hab. Special actor depth requires explicit
furniture=bunk metadata and a nearby unmirrored bunk. Existing generic states do
not opt in. Mirrored art parity is verified, not mirrored bunk sleep choreography.

## Current state
scripts/room_asset_library.gd caches complementary full-atlas textures with original
UV geometry. Crew Hab returns back/front prop entries at sort_y and sort_y+0.02;
marked bunk poses sort between them. Nursery base renderer adds narrow overridable
entry/signature helpers for its direct and retained queues. Other rooms retain the
original one-entry/sort-value behavior. Source-specific masks resolve variants
before copied IDs. Layer cache signatures include rect/registration/flip/texture:
a sideways layout move cannot leave stale presentation copies.

scripts/crew_sprite_player.gd reads the furniture marker. The staged Veld lowering
manifest opts in; no runtime catalog or NPC activity is bound to it. The raw source
and local builders remain in character/bunk-contact-study-2026-09-21/.

## Verification
Native tests/test_bunk_layers.gd: 17 checks, zero failures; paired Godot-generated
UID and native test-index entry included. Covers exact RGBA empty split/unsplit,
normal and horizontal mirror, direct/retained empty and occupied parity, source
preservation, texture and stable queue reuse, unchanged generic pose depth,
same-height horizontal movement and variant-source negative control. It waits for
observable draw completion and rejects headless runs.

Installed direct renderer matches all 19 Veld prototype captures byte-for-byte
without the fixture foreground overlay. Initial comparison using a subclass was
invalid because script-path identity dropped room assets; corrected with the actual
renderer and --unsplit-bunk-layers. Comparison uses all RGBA bytes, not getbbox's
alpha-only default. Native 36-case crew-room activity regression passes. Logs in
output/layout-default-audit-2026-09-21/: test-bunk-layers-final.log,
crew-activity-after-bunk-layers.log, bunk-layer-runtime.log,
bunk-layer-baseline-fixed.log. No export or frame-rate claim.

## Next action
Complete standing-to-seat/ducking, smooth lowering and reversed rise for Veld, then
Branforth, Bill and Marsh contact as needed. Add gear coverage, reachable station
registration and controller/save/interruption evidence. The bought bunk still has
no live sleep activity; this milestone installs its required renderer support.
