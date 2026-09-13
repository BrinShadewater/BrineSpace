# Project handoff

Updated: 2026-09-13 · Project: Brine Space · Task: Themed and universal room furnishings v3

## Objective and acceptance

Add large and medium matte props that reinforce themed room activity, plus restrained station-neutral furnishings that can fit several interiors. Accept this batch when six assets are selected in production rooms, readable at native scale in every rotation, route-safe, card-complete and reproducible from recorded sources.

## Accepted decisions and constraints

Universal pieces use neutral construction and generic service functions. They remain sparse support pieces; each room keeps a distinct themed activity. Owner aesthetic acceptance and a fresh playable export remain pending.

## Current state

Hydroponics Bay uses a nutrient island, Ore Refinery a sorting bench, and Cryo Chamber a thaw cart. Quarantine Cell uses a parts chest, Pressure Control an equipment plinth, and Isolation Vault a task table. Sources, prompts, registrations, cards, hashes and review evidence are indexed by `assets/room-furnishings-v3/manifest.json`. Selected room profiles and owning manifests record their dependencies; Hydroponics has no composition-owning room manifest.

## Verification

The asset audit passes six 1254×1254 true-alpha sources, six registrations, six cards and 24 native orientations in `output/room-furnishings-v3/verification.json`. The native review is `output/room-furnishings-v3/native-v2-contact-sheet.jpg`; the card review is `output/room-furnishings-v3/cards-sheet.jpg`. Preferred layouts pass for 176 orientations, room cards pass for 47 identities, and 20 side-wall variants pass in `output/test-runs/20260913-003920-headless`.

## Next action

Continue the larger asset-fix program with another small themed/universal batch, avoiding rooms being changed by the gameplay and character-overhaul sessions. Review this batch in a fresh playable export before owner acceptance.
