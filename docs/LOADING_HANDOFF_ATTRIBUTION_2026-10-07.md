# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: loading handoff attribution

## Objective and acceptance

Explain the remaining packaged loading pauses before selecting a remedy. Original PC/Mac loading, frame, memory, visual, bug and endurance gates remain open.

## Accepted decisions and constraints

Experimental package `66929cd10addc5b0` runtime inputs unchanged. Diagnostic adapters use isolated profiles and bounded metadata sampling without retained scene/image references. No runtime patch, art change, loading interval adjustment or diagnostic disabling is admitted. Cache-uncontrolled New Game/Continue results are not certified cold/warm loading.

## Current state

Four actual debug=false lifecycle runs progressively add stage labels, render/process boundaries, existing grid/upload counters, then an automatic-capture/breadcrumb-off control. Source/identity backups and runners remain under `output/drone-compiled-2026-10-07/` and its `qa-helper/` folder.

`ImagePrefetch.PUMP_MS=120` intentionally refreshes loading roughly eight times per second, explaining many routine gaps. It does not explain the second-long handoff pauses.

Stage run: interface/grid construction 8,246.784 ms New Game / 2,527.228 ms Continue; station prewarm 136.366/161.866 ms. Largest gaps are at/after prewarm transitioning to ONLINE.

Boundary run: New Game gaps 965.892/1,149.057 ms, render pre-to-post intervals 13.175/13.048 ms. Continue gap 1,511.166 ms, render interval 6.094 ms. These signals exclude canvas preparation; they do not identify all remaining CPU/GPU work.

Work-counter run: first New Game gap 963.912 ms includes 647.706 ms accumulated grid callback work/26 counted callbacks. Following gap 1,157.338 ms; counters consumed/reset by monitor at endpoint. Neither gap includes ordinary/indexed drone uploads. Continue gap 1,467.465 ms includes only 4.478 ms additional indexed upload time and 0.016 ms ordinary upload time; decode/preparation is excluded from upload counters.

An automatic report occurs during loading, recording the previous 10,779 ms frame. Capture/breadcrumb-off control still has New Game gaps 885.182/1,057.350 ms and Continue 1,435.744 ms; render intervals 12.661/14.263/5.487 ms. Automatic capture is not established as the main cause. This single two-feature control does not establish an accepted gain; normal diagnostics remain enabled.

## Verification

All four runs: 142 checks each, zero failures/errors/leaked-instance warnings. Every owner fingerprint: 2,936 files, zero changes. All handles terminal. No visual/release gate closed. Raw `packaged-loading-{stage,boundary,work,capture-control}-gaps.json`, lifecycle logs/results and owner fingerprints preserve evidence. The matched station adapter is restored; diagnostic adapters and fixture hashes are retained separately.

## Next action

Attribute first canvas preparation and deferred UI/scene handoff separately, including ordinary image decode and room submission. Preserve required crew completion, complete interactive rooms and pause/input ownership. Do not change scheduling until the remaining approximately one-second pre-draw work is identified. Larger sustained rendering and lossless drone admission work also remain.
