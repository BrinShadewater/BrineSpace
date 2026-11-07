# Project handoff

Updated: October 9, 2026 - Project: BrineSpace - Task: worker wait/upload/peak attribution

## Objective and acceptance

Continue full PC/Mac optimization/release-readiness. Diagnose private worker tail
regressions and texture peak increase before admission; preserve current-frame
pixels,timing,simulation and owner data. Normal source remains unchanged.

## Accepted decisions and constraints

Keep worker prototype private. Additive bounded diagnostics only: per-frame scalar
worker totals,existing post-render texture sample reused in trace,new-peak event
list capped128. No repeated script hashing/full inventories per frame,no quality
or renderer change. Shared private navigation/storage/drone controls remain.

## Current state

Actual debug=false1080p40room candidate-first/reference pair,3000idle frames/lane.
Visibility-safe sources are byte-identical to preceding reverse trial;only adapter
instrumentation changed. Delta cumulative worker waits across successive measured
rows,excluding first row(warm totals),gives median3us,p997us,max25,274us. Reference0.

Candidate worst frame4x653144.495ms has wait4us,
scriptdraw71.778ms and275.625MiB current-frame drone uploads. Other4x905105.645ms
has wait4us/zero current uploads (full-graph event previously observed). One distinct
4x31497.558ms frame has25.274ms worker wait,draw49.073ms and137.813MiB current uploads.
Thus normal waits are tiny,but rare long wait exists;largest stall isn't a worker
join in this trace. No queue-vs-build cause established without worker timestamps.

The candidate's texture peak2408.880MiB repeats baseline2346.502+62.377MiB. New
peak event at engine process2496;trace first shows it next row4x315(process2497,
sampled2496),following the large wait row. This offset is documented:process and
sampled-process ids differ by1,post-render texture sample can appear in following
collection row. Do not equate phase-local frame numbers with GPU render ids.

Peak neighborhood: candidate begins wheel-south/unload-south-cargo uploads at
sampled2495 vsreference2496. Next batch includes start-north,steer/wheel-east and
unload-south;candidate texture holds2408.880 for two sampled rows vsreference
1980.125MiB at corresponding collection row. Both settle to2041.38MiB soon after.
This associates peak with shifted sheet upload/lifetime timing,not proven resource
identity overlap or worker-caused VRAM allocation. Workers themselves emit numeric
commands only and don't create textures.

All compared phase/final gameplay endpoints equal;6238jobs joined/active0/peak2,
4074uploads each,settled end1916.471/exit228.259MiB match. Candidate means38.00/38.83/
40.75ms vsreference41.16/42.57/42.79ms. Diagnostic results still fail full release
gates;instrumented comparisons do not establish new admission or endurance.

Evidence:D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/water-worker-attribution/
(analysis.json,peak-neighborhood.json,raw traces,source identities,logs/profiles).
Changed checkout files:this handoff and CURRENT_STATUS.md only.

## Verification

Compiled source/branch checks pass,native debug=false/focused/logs clean,no missing
art,all3missions return/unload/fullgraphs recover,owner2936non-log files unchanged,
all processes terminal,adapters restored/router releases. Existing native598checks
are prior revision coverage,not repeated for unchanged measured rendering code.
Collection_usec currently evaluated before new trace fields;it doesn't include
all new getter overhead. Bound that overhead explicitly in next instrumentation.

## Next action

Add per-job submission/start/end timestamps to distinguish queue delay from worker
build/allocator contention,read only after join. Measure getter overhead separately.
Capture bounded live sheet/lease/eviction identities around the peak to determine
actual retained GPU-storage overlap. Then test measured scheduling/retention remedy
in matched actual workloads;don't guess high-priority scheduling is a fix. Preserve
fallback/visibility/settings/lifecycle safeguards. Continue independent upload/
navigation stalls and complete original Windows/Mac release scope.
