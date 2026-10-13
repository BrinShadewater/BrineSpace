# Project handoff — Solar Array rotation copying reduced

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

## Objective and acceptance
Continue sustained large-station rendering optimization. Previous turn was progress:
matched real-map runs verified construction fixes and established remaining frame gates.
This pass traces and reduces a measured rotation setup cost; release remains uncertified.

## Accepted decisions and constraints
Windows RTX 4070 Ti/1080p, actual debug=false performance executable, muted secondary
display, disabled physical input, isolated resolved APPDATA, owner fingerprints and
20 GiB storage floor. Reuse runtime with small overlays. No art, animation, gameplay,
texture-quality, engine or indexed-provider changes.

## Current state
Changed rooms/full-wall-v1/solar_array_view.gd: each existing rotation snapshot may
retain an additional owned working layout/props/profile copy. Before restoring it,
compare its complete values with the original snapshot. Any mutation makes fresh deep
copies; unchanged data reuses the working set. Original snapshots remain independent;
rotation tables remain bounded to four entries and preserve existing edit/Studio
invalidation. GPU images remain shared as before. This retains additional bounded CPU
metadata; OS memory and transition-lifetime acceptance are still required.

Changed tests/test_solar_rotation_cache.gd: exercise rotations after deliberately
mutating active props, layout and profile. Compare restored values/pixels and explicitly
require the mutation markers to disappear. Existing script UIDs preserved. Installed
Solar bytes exactly match the candidate measured in release gameplay (installation.json).

Private instrumentation remains outside production. A 40-room trace finds no measured
Solar setup in idle/pan, but rotation restores reach 2.8 ms in zoom rebuild samples.
The parent configure and wall application are comparatively small. This identifies
deep copying as the local cause, rather than a missed rotation cache or art upload.

## Verification
Three alternating matched pairs each on reported12, current10→11 and corrected40:
18 actual release runs,19,440 measured frames, idle/pan/zoom/lighting at1×/2×/4×.
The six completed large runs were reused when extending to the real saves. All108
full gameplay and phase camera pairs exact; no runtime/missing-image errors. Input,
mute/display and complete initial station coverage guards pass.

| Map | Mean ms, normal → installed | p95 ms | p99 ms | >50 / >100 frames |
|---|---:|---:|---:|---:|
| Reported12 |13.244 →13.154|19.651 →19.212|23.231 →22.904|0/0 →0/0|
| Current10→11 |12.785 →12.788|19.029 →18.994|28.609 →29.513|1/0 →1/0|
| Expanded40 |26.685 →26.623|44.649 →43.369|57.325 →57.205|71/0 →73/0|

Solar configure mean during lighting: reported884→431 µs (51% reduction), large
535→312 µs (42%). During zoom: reported116→57, large157→92 µs. Large local setup
improves in every pair; its overall mean improves0.23% in all pairs. Reported mean
improves0.68% with mixed pair means; current mean is effectively unchanged (+0.02%).
Accept for the consistent measured local cost reduction and regression coverage,
not as a stutter cure. Current p99 worsens; large max87.432→92.015ms and >50 count
increases slightly. Preserve these observations and continue investigation.

Texture peaks unchanged:1558.872/1940.831/3028.007MiB. Not startup/OS/lifetime peaks.
All p95 gates and current/large p99 gates still fail. No cold/warm, full title/Continue,
1440p, target-hardware or Mac certification is implied.

Native visual fixture:425 checks pass against original behavior, including four
rotations, four shell/floor passes, power/clocks and five layout edit modes. Passes with
defaults and copied owner layouts. Installed canonical source:440 checks pass, including
explicit mutation restoration. An additional retained-image check gives442/zero failures;
the nonempty exact selected-layout prop capture was visually inspected. A preceding
saved PNG was blank and is not visual acceptance. Initial external candidate fixtures
missed catalog/floor registration by script path; correcting those identities resolved
the fixture mismatches. Failed runs exited and owner guards passed before retries.

Evidence under D:/bs-release-crew-cache-20261009/benchmark-input-isolation:
large-solar-setup-trace and solar-working-copy-trial. Focused runners under
output/renderdoc-tools-2026-10-08/run-large-solar-setup-trace.py,
run-solar-working-visual.py, run-solar-working-performance.py and its comparator.
Comparison, identities, installation, reports/logs, PNGs and owner/storage records retained.
Jobs terminal/runtime configuration restored; all owner guards2938 files unchanged.
About79MiB evidence+isolated profiles, C125.06/D74.05GiB free. No full copies/deletion.
Focused source/test diff check passes.

## Next action
Trace larger 40-room setup/content and lighting redraw costs. The local Solar saving is
only a small part of the roughly26.6ms scene average; prioritize the next measured
hotspot rather than extending this cache speculatively. Investigate remaining >50ms
frames and current completion/navigation work. Preserve selected pixels and repeat
matched comparisons for each proposed fix. Broader PC/Mac release gates remain open.
