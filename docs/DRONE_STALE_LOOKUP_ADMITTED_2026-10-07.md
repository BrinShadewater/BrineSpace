# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: stale drone lookup cleanup admitted to source

## Objective and acceptance
Reduce stale image retention while preserving selected animation pixels, retained
canvas ownership and upload reuse. Full original PC/Mac release gates stay open.

## Accepted decisions and constraints
Adopt as a conditional transient memory fix, not an FPS improvement. No art,
filtering, atlas or animation changes. Keep 256 MiB decoded lookup budget and
recent image protection; retained canvases independently keep their images alive.

## Current state
Normal `scripts/drone_animation.gd`: frame-post-draw over-budget stale pruning,
session weak lookups to reuse still-held immutable images, expired weak metadata
cleanup, additive weak-entry/removal diagnostics. `scripts/session_art_cache.gd`:
final-owner weak metadata clear and trim signal disconnect. Existing native
`tests/test_session_art_cache.gd` adds four signal/lifecycle assertions; UID kept.
No release executable/PCK rebuilt this turn.

## Verification
Third current-source native40-room1080p9-phase pair: full state/pinned image/
viewport equality,98 uploads each, clean logs/exits, all texture endpoints equal.
This control had no stale surplus at zoom2x: both4,391.55474MiB. Prior two pairs
each reproduce exact64,225,188byte saving when control retains stale tyre/effect
lookups. Thus benefit is conditional; no three-run universal saving claim.
Third median phase mean36.72218->37.25892ms; frame times mixed across all pairs.
Historical104ms stall remains open; zero>100ms in this pair does not close it.

Pre-admission native runtime tests pass:252 clips/144 directional samples/dock
boundaries,13 upload checks,22 session checks. Admitted-source rerun passes same
animation coverage,13 upload checks and26 session checks, with no errors/warnings/
leaked instances. Prior private ownership/raster probe13 and lifecycle probe14
checks pass. Reversed trim overhead mean33.31us,max791us/720 rendered frames.
All owner fingerprints2,936 files unchanged; all processes terminal.
Artifacts: `output/drone-stale-lease-2026-10-07/gameplay-third/`,
`runtime-regressions/`, `admitted-regressions/`.

Admitted SHA256:
- Motion: ceb4a541137cd3065585294ceba74329d45f8da19d7169e4eb24f8001b5fb0b1
- Session: aa454ce1bdb0f5d95a8115e3eebe0497a180f301d5396af11818f8d8889ecd72
- Session test:1504b24588fae53bfb7646c664505e845512e5358f2eb38ed91896f7adc0ae2c

## Next action
Prioritize the larger zoom redraw stall and exact crew texture memory provider.
Refresh maintained packaged candidate after the next substantive accepted source
milestone; audit/run debug=false and verify scene transitions there. Current
large-scene memory remains well above3GiB and p95/p99 remain outside60FPS gates.
