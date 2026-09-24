# Bill autonomous native observation

Updated September 21, 2026. Broad animation/polish goal remains unfinished.

## Objective and constraints
Observe self-selected goals with the normal frame and cycle timers, following the
targeted north/west service clips. Preserve costs, failures, owner layouts and saves.
No gameplay or artwork changed; no generation or publication.

## Current state and verification
Evidence: `output/bill-autonomous-native-2026-09-21/`.
Isolated controlled-blueprint paid setup followed by 120 wall-clock seconds with
normal processing and cycle timer. No assigned NPC goals or altered needs. Dialogue
minimized through its normal method; camera follows Bill. Final run exits zero,
survives cycles 4 through 9 and produces 1105 samples/1101 native crops.
All four walking directions observed. Goals: curiosity 815 samples, hunger 196,
maintenance 90, no goal 4. One paused sample, not zero. No kneel/repair/stand in this
window; this run does not extend visual work-action acceptance. No logged errors.

The initial run used unscaled NPC coordinates for cropping and produced zero
images. Its behavior trace includes a north work transition but is not visual
evidence. Preserved as `unscaled-crop-review.*`. Corrected framing uses the game's
get_test_walker_position helper. Four final crops were outside the viewport;
sample-to-capture IDs were not recorded, so the review board labels only chronological
capture indices, not exact phases/timestamps. Future fixture now records capture_index;
that logging addition has not been rerun. Motion excerpt playback uses nominal 110ms
timing, not exact simulation timing.

Native chronological board inspected: connected visible limbs across room travel;
wall/equipment occlusion and dark offline rooms remain visible context. This is a
bounded agent observation, not owner smoothness approval or human expedition acceptance.

## Next action
The apparent standing figure in the central chamber is BRINE, not Bill. Resolved
by inspecting `brine_core_view.gd`: `brine_chamber` draws its own body texture from
`legacy/default/assets/rooms/brine-core/source/brine-cleaned-v5.png`, visually matching
the capture. `architect_pod` is separate and delegates to `architect_cryo_art.gd`,
whose recovered branch draws empty equipment. `Architects.pod_for_display` propagates
recovery state. Development notes and the chamber renewal README explicitly describe
BRINE's suspended crew-style figure. No bug fix or art change is warranted by this
observation; no new recovered-pod runtime test is claimed.
Further autonomous work-state coverage and owner motion feedback remain open.
