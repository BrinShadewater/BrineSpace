# Project handoff

Updated: October 5, 2026 · BrineSpace · Repeated reading-pose GPU readbacks

## Objective and acceptance

Reduce verified transition work without changing selected frames, interruption
timing, save behavior or image lifetime. Continue memory diagnosis without
repeating rejected eviction, cropping or startup-worker candidates.

## Accepted decisions and constraints

Prior audits already cover decoded duplication and nested non-pool caches.
Weak lookup clearing cannot reclaim owned animation images; the tested full-bank
reload paths miss readiness deadlines. No additional memory remedy is accepted
here. Source review instead identifies repeated reading-pose GPU readbacks.
Cache only image storage explicitly marked immutable by the session texture pool.
Mutable, direct and unmarked generated images use the original readback algorithm.

## Current state

`scripts/crew_texture_pool.gd` marks its shared uploads `crew_immutable_pixels`.
`scripts/veld_npc.gd` keeps one six-pose lookup using weak references and integer
wrapper/storage/player identity keys. Check metadata and existing timing/facing
guards on every request. Replacing a wrapper or diffuse image invalidates the
lookup; no pixel copies or strong bank references are retained. Equipment switch,
new player, new scene and mutable-image fallbacks preserve original behavior.
Reference switch: `--reference-reading-poses`.

New paired-UID `tests/test_veld_reading_pose_cache.gd` is in the native performance
lane. Experimental full-Veld loader is freshly extracted from current grid source,
restricting only its actor loop. Evidence, full logs, measurements and source hashes:
`output/reading-pose-cache-2026-10-05/`. No art/save schema/package/upload changes.

## Verification

Godot 4.7.2 native Compatibility, RTX 4070 Ti. Initial complete-bank scan measured
763/790 us bare/helmet per call; this preliminary measurement is not a matched
optimization comparison. Final full-bank three alternating pairs, 60 calls per
variant/gear: 437→15 us bare, 434→15 us helmet. Separately, selected reading-only
bank three pairs measure 320→15 us for both gears. Host/load-dependent timings
differ; only matched pairs establish each saving. These are repeated helper costs,
not an overall FPS gain or explanation for second-long stalls. First acquisition
and other interruption/death pixel comparisons still require readbacks.

838 focused checks pass: both selected gears, all six interruption poses, exact
stage/timer/retained source through the 60 ms hold, wrapper/storage/metadata changes,
legacy loop/facing paths, mutable direct images and weak-bank release. Existing
crew-pool test passes 46 checks. Zero engine errors; 2,936 owner non-log files
unchanged in every isolated batch. All runners verify the resolved scratch profile.
Existing selected gameplay regression, with only output paths relocated and a
profile guard added: 22,683 checks, zero failures; 56 actual power/suspension
interruptions and 12 fresh-main disk restores. Exact interrupted source/contact,
paused restore and resumed finite future checks pass in both gears. A restored
bare room capture was visually inspected. This is staged main-scene restore,
not packaged Title → Continue or full-platform acceptance. No drawing changed.

## Next action

Keep the memory budget failure explicit: this cache does not detach
textures or certify safe residency. Any additional readback replacement needs
exact source/transition comparisons and current source invalidation coverage.
Minimum hardware, long stalls, packaged performance/endurance and native Mac gates
remain open. Frozen release inputs remain unchanged.
