# Project handoff

Updated: 2026-09-13 · Project: Brine Space · Task: Cross-department themed and universal furnishings v5

## Objective and acceptance

Continue the large/medium matte asset program in three visually different departments. Accept this batch when Reactor, Clone Lab and Biodome each use a large process-specific workstation plus a medium station-neutral support piece, with true-alpha sources, native four-rotation review, route-safe footprints, selected cards and recorded dependencies.

## Accepted decisions and constraints

Existing reactor, cloning and cultivation machinery remains intact. The new themed assets replace smaller generic preparation furniture rather than adding duplicate work surfaces. Universal assets use neutral construction and generic functions. Gameplay and character animation remain outside this pass. Owner aesthetic acceptance and a fresh playable export remain pending.

## Current state

Reactor uses `reactor_control_rod_bench` and `universal_tool_chest`; Clone Lab uses `clone_genome_island` and `universal_sample_trolley`; Biodome uses `biodome_potting_island` and `universal_supply_pallet`. Six 1254×1254 RGBA sources, prompts, registrations, generated-source paths, hashes, cards and selected profiles are indexed by `assets/room-furnishings-v5/manifest.json`. The Biodome q3 full-wall reconstruction explicitly retains the two authored furnishings.

## Verification

The focused audit passes six assets, three themed/three universal, three large/three medium, and 12 native orientations in `output/room-furnishings-v5/verification.json`. The reviewed room sheet is `output/room-furnishings-v5/native-v1-contact-sheet.jpg`; the reviewed card sheet is `output/room-furnishings-v5/cards-sheet.jpg`. The three updated dependency records have current profile and component hashes; broader owning manifests still contain unrelated stale records from concurrent room work. Preferred layouts pass for 176 orientations, room cards pass for 47 identities, and 20 side-wall variants pass in `output/test-runs/20260913-011605-headless`.

## Next action

Continue with another bounded themed/universal asset batch in rooms outside active gameplay and character-overhaul work. Review this batch in the next playable export before owner acceptance.
