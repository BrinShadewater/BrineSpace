# Project handoff

Updated: 2026-09-13 · Project: Brine Space · Task: Utility and science themed/universal furnishings v6

## Objective and acceptance

Continue the large/medium matte asset program in Tidal Condenser, Gravity Loom and Xeno Lab. Accept this batch when each room uses a large process-specific workstation plus a medium station-neutral support piece, with true-alpha sources, native four-rotation review, route-safe footprints, selected cards and recorded dependencies.

## Accepted decisions and constraints

Existing condenser banks, loom apparatus and xeno containment machinery remain intact. Themed assets replace smaller generic work furniture. Universal assets retain generic storage/service functions and include one narrow portrait footprint. Gameplay and character animation remain outside this pass. Owner aesthetic acceptance and a fresh playable export remain pending.

## Current state

Tidal Condenser uses `tidal_analysis_island` and `universal_valve_locker`; Gravity Loom uses `gravity_tensor_console` and `universal_diagnostic_rack`; Xeno Lab uses `xeno_assay_table` and `universal_decon_caddy`. Six 1254×1254 RGBA sources, prompts, registrations, generated-source paths, hashes, cards and selected profiles are indexed by `assets/room-furnishings-v6/manifest.json`. Full-wall wrappers retain the deliberately authored anchors through directional wall-bank placement.

## Verification

The focused audit passes six assets, three themed/three universal, three large/three medium, and 12 native orientations in `output/room-furnishings-v6/verification.json`. The reviewed room sheet is `output/room-furnishings-v6/native-v1-contact-sheet.jpg`; the reviewed card sheet is `output/room-furnishings-v6/cards-sheet.jpg`. Tidal and Gravity owning manifests pass composition dependency audit; the updated Xeno record is current while its shared batch manifest retains unrelated concurrent warnings. Preferred layouts pass for 176 orientations, room cards pass for 47 identities, and 20 side-wall variants pass in `output/test-runs/20260913-013058-headless`.

## Next action

Continue with another bounded themed/universal asset batch outside active gameplay and character-overhaul work. Review this batch in the next playable export before owner acceptance.
