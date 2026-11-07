# Project handoff

Updated: October 14, 2026 · Project: BrineSpace · Task: smaller full-atlas uploads

## Objective and acceptance

Reduce large mining uploads with exactly the same pixels/sampling and bounded memory,
then benchmark. Private feasibility work; no normal source admission or export implied.

## Accepted decisions and constraints

Test a materially different path from rejected live palette shaders and cropped frames:
upload full-coordinate RG8 color IDs plus a small RGBA palette, expand once into a full
RGBA viewport target, then draw that target through the original ordinary sampler.
Preserve original PNGs, dimensions, invisible RGB, animation clocks, roots, filters,
layering and gameplay. Keep the 256 MiB ordinary cache policy. No downscaling or lossy art.

## Current state

**Reject this candidate for performance. Normal game source/art and Windows delivery
are unchanged.** Private files: `output/drone-gpu-rebuild-20261014/`; frozen source,
small source-overlay packs, encoded PNGs, JSON, screenshots and logs:
`C:/bs-drone-gpu-rebuild-20261014/`. Reuse the existing physical QA runtime serially.
Reference is the prior private room-image reuse baseline, excluding allocation reuse.

Offline encoding reconstructs both North/South mining atlases exactly, including all
transparent RGB. Native feasibility succeeds for both. Runtime scope is **North only**:
the target's measured backing overhead rules out assuming broad coverage is cheap.
Only private `drone_animation.gd` changes plus new private `drone_gpu_rebuild.gd`;
seven normal runtime sources remain byte-unchanged.

Selected PNG and both derived PNG hashes/dimensions guard decoding. The worker loads
indices; main-thread creation uploads indices/palette. A root-owned post-draw manager
keeps target nodes alive through weak texture-wrapper records. Canvas pins preserve the
wrapper across cache eviction/restoration. Manager queues staging deletion after drawing,
accounts for it until deletion is observed, and deletes targets after the last wrapper
dies. No callbacks or node teardown execute inside a dying Texture2D destructor.

One selected path bounds pending staging to 70 MiB; peak actual source staging is
72,297,472 bytes / 68.95 MiB. A conservative 3 GiB admission estimate plus 96 MiB reserve
selects the unchanged original RGBA path if refused. Upload diagnostics distinguish
encoded transfer bytes from logical RGBA residency; ordinary cache bookkeeping does
not pretend to include all viewport backing. No new live palette shader or delayed
publication flag: first-use rendering depends on normal viewport dependency ordering.

## Verification

Actual debug=false Godot 4.7.2 Compatibility, RTX 4070 Ti, 1920x1080, muted secondary
display, disabled input, fixed window, fresh scratch APPDATA, resolved user-directory
and source/instance identity guards. All GPU jobs serial.

Native raw feasibility: **76 checks / zero failures** across both large source sheets.
Every GPU-reconstructed RGBA byte matches, including zero-alpha RGB. First-use rendering,
nearest/linear, five frame indices, three scales, mirror/rotation/tint tested.
Final actual candidate: **16 ownership/integrity checks + 38 native rendering checks,
zero failures**. Includes two retained canvases -> one -> none, weak restoration,
staging/output release, repeated reconstruction, changed-source rejection, first-use
and sampling equality. Final reference: 16 checks / one expected missing-reduction
failure. Representative reference/rebuilt PNGs are byte-identical and visually reviewed:
`native-pixels3-{reference,rebuilt}.png`.

Footprint control, one atlas with reference retained:
baseline 5.028 MiB; original only 188.777; original+output 464.402;
original+output+staging 556.333. Thus an ordinary image adds 183.75 MiB to the engine
counter, the rebuilt target 275.625 MiB, and staging about 91.93 MiB. GPU expansion cuts
transfer volume but increases target backing; it is not a resident-memory optimization.

Matched station benchmark: idle/pan/zoom/lighting at 1x/4x, 120 frames/phase,
both execution orders: **3,840 frames / 16 exact state-camera pairs**.

| Metric | Forward reference / candidate | Reverse reference / candidate |
|---|---:|---:|
| Mean frame | 24.791 / 25.764 ms | 24.834 / 26.049 ms |
| Candidate change | 3.92% slower | 4.89% slower |
| Maximum frame | 72.061 / 78.714 ms | 77.032 / 149.733 ms |
| Frames >50 ms | 5 / 9 | 3 / 7 |
| Frames >100 ms | 0 / 0 | 0 / 1 |
| Selected North transfer | 137.8125 / 68.9482 MiB | 137.8125 / 68.9482 MiB |
| Selected North creation call | 12.147 / 37.338 ms | 12.568 / 64.452 ms |
| Sampled engine texture peak | 2784.653 / 2876.529 MiB | 2784.653 / 2876.529 MiB |

One rebuild/run, no admission fallback. P95 improves only 2/8 and 3/8 phases; 0/16
candidate phases meet the existing 60 FPS gate. The largest reverse candidate frame
overlaps North rebuild and ordinary South upload: 206.76 MiB / 85.683 ms creation API
time, 135.281 ms before-render wall time. Scopes overlap and must not be added.
Creation includes allocation/staging/scheduling, not completed GPU expansion; delayed
viewport queries cannot identify this frame's GPU execution cost. In-process isolated
repeat still costs 39.741 ms after initial 42.317 ms, so this is not established as a
cold-shader-only problem. No speculative shader prewarm admitted.

Reported station texture peak stays below 3072 MiB, +91.875 MiB vs reference. Conservatively
adding twice the largest raw staging payload to that sampled peak gives 3014.425 MiB;
this is an allowance, not an observed driver-VRAM maximum. Per-frame sampling alone
does not certify all within-frame/driver allocations. Release static-CPU counter returns
zero/unavailable; no total process-memory or endurance claim. No unbounded new CPU cache.

Initial wrapper teardown exposed an invalid PREDELETE Callable then an access violation;
the manager design replaces that path. Two later pixel-fixture attempts incorrectly
dropped the owning wrapper while retaining only its raw viewport/ViewportTexture. They
failed/crashed and are excluded; the corrected fixture retains the owning texture
through both control lanes. Logs retained. No production fix inferred from invalid tests.

Final audit: all seven final evidence runs verify immutable pack/source identities;
no captured engine errors or SafeImage failures (reference assertion failure expected).
All 19 owner guard records preserve 2,948 files. Original North/South PNG hashes and seven
normal runtime files unchanged; no QA process remains. No export/commit/publication.
Evidence: `analysis.json`, `final-audit.json`, `north-*-max-frame.json`, `ownership-green3.json`,
`native-pixels3.json`. Earlier raw feasibility pack preserved as `feasibility-reference.pck`.
Final candidate SHA-256:
`e51799f5de7aec0cbe70efc7588d1234c1e693a0b474b54ac288c584b6419c74`.

## Next action

Keep GPU rebuilding private and rejected. Halving this transfer is insufficient when
creating its destination costs more than the original upload. Expanding it to more
sources would increase memory exposure without a demonstrated timing benefit. Do not
repeat this, allocation reuse, larger-cache, prewarm, crop, live-indexed or separate-thread
variants unchanged. A further exact-storage approach must avoid the extra expensive
render target as well as preserving full-coordinate sampling; otherwise return effort
to larger steady-frame CPU/submission costs. PC/Mac and full release gates remain open.
