# Architect cryostasis

New loops begin with one pod in BRINE Core containing the architect selected on
the title screen. Major Bill is initially available. Dr. Veld and Chief Engineer
Branforth become permanently selectable after their derelict recovery completes.
Each loop distributes the other two identities into the two existing wards,
one per ward, so no architect appears twice. The underlying ward system retains
support for one or two pods and legacy generic saves.

Expansion, matching doors, the 8 Metal repair and 18-second repair duration remain
in effect. Repaired wards become station rooms. Powered thaw requires free berths,
food and oxygen. A seven-second wake sequence adds the matching architect to the
Crew roster and releases their existing NPC at a clear navigation point beside
the pod. The startup pod uses emergency reboot supply; ordinary crew upkeep applies
once its occupant joins. Death removes physical presence without deleting the
permanent unlock. Pause and Continue retain intermediate animation progress.

## Art provenance and integration

Bill reuses `../derelict-cryo-v1/wake-0.png` through `wake-5.png`.
Veld and Branforth use generated identity edits of that same six-pose source,
referencing their existing south-facing character strips. Exact prompts and raw
sources are preserved here. `build_pack.py` uses the project's edge-connected
neutral-background cleanup, then fixed crops without stretching or mirroring.
The raw outputs had opaque checkerboard exteriors; cleaned RGBA sources and all
six transparent 418 × 627 frames remain reproducible. Manifests record source
hashes, crop data, pivot (210,560), playback timing and the empty-pod policy.

The runtime shares raw-PNG loading and registration between core and wards via
`architect_cryo_art.gd`. The installed empty pod reuses the original cryo-room
source. The identity animation gives way to the matching existing NPC sprites;
it does not introduce a new movement rig or architect bonuses. Room geometry
invalidates its furniture cache when the core pod appears or ward pod count changes.

## Verification

Both sprite manifests pass the sprite-animation validator with zero warnings.
`tests/test_architect_recovery.gd` exercises startup identity, no early NPCs,
pause, partial-wake save/Continue, permanent unlock and selection, ward release,
unique identities, malformed saves and old checkpoints. The generic cryo, save,
crew, wreck, discovery and drone regression fixtures also pass.

`tests/playtest_architect_recovery.gd` renders all six core frames for all three
architects, recovered wards, released and walking NPCs, and the title selector.
It asserts pixel-frozen paused emergence and checks title layout at 1280, 1600
and 2560 widths. Evidence is in `output/architect-recovery-v1/` with logs in
`output/architect-native-verified.log`. Native crops provide the room thumbnail
and comparison preview. Repair pacing and character animation polish still need
human playtesting.
