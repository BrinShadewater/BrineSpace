# iPad title loading — October 19, 2026

Candidate `brinespace-efdb7ff32be59034`, source SHA-256
`efdb7ff32be59034b0cd4b5e03f3dc597de1f0dbf12d12caacafca218cefc7a4`.
Branch `codex/ipad-memory-placement-2026-10-17`, HEAD
`81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted uncommitted work.
Complete candidate, before snapshots, rejected probes, logs and device evidence:
`/Users/Shared/BrineSpace-ipad-optimization-20261019/title-load-pass`.
Prior tested `f9155b4334164440` remains complete in sibling `card-png-staging`.
Frozen Mac and Windows deliveries were unchanged.

## Change and attribution

On tablet/iOS, two bounded CPU-only jobs decode the existing title background and
silhouette PNGs concurrently. Both jobs are joined before title ready returns.
GPU creation stays on the main thread; temporary Image owners are cleared after
adoption. There is no persistent image cache, artwork change, reduced resolution,
save-format change or gameplay change. Desktop/reference remains serial. Missing
or failed prepared images use the original safe-loader fallback. This is a
loading-latency change, not a demonstrated retained-RAM reduction; simultaneous
preparation can have a slightly higher transient CPU allocation.

Native attribution found Save/main removal about54ms (Save about50ms, tree removal
about4ms), followed by a119–133ms frame. Session-art release was2.991ms, while
cover ready was47.376ms of title ready73.626ms. UI skin lookups were not the dominant
cost and were left unchanged. A disk-prepared-raster experiment was slower
(cold117ms, warm55–57ms), so it was completely reverted, including prepared-cache
edits. Rejected probes remain only in local evidence.

Alternating native serial title preparation was50.428/48.630/48.553/48.528ms;
two-worker preparation28.072/27.286/26.732/26.837ms. Native title-transition first
frame118.737→99.263ms is an observation, not proof of a physical-device effect.
The new test failed on the serial baseline, then passed. Both source pixel arrays,
composited frozen viewport pixels, desktop reference, bounded joined jobs and
empty temporary-image dictionary passed. Scoped independent review found no
actionable issue; its suggested direct lifetime assertion was added.

## Exact package

Release compilation and strict signing passed. Eight actual-PCK fixtures passed:
tablet title loading, card regions, card storage, raw texture regions(339checks),
shared room floors, hull UI(175checks), RunSave and tablet controls. Asset audit
36197selected and source audit437selected/433extras found no missing/changed or
unknown/unexpected entries. Export/app PCK SHA-256:
`0e26f3eae0ea8ebcc893838f1b003adf5f2c4e2aa4b1b6b30300b5647b1fb3a7`.
Executable SHA-256:
`f59b8543f4c0468b21ab9cb136baf2561c5cfa66008ed20a065eb67e423c4afe`.
Export configuration was restored byte-exact; temporary QA source files removed.
Native runs used isolated profiles and verified the real Mac profile unchanged.

## Physical validation

Device iPad13,18/A14/4GB/iPadOS27.2, bundle
`com.shadewater.brinespace.nativeoptimization20261017` (Validation2).
Installation preserved all five original save/checkpoint files SHA-256 exact.
Actual paused cycle64/seven-room checkpoint, normal rules and real touch UI.
No deterministic gameplay fixture was rerun for this title-only change.

Five real Save & Return to Title/Continue cycles passed without a crash, game
error or automatic stall report. Baseline title-return frames were260.016,
254.197 and236.414ms. The report retains only32recent hitches; only the fifth
candidate title transition remained:163.377ms (153.950ms before-render). Do not
present this as five timed transitions or a controlled causal comparison.
First station setup4.068s; repeat setups3.244/3.034/3.056/2.999s. First
interface/grid2.688s; this larger loading cost remains open. Automatic capture
skips paused stalls, so zero automatic reports does not certify pause-free loading.
The manual report still contains a2.401s station-setup frame.

342valid nominal1Hz samples from the one candidate process: sampled peak
1,865,780,552bytes. End-of-title samples after each cycle were834,079,904 /
836,668,600 /838,257,848 /839,158,992 /839,847,120bytes. Short trailing-five-sample
medians ranged836.7–855.4MB and include settling. The gradual5.77MB difference
between first/fifth title snapshots requires a longer test; this is not leak
clearance. The old process peak1,874,201,928bytes covered a different/longer
workload and cannot establish a RAM saving.

Actual card return, pinch zoom, rotation button, Codex scrolling and Home/activate
passed. Saved touch changes confirmed rotation1 and zoom.0708597375174268→
.219108316577404, with resources/rooms/hand/cycle/crew/speed and exact timer equal.
Two-finger pan/rotation and paid placement were not retested in the owner save.
All five originals were restored hash-exact before final owner launch. Intentional
stops caused retained recovery notices, not spontaneous crashes.

Fresh-process final Save/title/Continue/Save passed full saved gameplay-state
and exact1.11834893097652timer equality. Original cycle64/seven rooms was left
paused at4× with the menu closed. Continue's known1× reset was manually restored.
Only save timestamp/path/event history differed; final Save83.214ms, errors0.

However, that fresh-process title return again took **404.269ms**, including
387.990ms before-render, and triggered one automatic report. The following
216.687ms title-related frame is also retained; it is not a second independent
transition measurement and may include report overhead. This invalidates any
claim that all title pauses are fixed. The warmed163.377ms observation and native
CPU gain do not establish a controlled whole-transition improvement. Further
physical attribution should capture the first title return after a fresh process.
The existing authorized two-hour helper remains running.

[Portable evidence](ipad-memory-placement-evidence-2026-10-19/title-loading/ui-summary.json),
[physical cycle measurements](ipad-memory-placement-evidence-2026-10-19/title-loading/physical-cycles-summary.json)
and [remaining fresh-process title stall](ipad-memory-placement-evidence-2026-10-19/title-loading/final-owner-title-timing.json).

## Retention and remaining work

User-authorized cleanup removed only the older iOS27.0 Simulator runtime, keeping
iOS27.1 and physical-device testing. Xcode can download it again. Older life-room
and shared-floor QA packs were archived with full reconstruction hash verification;
the immutable recovery donor and both current/prior complete candidates remain.
Recovery records: `/Users/Shared/BrineSpace-workspace-cleanup-20261019-followup`.
Source, saves, frozen releases and current builds were preserved. APFS sharing
means logical archive sizes are not physical space reclaimed. About12GiB remained
free after this package; do not remove recovery donors.

The iPad is not release-cleared. Initial station interface/grid work, organic
multi-crew performance, paid placement and long-term growth still need attention.
This pass establishes no new whole-process RAM saving or whole-station initial
loading improvement. Source remains uncommitted; no upload or frozen rebuild.
