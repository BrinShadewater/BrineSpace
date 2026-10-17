# Cryostasis fall and recovery — September 30, 2026

Owner found the appearance good and requested that live crew start at the landing
spot. Landing v2 fixes the drawing-offset handoff and validates actual rendered
positions. Source art/timing unchanged. Current preview:
`output/cryo-fall-landing-grade-v6/thaw-and-exit.gif`.

Installed only for human pod emergence: Bill, Veld and Branforth. Slower exit,
knees buckle, hands catch the floor, grounded side pose, push up, kneel, upright.
No death state or gameplay penalty is invoked. Existing recovery totals, costs,
resource/berth gates and unlocks remain unchanged; crew enter navigation only
after the completed recovery. Marsh keeps his separate charging sequence.

The physical sequence occupies the final 4.6 seconds of existing saved wake
progress: opening0.55s, step1.4s, fall0.7s, floor hold0.55s, recovery1.25s, idle0.15s.
Frost clears before opening. The mild cold-blue tint persists until floor contact,
then recedes during recovery. Translucent internal mist fades as the door opens;
a pale, flattened cloud lingers at the base. Mist uses linear sampling to match
the matte crew's gameplay density while housing retains its original sampling.
Pause/Continue reconstruct every phase from wake; no independent playback timer.

Three new eight-pose sources were generated with detailed directional masters
and actual selected matte idle references. Exact prompts and immutable sources
are in each actor's `sources/`. High-resolution references:

- Bill: `character/bill-video-south-v6/master-input.png`.
- Veld: `character/veld-video-south-v1/master-input.png`.
- Branforth: `character/branforth-video-south-v1/master-input.png`.

`python tools/build_cryo_fall_recovery.py` extracts connected authored poses,
cleans exterior haze, applies one frozen neutral material calibration per actor,
registers floor contact and packages256px canvases/pivot128,224/standing148.
One uniform source scale per actor; crouches/lying poses are never enlarged to
standing height. First/last frame pixels are the exact selected idle, padded by
36,52. Fall's final frame is rise's first frame. Six new interior poses per actor;
source standing endpoints remain preserved but are not substituted for live idle.
Generated material transfer, source hashes and placement records in registration.

Private recovery manifests load through `architect_cryo_art.gd`; they do not
override general crew actions, selected locomotion, equipment or ACTIVE_ASSETS.
PNG assets retain the repository's Git LFS attributes.

Packaging contract tests and all three sprite manifests pass with no warnings.
Recovery/timing/save regression gates pass. Native pause, exact release point,
inactive grounded crew, and grounded save/Continue checks pass for all three
humans; rotated ward playback checked. Preview and evidence:
`output/cryo-fall-recovery-v1/thaw-and-exit.gif`. Owner accepted the polished grade-v6 sequence for gameplay and found derelict
cryolabs. Shared core/unrepaired/repaired routes and found-ward assertions verified
in output/cryo-installed-v7. Playable export validation remains pending.
