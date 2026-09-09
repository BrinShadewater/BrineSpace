# Companions

Implemented locally September 9, 2026. [Visual review](../character/companions/review.html).

## Accepted identities and encounters

Companions are additional NPCs, separate from architects.

| Identity | Appearance and motion | Discovery |
|---|---|---|
| River | Small sage-green/ivory R2-D2-like wheeled droid | Trash container in a derelict garbage disposal room, north of the starting core |
| Josh | Larger muted bluish lavender Johnny 5-like robot, explicitly on twin treads | Shipping crate in derelict storage, east of the starting core |
| Margot | Alex's white/tabby cat with green frog hat; [portrait V3](../character/margot-portrait-v3/portrait.png) simplifies fur and matches crew shading, four-direction idle/walk | Small surviving pet cryopod beside two broken human cryopods containing skeletons, south of the core |

River's utility-droid V1 portrait and Josh's V4 portrait are owner-selected. Named
copies, original paths and hashes live in character/companions. Josh's explicit
September 9 tread instruction supersedes every earlier dog or biped description.
The superseded biped sheet is retained as source history and is not loaded.

## Playable companions

New loops place three finite recovery compartments unless their companion was
selected for that expedition. Connect a matching door, spend 8 Metal on hull
repair and wait 18 simulation seconds. Inspect the connected room and explicitly
open its trash container or shipping crate, or start Margot's pet-pod thaw. Eight seconds of powered restart/thaw
releases the companion and permanently unlocks future selection. Repair payment,
partial restart, opened container, roster, actor route and playback survive
Save/Continue. Pause and power loss stop the applicable work without losing progress.
Repeated interaction never duplicates the actor or unlock.

The shared New Loop picker offers optional unlocked-companion checkboxes beside
the architect choice. Choose any subset, including none. Confirm saves the choices;
Back leaves them untouched. Selected companions arrive in the core after the
architect wakes. Unselected companions remain recoverable in their encounters.
Old checkpoints receive no new obstacles or surprise NPCs.

Companions keep company with nearby living crew using connected-door routes and
prop collision geometry, with independent decision RNG and animation playback.
The Crew journal has a separate Companions section. They do not occupy architect
berths, construct rooms or use human Food/Oxygen. Personal battery, damage and
special work abilities are not part of this prototype pass.

Found compartments reuse the salvage-workshop, storage-bay and cryo-chamber room shells and
normal functioning economies. Recovery objects have dedicated opened/closed art
and reserved collision footprints; intersecting furnishings are omitted only in
these found compartments. Normal blueprint layouts and player layout files are
unchanged. Recovered rooms retain Suspend/Resume controls and show their upkeep.
Costs and durations above are first-pass tuning, not owner balance acceptance.

Margot's found cryo ward contains exactly three dedicated pod props with matching
navigation footprints. The two failed human pods never grant crew. Her pet pod
remains occupied through the eight-second thaw and opens empty only after rescue.
The restored cryo chamber consumes 1 Power/cycle. Margot uses the companion
prototype's social movement; pet feeding, drowning and other survival behavior
are not implemented. Companion checkpoint V2 reads older two-robot V1 saves;
older loops gain neither a cat nor a new rescue obstacle.

## Personality and interactions

Margot now sits, grooms and naps between walks. Use Journal > Crew > Pet Margot
to see her reaction; petting also wakes her from sleep. River inspects recovered
salvage containers and makes quiet spatial chirps. Josh makes tread pivots and
head gestures, and approaches nearby architects performing repairs to watch.
Actions, transition time, cooldowns and pending approaches survive Continue and
freeze when paused. See [personality handoff](COMPANION_PERSONALITY_2026-09-09.md)
and [motion review](../character/companion-personality-v1/review.html).

## Base art and verification

Each companion has four-direction idle and locomotion clips: 8 clips / 24 frames,
92x92 canvas with pivot (46,86). River is 44 source pixels tall; Josh is 70.
Margot is 28-34 source pixels tall including her raised tail/hat, and walks on
four paws. All three runtime packs load raw PNGs through the existing sprite player. Exact
image_gen prompts, source sheets, deterministic builders and moving reviews are
preserved. No mirrored views. Generic manifest checks report zero errors/warnings.

Focused headless and native checks cover recovery, paid repair, power/pause,
selection/cancel, new-loop inclusion, legacy saves, malformed records, disk
Continue, actor travel and small-window picker layout. Native captures and motion
previews remain available for owner art/motion acceptance. Existing architect,
save, construction and wreck tests also ran; detailed results and log limitations
are in the [handoff](COMPANIONS_HANDOFF_2026-09-09.md).

No executable package rebuilt. Margot's added evidence and remaining motion
review are recorded in [her handoff](MARGOT_INTEGRATION_2026-09-09.md).
