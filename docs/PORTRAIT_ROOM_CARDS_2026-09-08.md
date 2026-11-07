# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: portrait room-card preview

## Objective and acceptance

Show the owner room cards with a taller, recognizably card-shaped silhouette.

## Accepted decisions and constraints

Preview keeps existing artwork, text and card interactions. Owner visual acceptance
of the new proportions remains pending.

## Current state

`scripts/main.gd`: cards changed from 276 × 272 to 224 × 320; artwork area grows
from 92 to 128 high. Rarity badges anchor to the right edge, prototype badges sit
below them, and the hand tray/deck height accommodates the portrait format.
`tests/preview_portrait_cards.gd` captures an isolated opening hand without using
the owner's save. Preview: `output/portrait-room-cards.png`.

## Verification

Native Godot 4.6.1 capture exits 0. Visually reviewed at 1600 × 900: all three cards
fit, including wrapped Mining Drone Bay title and Hydroponics costs/outputs.
This is a visual layout preview, not a full gameplay regression run.

## Next action

Owner review of proportions. No commit or push made.
