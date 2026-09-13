# Project handoff

Updated: 2026-09-13 · Project: Brine Space · Task: Clinical and biology themed/universal furnishings v7

## Objective and acceptance

Continue the large/medium matte asset program in Life Support, Med Bay and Bio Lab. Accept this batch when each room uses a large process-specific workstation plus a medium station-neutral support piece, with true-alpha sources, native four-rotation review, route-safe footprints, selected cards and recorded dependencies.

## Accepted decisions and constraints

Existing atmospheric machinery, treatment beds and biology processors remain intact. Themed assets replace smaller generic work furniture. Universal assets retain generic storage and transport functions and were reviewed on dark industrial, pale clinical and pale biological floors. Gameplay and character animation remain outside this pass. Owner aesthetic acceptance and a fresh playable export remain pending.

## Current state

Life Support uses `life_atmosphere_analysis_island` and `universal_filter_cassette_chest`; Med Bay uses `med_sterile_triage_island` and `universal_enclosed_equipment_cart`; Bio Lab uses `bio_culture_preparation_island` and `universal_specimen_transit_case`. Six 1254×1254 RGBA sources, prompts, registrations, generated-source paths, hashes, cards and selected profiles are indexed by `assets/room-furnishings-v7/manifest.json`. Full-wall wrappers retain the authored centerpiece and support anchors.

## Verification

The focused audit passes six assets, three themed/three universal, three large/three medium, and 12 native orientations in `output/room-furnishings-v7/verification.json`. The reviewed room sheet is `output/room-furnishings-v7/native-v2-contact-sheet.jpg`; the reviewed card sheet is `output/room-furnishings-v7/cards-sheet.jpg`. The updated Life Support, Med Bay and Bio Lab records point to current profiles, cards and component hashes. The broad shared dependency audit still reports unrelated stale records for Mycelium Nursery, Data Archive, Anomaly Lab and Medical Center; none of the v7 room IDs appear in its errors. Preferred layouts pass for 176 orientations, room cards pass for 47 identities, and 20 side-wall variants pass in `output/test-runs/20260913-014953-headless`.

## Next action

Continue with another bounded themed/universal asset batch outside active gameplay and character-overhaul work. Review this batch in the next playable export before owner acceptance.
