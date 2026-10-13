# Drone upload experiment and paired-build handoff

Updated: October 5, 2026 · Project: BrineSpace · Task: PC/Mac release readiness

## Objective and accepted constraints

Investigate remaining upload stalls, prepare matching Windows/Mac candidates and
establish native Apple Silicon evidence. Preserve selected pixels, clocks, quality,
saves and layouts. No public upload. Performance/memory gates remain mandatory.

## Controlled upload result

A native developer probe decodes the selected collect-east-cargo atlas before
measurement, then alternates 30 fresh GPU uploads with 30 resident-texture draws.
Order alternates per round; both paths draw identical pixels, use uncapped/VSync-off
rendering, and settle between samples. Atlas: 2688×8960, 96,337,920 bytes (91.875 MiB).

| Measurement | Fresh upload | Resident texture |
|---|---|---|
| Median create/assignment | 11.013 ms | 0.002 ms |
| Median interval through two rendered frames | 12.528 ms | 0.510 ms |
| Maximum interval through two rendered frames | 13.828 ms | 1.215 ms |

This establishes a material synchronous upload cost on the RTX 4070 Ti host. It
does not certify gameplay or target hardware, nor reproduce the long station
stalls. The earlier cached developer run's 937.090 ms outlier records its last
upload eight process frames earlier; 404.539 ms precede rendering and 510.037 ms
follow the render signal. GPU time is 10.925 ms. Last-upload metadata alone cannot
exclude delayed driver work, texture retirement, scheduling or other callbacks.
No speculative drone rendering change was accepted on this evidence.

Probe is developer-only; its Image.load_from_file call emits an export warning
and is not shipped. Runtime PNG loading is unchanged. All 60 samples completed;
2,936 owner non-log files unchanged under an isolated profile. Evidence:
`output/drone-upload-2026-10-05/upload-probe.json`, `summary.json`, `probe.log`.

## Candidate selection

Physical copy of the previous accepted snapshot, plus the verified Research Lab
rotation cache. New source identity: **brinespace-af8b5f00998283ef**.
55,692 frozen inputs including tools/templates; 36,235 selected runtime inputs.
Comparison against brinespace-124c70736fbfb879 changes only
`rooms/full-wall-v1/research_lab_view.gd`: no runtime additions/removals or art changes.
Previous candidate remains available for rollback. Research cache retains its
453 native checks from PRE_RENDER_OPTIMIZATION_2026-10-05.md.

## Verification and delivery

Manifest tests: 9 pass. Mac template-selection tests: 2 pass. Release assertion
tests: 2 pass. Both exports pass. Universal 2 bundle contains arm64/x86_64 and an
executable with mode 100755. Exact PCK audits outside the checkout each check
35,779 assets: zero missing/changed/unexpected. Both PCKs have SHA256
`d3d9d18daa4e2d2b04e6620c44ef7da6e6e2c316a7ef0ab66d6f88aaffa89910`.
Runtime manifests match exactly. Frozen input verification checks 55,692 files
without unexpected changes. All owner fingerprint checks preserve 2,936 files.

Actual Windows release intro/title/New Game/dialogue/simulation/F8 smoke passes
with zero failures and debug=false; 1080p gameplay screenshot inspected. The
existing 34-object exit warning remains open. This functional check ran while Mac
export was active and provides no performance evidence.

After export completed, three runs per Windows package measured the same 40-room
1080p workload, 180 frames per action/speed, uncapped, with automatic diagnostics
enabled. A process monitor rejected competing Godot/BrineSpace processes; all six
runs were valid and completed without engine/script errors. Median per-run p95:

| Action | Speed | Prior package | New package |
|---|---|---|---|
| Zoom | 1× | 55.816 ms | 53.933 ms |
| Lighting | 1× | 70.076 ms | 69.219 ms |
| Zoom | 2× | 65.267 ms | 58.951 ms |
| Lighting | 2× | 70.180 ms | 73.138 ms |
| Zoom | 4× | 62.895 ms | 62.634 ms |
| Lighting | 4× | 70.789 ms | 68.204 ms |

The component setup reduction is confirmed, but this batch does not establish a
consistent overall lighting improvement: 2× p95 is 4.2% worse. Do not promote the
earlier development-only 4.9–6.5% lighting gain as a packaged result. All 18 new
candidate phase runs fail the frame gates. Worst frames: prior 1030.216 ms, new
1037.501 ms. Both memory sequences match: 4036.943/4035.401/4035.401 MiB.
New candidate request-to-ready: fresh profile 15.690 s, warm 6.444/5.902 s; disk cache
uncontrolled and synthetic station construction excluded. The earlier r6 run set
had shorter outliers; these new results expand the known packaged-stall issue,
without establishing its cause. Source selection alone did not solve the gates.

Internal deliverables: `output/drone-upload-2026-10-05/windows/BrineSpace.exe` with
adjacent PCK, and `output/drone-upload-2026-10-05/macos/BrineSpace.zip`. Each has
build metadata, hashes, instructions and copied notices. The Mac checklist is
included. Evidence: `pair-audit.json`, `runtime-delta.json`, `frozen-check.json`,
`normal-entry-r2/`, `baseline-benchmark/`, `candidate-benchmark/`, `comparison.json`.
These artifacts are test candidates, not public-release certification.

Apple Silicon execution is unavailable on this Windows host. First Mac session
uses a separate macOS test account, confirms actual generated save/report paths,
then exercises clean launch, input/Retina, audio/focus and save/relaunch/Continue.
The checklist accompanies the Mac candidate. Do not assume APPDATA isolation or
unverified HOME redirection establishes Mac profile safety. Developer ID signing,
notarization, downloaded Gatekeeper/stapling/offline tests and Intel gameplay remain
open. Native Mac tester/machine details requested; no credentials collected.

## Next action

Gather the first Mac results and instrument complete drone upload/eviction history
alongside before/after-render intervals and focus/scheduling state. Choose a remedy
only after a matched station workload supports it. Reduce the oversized texture
working set without changing visible pixels. Full benchmark matrix, original bug
closure, save upgrade, two-hour soak and ten scene transitions remain release gates.
