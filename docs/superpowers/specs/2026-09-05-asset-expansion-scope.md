# Complete asset expansion scope ledger

The owner approved all seven asset groups on 2026-09-05 in addition to the hybrid
room redesign and three playable discovery branches. This ledger preserves the
whole request while separate implementation plans keep each subsystem testable.
This is scope tracking, not a claim that assets have been produced.

## Approved deliveries

- [ ] Room art: 31 existing identities and three new identities, with canonical
  doors and matching card thumbnails. First production checkpoint: reactor,
  hydroponics and mining bay under the room-art pilot plan.
- [ ] Functioning machinery: coolant, fans, growth, scanning and gravity motion
  attached to rooms, driven by actual operation, stopping on pause/offline.
- [ ] Door and connection assets: reusable open/closed frames, sealed ends and
  conduit treatments aligned with actual connection geometry. Inspect and reuse
  existing `dooranimated.png` where appropriate rather than discard it blindly.
- [ ] Blueprint presentation: coherent room thumbnails, unidentified treatment
  without revealing a hidden silhouette, and a newly-unlocked treatment.
- [ ] Discovery feedback: local discovery burst, stabilization pulses and distinct
  restrained sound cues; do not turn the station into a constant flashing display.
- [ ] Status graphics: functioning, no power, missing input and suspended icons,
  distinguished by shape and accompanied by text.
- [ ] Crew/drone assets: idle, walking, maintenance and workstation activity.
  Inspect existing Major Bill and mining-drone animations for reusable sources.
  Visual representation should follow real population and operation; adding a
  detailed job-assignment simulation is not implied by this asset request.
- [ ] Ambience: original or appropriately licensed machinery, ventilation, radio
  and hull sounds, layered sparingly with master/SFX/ambience volume controls and
  mute. No third-party audio purchases or new paid service without authorization.
- [ ] Gameplay: Tidal Condenser, Mycelium Nursery and Gravity Loom, three hidden
  unlock recipes and six further patterns, as specified in the room expansion.

## Delivery order

1. Art pilot and native readability checkpoint.
2. Remaining canonical art batches plus new-room playable expansion.
3. Doors, statuses, blueprints and local operational/discovery feedback.
4. Crew/drone activity assets and population-aware presentation.
5. Sound cues, ambient layers and audio controls.
6. Integrated native playtest, regression suites and seeded balance comparison.

Each subsystem receives a concrete implementation plan before code changes.
Sprite strips use an approved seed and stable frame anchors. Bitmap generation
uses the built-in image tool; no sheet is mistaken for an integrated animation.
Audio acquisition/synthesis method must be documented before production; do not
claim an image-generation tool creates sound. Existing art and saves are retained.
