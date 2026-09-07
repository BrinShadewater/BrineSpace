# Tidal Condenser gameplay branch

Implemented the approved design values: locked Engineering/uncommon blueprint,
7 Metal + 2 Data build cost, 2 Power consumption, 2 Water production and the
west/east/south tee. Unlocked copies enter Industry/Biosphere decks.
Thermal Reclamation unlocks it; Nutrient Mist and Chilled Cells each grant their
specified cycle bonus and one-time 3 Research terminal reward. Existing patterns,
save schema and failure conditions are preserved.

`tests/test_condenser_gameplay.gd` passes real paid-click affordability/spending,
production/power starvation, hidden card hints, interrupted three-cycle discovery,
one prototype reward, idempotent terminal rewards and rotated compatible/sealed
partner cases. It uses a process-specific isolated save. Nursery's branch and
the four existing gameplay regression suites also pass with no SCRIPT ERROR/ERROR
lines. Evidence is in `output/tidal-condenser/test_*.log` and `.err`.

The initial test incorrectly assumed zero stored Power stopped Life Support
next to a functioning Reactor. Production power sustains it in the existing
economy, so the corrected test suspends Life Support to interrupt the streak.
Original failing `gameplay.*` evidence is retained. No economy behavior was
changed to satisfy the fixture.

Art source exists but station/card registration is still pending. This branch
is not a claim of full room or native discovery-UI acceptance; new art and native
progression/export checks remain required.

## Native paid progression

`tests/playtest_condenser_progression.gd` passes at 1280x720, 1600x900 and
2560x1440 using the actual scene. It controls only the foundation draft and RNG;
normal costs, resources and failure conditions remain enabled. Paid Reactor,
Mining Drone Bay and Life Support sustain three complete discovery cycles;
Thermal Reclamation earns one live-deck prototype, a normal reroll draws it,
and the condenser purchase spends the exact authored cost. The next full cycle
runs it; inspector suspension stops it and resume clears suspension.

The 1600 prototype and built/functioning captures were visually inspected:
learned recipe/blueprint text and new card art are visible, the condenser appears
in the station and its +2 Water effect is shown. The objective overlay partly
covers the station edge; these are UI/progression evidence, not full art review.
Logs/captures are `output/tidal-condenser/progression-v2-1600` and
`progression-1280`, `progression-2560`. Initial v1 failed to parse because the
adapted fixture referenced a nonexistent parent; preserved, corrected in v2.
All completed runs exit zero without SCRIPT ERROR/ERROR lines. Metadata saves
are process-specific; the fixture also isolates the manual loop-save path.
Placement-preview rotations and terminal recipes in native UI remain separate
from this unlock/build sequence.
