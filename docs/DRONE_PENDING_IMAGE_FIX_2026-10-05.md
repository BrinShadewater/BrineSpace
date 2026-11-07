# Drone pending-image cleanup fix

Updated: October 5, 2026 · BrineSpace · Runtime fix validated, not packaged

## Objective and acceptance

Investigate the larger drone allocation after conservative Veld residency savings
proved limited. Correct a reproduced unnecessary allocation without changing art,
frame timing, simulation or texture sampling. Keep active-fleet residency separate.

## Accepted decisions and constraints

Preserve the existing pixel-verified transparent-image representation: a wholly
invisible atlas becomes one transparent RGBA pixel and its drawing is skipped.
Do not evict active atlases or revisit rejected atlas remapping. Keep worker task
completion on scene/Studio exit; decodes must not outlive their owner.

## Current state

`drone_animation.gd::request_texture` stores both decoded image and `invisible` in
the completed worker result. Normal `finish_texture` forwards both to `cache_image`.
However, `drone_dock.gd::finish_pending_jobs` previously forwarded only the image,
so `cache_image` defaulted `invisible` to false. Exiting gameplay or Studio while
an entirely transparent sheet was pending could upload its full storage and lose
the invisible marker instead of using the established one-pixel representation.

The isolated native reproduction requests the actual selected `empty-120.png`,
then drains pending jobs using the real cleanup method:

| Result | Before | After |
|---|---:|---:|
| Decoded cache allocation | 96,337,920 bytes | 4 bytes |
| Texture size | 2688 x 8960 | 1 x 1 |
| Invisible marker | false | true |
| Pending jobs after drain | 0 | 0 |

The fix forwards `bool(job.result.get("invisible",false))`, matching the normal
loader's behavior. It avoids **91.875 MiB minus four bytes for this reproduced
pending sheet**. It does not establish how frequently the owner encounters this
exit condition, and is not a reduction to the measured steady-state active fleet.

Changed runtime: `scripts/drone_dock.gd` (one argument added).
Changed regression: `tests/test_drone_runtime_animation.gd` now queues both the
actual transparent sheet and a visible dock image through cleanup, checks tasks
are drained, checks the collapsed texture/marker and compares every visible pixel
to its decoded source.

### Active allocation assessment

The earlier 18-entry cache inventory remains evidence for that diagnostic only.
Its largest entries were three directional mining body/effect pairs (six sheets,
137.8125 MiB each), three wheel sheets (45.9375 MiB each), and two collection
sheets (91.875 MiB each), plus dock components. All were touched recently.
Current drawing selects body, wheels and any work effect together. Multiple drones
can require different headings/phases simultaneously. The cleanup fix cannot free
these visible layers, and forcibly enforcing the 256 MiB soft cap risks thrashing.

`prepare_paths` also refreshes recency before uploads to protect sibling layers;
recent use therefore includes preparation, not only submitted drawing. Future
residency traces should distinguish preparation, visible draw and retained-canvas
ownership. This nuance does not establish that any of the historical 18 entries
were safely evictable. Empty frame ranges keep their parent effect sheet ready for
upcoming visible frames; deleting it during a transparent interval is not accepted.

## Verification

Evidence: `output/drone-drain-fix-2026-10-05/` contains reproduction, isolated runner,
before/result JSON, guarded full-regression copy/runner and logs.

- Native before/after reproduction demonstrates the allocation and marker change.
- Maintained drone regression: 252 clips, 144 directional phase samples, dock
  boundaries and new pending-image checks; zero failures or engine errors.
- Visible cleanup image matches source bytes exactly.
- All three native runs used scratch APPDATA with a resolved-directory guard;
  every before/after owner check found all 2,936 non-log files unchanged.
- No frozen release rebuilt; no gameplay FPS, whole-game memory-budget or Mac
  acceptance claimed. Existing script UIDs preserved.

## Next action

Carry this fix into the next planned candidate build. For larger memory gains,
collect per-frame drone preparation/draw/retained-owner sets under a matched active
workload before considering eviction. Do not repeat rejected crop/remapping tests
or mistake this cleanup saving for removal of the active ~1.15 GiB allocation.
Keep render optimization work moving independently; release memory and Windows
stall gates remain open.
