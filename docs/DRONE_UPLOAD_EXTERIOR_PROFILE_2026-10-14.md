# Project handoff

Updated: October 14, 2026 · Project: BrineSpace · Task: drone uploads and exterior drawing

## Objective and acceptance

Profile mining-drone uploads and exterior submission, then test a targeted improvement
without changing selected pixels, sampling, animation, gameplay or owner data. Compare
against the frozen room-image reuse prototype; do not imply a new production build.

## Accepted decisions and constraints

Keep the 256 MiB normal cache and original full-size source images. Earlier larger-cache,
prewarm, cropped/indexed storage and six-source sharing trials remain rejected in their
recorded scopes. Separate render-thread mode previously crashed before gameplay;
do not repeat that configuration as a release optimization. Relevant evidence:
[current upload context](DRONE_CURRENT_UPLOAD_CONTEXT_2026-10-10.md),
[prewarm rejection](DRONE_PREWARM_BUDGET_REJECTION_2026-10-10.md),
[sharing](DRONE_STORAGE_SHARING_MAP_VERIFICATION_2026-10-10.md),
[render-thread rejection](ATLAS_CPU_AND_BILL_STORAGE_2026-10-07.md).

## Current state

**No optimization admitted. Normal source, art and Windows delivery are unchanged.**
New private drivers/fragments: `output/drone-profile-20261014/`. Frozen source, packs,
identities, JSON and logs: `C:/bs-drone-profile-20261014/`. Reused the existing physical
QA runtime serially. Seven-file reference includes the prior private room-image reuse
candidate and frozen normal drone/session scripts. Candidate changes only private
`drone_animation.gd` and `session_art_cache.gd`.

The allocation experiment keeps at most one spare ordinary RGBA8/unmipmapped texture,
bounded to 48 MiB. Existing aged eviction can supply it only after cache removal leaves
one local strong reference; runtime canvas pins exclude textures used by retained drawing
commands. Old weak-path lookup is removed before repurposing. Matching uploads call
`ImageTexture.update()` with the original full image; final session exit clears the spare.
No crop, resampling, prewarm, clock, quality or readiness policy change. This cap targets
46 MiB wheel/steering sheets, not the 138 MiB mining-body sheets.

## Verification

Actual debug=false Godot 4.7.2 Compatibility, RTX 4070 Ti, 1920x1080, muted secondary
display, disabled physical input, fixed window, fresh isolated APPDATA and source/instance
identity guards. Deterministic 40-room mixed-large fixture, same active crew/production.

Final caller-separated diagnostic: 720 measured idle/zoom frames, 1x/4x. Nested scopes
below are microsecond timers converted to milliseconds; **do not add them**. They are
instrumented diagnostic results, not a performance comparison or hardware guarantee.

| Phase | Exterior pass | Fleet drawing | Exterior readiness | Exterior cache/image creation | Exterior sampling |
|---|---:|---:|---:|---:|---:|
| Idle 1x | 0.535 | 0.403 | 0.035 | 0.027 | 0.042 |
| Zoom 1x | 1.760 | 1.598 | 1.188 | 0.969 | 0.053 |
| Idle 4x | 2.712 | 2.526 | 1.959 | 1.564 | 0.060 |
| Zoom 4x | 1.818 | 1.633 | 1.298 | 1.034 | 0.034 |

The readiness/upload path dominates active transitions. Harvest/construction/other
exterior work is much smaller; total cache trimming outside exterior is 0.044–0.144 ms
per frame. Docked consumers are classified separately (zoom-4x cache/image creation
0.331 ms), so these costs are not silently charged to exterior drawing. These timers
exclude worker decode CPU time; readiness and image creation are distinct scopes.

Fresh diagnostic outlier: 116.488 ms frame overlaps mine-north and mine-south uploads,
289,013,760 bytes (275.625 MiB), 50.479 ms image-create API time. Correlation uses the
explicit sampled upload event frame and timestamps. This supports a synchronous upload
burst; it does not establish current-frame GPU execution time or an additive breakdown.
See `detailed-v3.json`, `profile-outlier.json`. V1's first phase includes warm-up totals;
exclude it. V2 fixes the reset but aggregates dock/exterior; V3 supplies final attribution.

Allocation trial: four serial runs, both orders, idle/pan/zoom/lighting at 1x/4x,
120 frames/phase: **3,840 comparison frames / 16 exact state-camera pairs**.

| Metric | Forward reference / candidate | Reverse reference / candidate |
|---|---:|---:|
| Mean frame | 25.532 / 26.945 ms | 30.691 / 36.047 ms |
| Candidate change | 5.54% slower | 17.45% slower |
| Maximum | 76.563 / 78.750 ms | 96.665 / 110.427 ms |
| Frames >50 ms | 7 / 11 | 39 / 62 |
| Frames >100 ms | 0 / 0 | 0 / 4 |
| Sampled upload API total | 598.676 / 647.242 ms | 716.192 / 839.927 ms |
| Peak engine texture counter | 2784.65 / 2799.59 MiB | 2784.65 / 2799.59 MiB |

Candidate reuses 66 allocations in each run but p95 improves only 1/8 phases per order;
0/16 candidate phases pass the existing 60 FPS gate. Repeated sampled upload payload
remains about 4.8 GiB/run: reuse does not reduce transfer volume. Events are deduplicated
by frame/path/start timestamp from bounded sampled diagnostics, not a complete session
GPU inventory. Per-frame texture peak remains below the 3072 MiB gate, but rises 14.94
MiB; phase endpoints alone would misleadingly show a decrease. Host variation is large;
these results reject this candidate, not every possible texture-update strategy.

Native contract: baseline red4 six checks / one expected missing-reuse failure; candidate
initial six / zero; extended **16 / zero**. Full RGBA bytes and dimensions exact, two
retained canvases keep identical nonempty pixels under pressure, one remaining pin stays
immutable, weak restoration cannot return a repurposed image, both eviction sites covered,
size/format behavior and final session release checked. Source review found no actionable
issue. Red1–3 are invalid fixture attempts: Vector2/Vector2i comparison aborts the final
check before output; corrected explicitly, retained, excluded from acceptance.

All nine accepted evidence runs verify immutable overlay/source identities; no captured
engine error text or SafeImage failures. Seventeen owner guard records preserve all 2,948
files. Seven normal runtime files unchanged; no QA process remains. No export/commit or
asset edits. Audit: `final-audit.json`; paired results: `analysis.json`. Candidate SHA-256:
`f3c12d65822502e225d46b42a2140cb731f7acd58cf67bc82a7b67db1f96cc4e`.

## Next action

Keep allocation reuse rejected and private. The useful remaining upload target is the
large full-atlas payload at visible state transitions, with exact original-coordinate
sampling and bounded memory as hard constraints. A smaller sampling/dust cleanup cannot
materially close the 60 FPS gap. Do not repeat larger-cache, prewarm, crop, indexed,
sharing or separate-thread variants unchanged. No appearance-preserving improvement was
established in this interval; a materially different storage remedy needs its own exact
pixel and matched-performance evidence before integration. Target PC/Mac, endurance and
full release acceptance remain separate work.
