# Project handoff

Updated: 2026-09-13 · Project: Brine Space · Task: Power-room themed and universal furnishings v4

## Objective and acceptance

Continue the large/medium matte asset program by replacing the repeated generic service bench in the three power-expansion rooms. Accept this batch when every room has a distinct themed work anchor plus a restrained neutral support piece, with true-alpha sources, native four-rotation review, route-safe footprints, selected cards and recorded dependencies.

## Accepted decisions and constraints

The main turbine, digester and heat-recovery machines remain unchanged. New furnishings describe nearby work rather than duplicating the focal machinery. Universal assets use generic service functions and neutral construction. Gameplay and character-animation work remain outside this pass. Owner aesthetic acceptance and a fresh playable export remain pending.

## Current state

Current Turbine uses `current_flow_governor` with `universal_instrument_cabinet`; Biomass Digester uses `biomass_feedstock_island` with `universal_maintenance_trestle`; Heat Recovery uses `heat_exchanger_manifold` with `universal_cable_caddy`. Six 1254×1254 RGBA sources, prompts, registrations, generated-source paths, hashes, cards and selected composition profiles are indexed by `assets/room-furnishings-v4/manifest.json`. The power-room renderer selects the v2 profiles, and `rooms/power-expansion-v1/manifest.json` owns their dependency records.

## Verification

The focused audit passes six assets, three themed/three universal, three large/three medium, and 12 native orientations in `output/room-furnishings-v4/verification.json`. The reviewed room sheet is `output/room-furnishings-v4/native-v1-contact-sheet.jpg`; the reviewed card sheet is `output/room-furnishings-v4/cards-sheet.jpg`. Composition dependency audit passes all three power-room profiles. Preferred layouts pass for 176 orientations, room cards pass for 47 identities, and 20 side-wall variants pass in `output/test-runs/20260913-010049-headless`.

## Next action

Continue with another bounded themed/universal asset batch in rooms outside the active gameplay and character-overhaul work. Review this batch in the next playable export before owner acceptance.
