# Reactor economy and lighting review

## Why the earlier offline picture remained lit

The earlier host-animation fixture removed the cell from `powered_room_cells`
without adding an offline reason or entry in `unpowered_room_cells`. The lighting
helper treats that combination as awaiting evaluation, not loss of light power.
The machinery flag alone is therefore not a whole-room darkness fixture.

Current Reactor data produces six Power and consumes no inputs. An empty reserve
does not power-starve that generator. The real applicable shutdown condition is
`SUSPENDED`; do not alter costs or add consumption to force a darkness test.

## Native evidence

`tests/playtest_reactor_lighting.gd` calls the actual `_apply_room_economy()` for
running, suspended and resumed states. It then steps the production lighting fade
explicitly, including an attempted advance while paused halfway through.

`output/reactor-lighting-native-v1` exits 0 with zero assertion failures and no
ERROR/SCRIPT ERROR entries. Raw-image loading warnings remain. All four rotations
verify:

- Reactor functions and generates six Power with zero initial stored Power.
- Suspension produces the real offline reason, stops generation and targets zero
  light intensity.
- The 0.65-second fade reaches half intensity after 0.325 seconds; pausing retains
  both its level and exact room pixels despite an attempted 0.65-second advance.
- Completing the fade darkens the rendered room. Sampled image-space luminance
  falls from approximately 0.234–0.236 to 0.095–0.096. This is a screenshot metric,
  not a physical light measurement.
- Resuming and evaluating the economy restores operation; the full fade returns
  to the exact original sampled brightness in every rotation.

`output/reactor-lighting-negative-v1` exits 1 with eight expected failures. Its
test-only stuck-on level fails both zero-intensity and rendered-darkening checks
in every rotation. Production code remains unchanged.

The positive record `reactor-lighting.json` retains per-rotation measurements and
the main, grid and lighting helper hashes. Input isolation passes. A subsequent
native editor import exits 0 without engine/script errors and creates the test's
paired UID.

## Visual scope and remaining work

Reviewed full 1600x900 captures `reactor-light-q0-suspended.png` and
`reactor-light-q3-half.png`. The room darkens without erasing its low shell or
machinery silhouettes, and the fixtures lose their bright active appearance.
These selected frames are not exhaustive visual acceptance at every resolution.

The test uses fixture placement and direct suspension state followed by actual
economy evaluation, not UI clicking, paid construction or a continuous player run.
It does not certify character overlap, emergency illumination, other departments
or fresh exported execution. UI counters are not explicitly refreshed after each
fixture economy call, so the top-bar values in these images are not economy UI
evidence. The machine and lighting assertions use the actual state directly.

No art, geometry, production lighting, economy or player save changed. The bible
already separates electrical power, equipment operation and emergency lighting;
this finding reinforces that contract without adding a duplicate policy. Native
Reactor lighting is verified for suspension/resume; packaging remains separate.
