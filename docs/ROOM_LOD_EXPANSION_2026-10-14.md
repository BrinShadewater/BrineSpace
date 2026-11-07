# Project handoff

Updated: October 14, 2026 · Project: BrineSpace · Task: expanded distant-room prototype

## Objective and acceptance

Owner approved expanding the private room-image prototype to more expensive rooms,
measuring zoom-in/out hitches and benchmarking again. Keep crew, doors and warnings
live. Preserve crew/furniture order and use the full renderer at close distances.
This remains a feasibility prototype; no production integration or export requested.

## Accepted decisions and constraints

Retain the original three large rooms; add eligible contents of Life Support,
Storage Bay, Hydroponics Bay, Research Lab, Reactor, Crew Hab, Galley and Solar Array.
Actual expanded queues must contain only standard library props/base/live entries.
Actors, custom/portable props, docks, aquariums, wet materials and unknown passes
keep full drawing. Any crew inside a room forces immediate full-content fallback,
preserving the existing sorted depth order. Grid updates eligibility before both
the retained advance shortcut and full submit. Fire/wet/recovery rooms stay live;
doors, warning/hazard overlays, floors and walls remain outside ordinary captures.

Ordinary rooms use one 384-square transparent image over square painted bounds with
padding. Large rooms retain two 512-square images around live doors. Source art
uses NEAREST filtering, matching GridCanvas. Entry <=0.24, exit >0.28. A shared
budget schedules at most one room capture per engine frame. Original drawing stays
visible until frame_post_draw confirms the capture; ticketed callbacks replace
obsolete pending callbacks. Cache key includes content generation/count, static
state, layout revision, painted bounds, filtering and Reduced Motion. Actor entry
does not create a cached crew image. Machinery animations intentionally hold at distance.

## Current state

**Normal game source and Windows delivery are unchanged.** Drivers/private fragments:
`output/room-lod-expand-20261014/`; derived source, frozen overlay packs, JSON, logs
and images: `C:/bs-room-lod-expand-20261014/`.

Three comparison lanes share the physical `brinespace-2fb8e8659a3be093` Windows QA
copy and previously accepted companion CPU fix: original renderer, earlier three-
large-room prototype, expanded candidate. Frozen source checks and actual companion
instance checks are mandatory. RTX 4070 Ti, Godot 4.7.2 Compatibility, debug=false,
1920x1080 secondary display, muted audio, disabled input, fixed window dimensions.
Native/GPU jobs serial; scratch APPDATA and owner fingerprints around every job.

## Verification

Final native probe: **18 checks / zero failures**. Actual Bill entry restores live
ordered slots; the occupied room interior is pixel-exact against full drawing.
Departure restores raster use. Actual fire keeps the room live and its interior
matches full drawing. Direct hazard/wet gates, pending capture visibility, queue-tail
removal, Reduced Motion and one-owner-per-frame scheduling are covered. The actor
fixture restores animation playback as well as position; snapshots match after it.
All frozen comparison state snapshots match. At zoom 0.30 and 0.50, fallback pixels
match in both directions; distant sampling/held animation differences are expected.

Independent review caught queue-tail invalidation, Reduced Motion and painted bounds
before timed admission. Rapid same-frame replacement exposed duplicate signal
connections; callbacks now disconnect the prior pending callable before registration.
Earlier diagnostic probes with these failures are excluded. A first hitch harness
used an immediate camera setter and lost coverage; it is excluded. Maintained
animated zoom requests with a fixed comparison center replace that setter.

### Steady three-lane comparison

Idle, pan, zoom and lighting at 1x/2x/4x, 120 frames per phase, all three lanes in
forward and reverse order: **8,640 accepted frames / 24 exact state-camera triples**.

| Order | Original mean | Three-room mean | Expanded mean | Expanded vs original | Expanded vs three-room |
| --- | ---: | ---: | ---: | ---: | ---: |
| Forward | 27.379 ms | 27.695 ms | 27.521 ms | 0.52% slower | 0.63% faster |
| Reverse | 27.309 ms | 26.480 ms | 25.641 ms | 6.11% faster | 3.17% faster |

Idle 1x: original 24.546/24.023 ms (~41-42 FPS), three-room 23.192/23.727 ms
(~42-43 FPS), expanded 21.770/22.747 ms (~44-46 FPS). Expanded cached-room counts
vary with crew/hazards; roughly two dozen ordinary rooms plus the three large rooms
are active. Mean calls: original ~2,881, three-room ~2,684, expanded ~2,385:
~17.2% below original and ~11.1% below three-room. End texture counter adds
41.25 MiB versus original / 29.25 MiB versus three-room in both orders.

