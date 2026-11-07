# Gravity Loom gameplay evidence

Uses the existing expansion specification: 12 Metal, 8 Data and 3 Rare Minerals
to build; four Power per functioning cycle produces one Data and one Rare Mineral.
The room starts locked and enters Science/Anomaly doctrine decks after unlocking.

`tests/test_gravity_gameplay.gd` exercises real paid-click and economy paths,
canonical resource IDs, starvation, interruption/reset of Inertial Containment,
three consecutive functioning cycles, one prototype, and both terminal recipes
in all four rotations. Research and prototype rewards are checked for idempotence.
Passing evidence: `output/gravity-loom/progression-v2.log`, zero errors/exit zero.

Earlier basic evidence was insufficient: it repeated a noncanonical `rare` key.
Definition and test now use `rare_minerals`, checked against the resource catalog.
The first progression run also exposed incorrect fixture partner rotations and
an assumed zero research balance; failed logs remain for traceability.

This is isolated fixture progression, not a native paid draft-through-unlock run.
Actual walker routes, additional viewport checks and export remain outstanding.
