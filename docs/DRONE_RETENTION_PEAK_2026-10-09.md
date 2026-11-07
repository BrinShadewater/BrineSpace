# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: drone retention peak and worker diagnostic load order

## Objective and acceptance

Continue the full PC/Mac performance and release-readiness plan. Explain the private
water-worker prototype's extra texture peak, test a measured remedy, and distinguish
worker scheduling from numeric preparation. All original release gates remain open.

## Accepted decisions and constraints

Keep both the worker prototype and retention remedy private. Preserve pixels, clocks,
resource identity, runtime PNG loading and owner data. No quality reduction, permanent
cache, renderer upgrade or normal-source change. Memory improvement alone does not
establish an FPS gain or release acceptance.

## Current state

Bounded weak-reference/RID bookkeeping in actual debug=false 1080p 40-room gameplay
localizes the extra peak to drone sheets. Around process frames 2496–2497, the worker
candidate owns 737.16 MiB of live sheets versus 415.60 MiB in the comparison. Five
extra sheets total 321.5625 MiB: collect-west, collect-west-cargo, carry-north,
carry-north-cargo and wheel-layer-west. They were last used at frame 2494. The
two-frame recent-use exemption preserves lookup ownership when new sheets arrive
at frame 2496. Process/render sample offsets remain explicit in the raw evidence.

A private one-frame exemption changes only the two pressure-eviction checks; both
lanes keep workers enabled and the 256 MiB cache budget. Matched candidate-first
release run, 3,000 measured idle frames per lane at 1×/2×/4×:

| Metric | Two-frame reference | One-frame candidate |
| --- | ---: | ---: |
| Global texture peak | 2408.880 MiB | 2345.481 MiB |
| Live drone sheets at frames 2496–2497 | 737.16 MiB | 415.60 MiB |
| Crew presenter uploads (not drone uploads) | 4074 | 4074 |
| Texture memory after scene disposal | 228.259 MiB | 228.259 MiB |
| Mean frame time, 1× / 2× / 4× | 38.024 / 39.241 / 40.228 ms | 38.840 / 39.672 / 41.176 ms |
| p99, 1× / 2× / 4× | 54.170 / 61.832 / 72.326 ms | 53.439 / 61.174 / 72.386 ms |
| Worst frame | 143.631 ms | 137.548 ms |

Counter-scope correction from subsequent source audit: private_end.uploads is the
crew presenter counter. The sampled-frame drone audit is 474 reference versus 475
candidate, one additional 802,816-byte north cargo-pose upload. Thus the blanket
one-frame policy does increase drone churn slightly; the earlier 4074 comparison
does not establish unchanged drone uploads. See WATER_PRIORITY_RETENTION_2026-10-09.md
for the refined policy, true drone counts and follow-up findings.

Peak improvement is 63.398 MiB; local overlap reduction is larger because the global
maximum occurs elsewhere after the remedy. Crew/drone/mission endpoints match in
all three phases. All natural missions return, unload and recover full navigation.
Average frame times worsen by 0.43–0.95 ms in this order; tails are mixed. No FPS
benefit is accepted. These are RTX 4070 Ti diagnostics, not target-hardware certification.

The newly added worker queue/build payload was null in the two full diagnostic
pairs. Investigation found a late adapter remount of census.pck overwrote the
early-mounted timing base before compilation. Those runs provide no new queue/build
attribution. Their drone measurements remain valid: the census pack does not replace
the drone module, whose compiled hash and selected retention branch were checked.
Previously measured scalar worker-wait attribution is separate evidence.

Removing the late remount restores queue/build/join payloads. A short actual-release
probe verifies all three instantiated MoonBase objects through their inherited
moonbay_base_canvas.gd script, byte hash
1149e11448932977dc4040ee39cfac8d96bd651aa6edf62cf415f9c82bdd061d.
The inner-class script itself has empty source; source checks must follow the base
script. Checks also run after canvases exist, avoiding vacuous early iteration.
Payload remains intact after game disposal. This short probe does not explain the
earlier rare 25 ms wait.

Evidence under D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/:
water-worker-detail/, drone-retention-window/, drone-retention-runtime/.
The corrected reversed runner is prepared in drone-retention-corrected-reverse/;
it has not run. It requires three compiled base identities, non-null timing payloads,
timestamp arithmetic, cleanup bounds and matched gameplay endpoints.

Checkout changes are private preparation/probe scripts under
output/renderdoc-tools-2026-10-08/, this handoff and CURRENT_STATUS.md. Normal gameplay
source is unchanged.

## Verification

Focused native GPU retention fixture: 9 checks, reference 2 expected failures,
candidate 0. Tiny 32-byte fixture budget exercises actual textures, eviction,
retained-command pixel equality, RID preservation, no-upload weak reconnection and
owner release under renewed pressure. An initial fixture assumed eviction without
pressure; that expectation was corrected before the recorded red/green pair.

Full release pairs have clean logs, debug=false, focused windows, no missing-art
failures, matched mission outcomes, all 6238 jobs joined, peak 2 active jobs and final
active 0. Bounded lifetime sampling takes at most 159 µs per call in the retention
pair, for 41 samples per lane. Failed worker-getter timings are not valid overhead
measurements of the completed getter. All runs/probes use isolated profiles; owner
2936 non-log files unchanged. Processes terminal and temporary adapters restored.

Remaining: corrected long worker timing, reversed retention comparison, animation
availability during reuse/transitions, full visual/lifecycle acceptance, and all
original packaged bug, performance, endurance and Mac certification requirements.

## Next action

Run drone-retention-corrected-reverse/run.py with the bundled Python runtime and
project cwd. Inspect compiled identities and complete payloads before interpreting
queue versus build duration; deduplicate events by submission timestamp when the
collector carries the preceding frame. Compare reverse-order frame tails, uploads
and sheet lifetime. Keep the remedy private if frame pacing or animation availability
regresses. Then target the independently measured large upload bursts and remaining
CPU draw work. Do not change worker priority without a measured scheduling cause.