Expanded p95 improves 15/24 phases versus original and 15/24 versus three-room.
Expanded worst frames are 100.677 and 89.349 ms; still **0/24 expanded phases pass
the maintained 60 FPS gate**. Forward 2x lighting and following phases are broadly
slower across script and renderer scopes despite lower draw counts; cause unresolved.
Do not pool away this variation or claim a consistent overall FPS/pacing gain.
Render CPU averages improve from ~6.56 ms original to ~5.59-5.97 ms expanded;
live-room callback totals are mixed (~6.31-6.78 ms vs original ~6.50 ms).
Nested/delayed scopes are not additive. Evidence: `steady-analysis.json` and six
`forward-*` / `reverse-*` JSON, trace, identity and owner files.

### Cold, repeated and interrupted zoom

Normal animated zoom requests cross 0.20/0.32 around a fixed station center.
Cold cases discard the scratch raster images after zooming close, before entering
distant view. Repeated cases retain them; interrupted cases reverse direction
mid-transition. 1x and 4x, 360 frames per phase, three lanes: **6,480 accepted frames**.
All six full simulation states and start/end cameras match across lanes; at least
23/40 rooms intersect the viewport throughout. This is one ordering, not repeated
release pacing certification. `hitch-analysis.json` contains per-frame window counts.

| Scenario | Original p95 | Three-room p95 | Expanded p95 | Expanded maximum |
| --- | ---: | ---: | ---: | ---: |
| Cold 1x | 37.880 ms | 43.724 ms | 36.921 ms | 68.958 ms |
| Repeated 1x | 37.465 ms | 37.358 ms | 37.492 ms | 51.713 ms |
| Interrupted 1x | 32.650 ms | 31.903 ms | 31.781 ms | 49.658 ms |
| Cold 4x | 44.866 ms | 40.897 ms | 41.363 ms | 64.898 ms |
| Repeated 4x | 54.517 ms | 52.580 ms | 42.204 ms | 93.180 ms |
| Interrupted 4x | 45.506 ms | 37.375 ms | 37.201 ms | 72.622 ms |

P95 improves 5/6 against original (repeated 1x essentially flat), 4/6 against prior.
Expanded maximum is 93.180 ms vs fresh original 99.727 ms; expanded has no >100 ms
frame in this scope. However entry windows are mixed: cold 1x's far-entry window
maximum is 63.742 ms vs original 45.493 ms. Do not claim hitch-free entry or a
universal reduction. Across the expanded run, 284 capture events schedule at most
one owner per frame; no unbounded simultaneous capture burst was observed.

Trace excerpts distinguish remaining costs: the cold 1x 63.742 ms frame contains
~29.8 ms after-render wait with no sampled drone upload, cause unresolved. A repeated
4x far-entry frame of 75.006 ms includes ~193 MB of rover atlas/cargo uploads taking
27.36 ms. An interrupted 4x 72.622 ms frame includes a 37.7 ms simulation step.
These do not establish one common cause or attribute every hitch to the room cache.
See `entry-hitch-excerpts.json`; no drone/simulation code was changed.

The first completed original hitch control reused its earlier failed scratch label
and inherited discovered-recipe flags. It is excluded: all phases differed only in
`run_discovered_synergy_ids`. `hitch-reference-fresh.json` uses a new profile and
matches all states/cameras. The driver now rejects reused runtime profile labels;
the guard's rejection and all seven Python drivers' syntax were checked. Real owner
data was never used as the running profile.

### Final audit

All **21 saved owner guards preserve 2,948 files**. Five normal runtime source files
match the frozen originals byte-for-byte. Final visual, both expanded steady runs
and expanded hitch run load the identical candidate pack, SHA256
`2a613b14040dab84dda01afef6c9d4eab31184c22207a383943faab3a4e9dd3c`.
Accepted logs have no engine/script errors; all QA processes have exited. Final
fitted/0.24 screenshots were reviewed after matching the source filter. Close fallback
at 0.30/0.50 remains pixel-exact; distant raster resampling remains visible at edges.
`final-audit.json` records integrity and identity. No export, commit or publication.

## Next action

The expansion and requested measurements are complete; keep it private. The next
useful CPU work is measuring cache-management overhead and unnecessary zoom-time
recapture. Full zoom phases add ~28 captures although room artwork often stays the
same; the current conservative generation follows retained-slot keys. Ordinary
advance also restores then hides original slots on active frames. Profile/value-key
these paths before production integration rather than enlarging the cache set again.
Static images improve distant idle/submission cost, but this version does not prove
consistent whole-workload performance or smooth 60 FPS zooming.

Arbitrary effect extents, ancestor tint/materials, other crew-specific poses,
all rotations/filter modes, long-run cache lifetime and owner visual acceptance
remain broader production checks. No release, Mac, endurance or 60 FPS acceptance
is implied by this prototype.
