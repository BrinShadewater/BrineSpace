# Veld live transition deadlines

Updated: October 5, 2026 · BrineSpace · Observational native fixture

## Objective and acceptance

Measure uninterrupted equipment-action preparation windows at 1x/2x/4x using
normal game delta and actual renderer requests, with all textures resident. Find
constraints for a future residency policy without introducing missing art or
changing gameplay timing. This is not packaged performance certification.

## Accepted decisions and constraints

Use a dedicated three-room native station and valid navigation anchor. Start the
normal actor equipment action directly, excluding travel lead time; this tests
the short window when already at the destination. Keep the normal main process,
actor updates, speed controls and rendering. Disable automatic comms processing
and focus-loss pause only in this fixture. VSync disabled, cap 60, window 1600x900.
No texture eviction, decoding or upload is added during the measured actions.

## Current state

Output-only `audit_player.gd` subclasses the real CrewSpritePlayer, delegates frame
selection unchanged, and records returned wrapper IDs, requested keys/equipment
and timestamps. Existing player properties/banks are transferred to it after
startup. Calls outside frame/frame_at_elapsed, including direct pixel reads, are
not intercepted. All six actions finished normally and all recorded returns were
non-null. Twelve rendered frames after each completion sample early successors.

| Speed | Action | Authored simulation duration | Observed wall time | Render frames | Largest observed interval |
|---|---|---:|---:|---:|---:|
| 1x | Equip | 2.14 s | 2183.689 ms | 129 | 44.307 ms |
| 1x | Remove | 2.24 s | 2249.401 ms | 135 | 20.733 ms |
| 2x | Equip | 2.14 s | 1081.972 ms | 65 | 21.568 ms |
| 2x | Remove | 2.24 s | 1968.396 ms | 56 | **931.629 ms** |
| 4x | Equip | 2.14 s | 549.123 ms | 33 | 22.327 ms |
| 4x | Remove | 2.24 s | 563.764 ms | 34 | 21.299 ms |

Measurements are one action per condition, not percentiles or repeated acceptance
runs. Frame-post-draw timestamps bound completion and requests at frame granularity.
The long 2x removal interval is an unresolved >100 ms stall with all storage loaded;
it invalidates any smoothness claim for the run. Do not use that enlarged wall time
as extra preparation budget or attribute it to a residency manager that is absent.
Existing Windows scheduling investigations remain relevant but do not establish
this particular interval's cause.

Equip requests included the bare equip animation, then helmeted idle-east and
walking east/west. Removal used the bare removal action, then bare idle and walking.
The observed successors are not an exhaustive transition graph: other directions,
hazards, work, turns and interruptions remain possible.

### Decision from the measurements

Reject **whole inactive-bank reload at one image per rendered frame, starting at
equipment action entry**. The previous inventory has 769 helmet-only non-death
images, while the measured 4x equip window provides 33 render frames. The earlier
five-image experiment cannot justify this larger deadline. Do not compensate by
delaying equipment completion or running hundreds of synchronous uploads at once.

The next candidate needs permanently ready immediate successors, hazard/death and
direct-read dependencies, plus preparation begun on locker request/approach where
possible. Streaming must be byte/time bounded. Even a two-MiB-per-frame hypothetical
budget would prepare only 66 MiB in 33 frames, below the 151.77 MiB decoded candidate
set; that arithmetic is not measured upload throughput. More aggressive throughput
must be demonstrated under gameplay, not inferred from an otherwise empty fixture.

## Verification

Evidence: `output/veld-transition-research-2026-10-05/` contains native fixture,
delegating audit player, isolated runner, raw result, summary script/JSON and log.
Final run: six completed actions, no engine errors, all 2,936 owner files unchanged.

Earlier attempts were rejected: activating Veld at the default (0,0) position
triggered exterior death; a state capture established it before correcting the
fixture to a navigation point. Another attempt paused during the action; the
dedicated fixture then excluded dialogue/focus pause. Those timings are not used.
The exterior-failure log is retained as `fixture-failure.log`. Runtime code and
owner settings were not changed. No visual-parity or full lifecycle certification
is claimed from this observational fixture.

## Next action

Build a conservative pin-set specification for the equipped and unequipped states:
all immediate locomotion/facing successors, current/return frames, relevant death
entrances, and pixel-read consumers. Quantify unique storage remaining after those
pins using the existing inventory. Add logging-only coverage for actual locker
approach, cancellation, pause/resume, death and restore before any eviction.
Do not enable eviction until observed requests are covered and preparation deadlines
pass. Keep the unresolved stall separate from storage policy and release acceptance.
