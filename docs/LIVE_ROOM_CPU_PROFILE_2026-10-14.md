# Project handoff

Updated: October 14, 2026 · Project: BrineSpace · Task: live-room drawing and CPU

## Objective and acceptance

Profile the current wall-batched Windows runtime, then test CPU reductions toward
60 FPS without changing art, animation, layout, compositing or simulation. Require
matched states/cameras, native pixels and measured CPU benefit for admission. Treat
whole-frame pacing and the 60 FPS gate separately from a local CPU reduction.

## Accepted decisions and constraints

Godot 4.7.2 Compatibility, RTX 4070 Ti, fitted 40-room mixed-large station at
1920x1080, four large rooms and active crew/drones. GPU work serial, muted secondary
display, viewport input disabled. Scratch APPDATA, resolved user-directory checks
and owner fingerprints. No gameplay/quality changes, refactor, commit or publication.

## Current state

The companion CPU cleanup is installed in source. Base delivery remains
`brinespace-2fb8e8659a3be093`; the physical QA copy and overlays are separate under
`C:/bs-live-cpu-20261014/`. Drivers: `output/live-cpu-20261014/`.

Three drawing candidates are rejected. `scripts/companion_npc.gd` now reuses the
topology check within one synchronous update; direct helper callers still validate.
No persistent cache or rendering changes. New `tests/test_companion_topology.gd`
and paired UID cover the contract, registered in the companions and performance-
diagnostics groups. Existing script UID retained. No Windows export this task;
the installed source change is absent from the existing Windows candidate.

## Verification

### Attribution

Instrumented current-release idle 1x: live-room callbacks ~6.39 ms, including large
base callbacks ~2.05 ms; ordinary retained content draws ~1.94 ms. Door/light
validation ~1.25 ms and surface validation ~0.58 ms. Pan retained animation advance
~0.385 ms, submit ~0.410 ms, library-live paints ~1.77 ms. Nested costs overlap;
these values must not be added as independent frame costs. Instrumentation has overhead.

Simulation step ~2.225 ms; crew snapshot ~1.458 ms, drones/wrecks ~0.210 ms,
airlocks ~0.133 ms, interface ~0.104 ms. Snapshot scopes differ from render intervals.
Initial content timer totals include startup carry-over and are excluded; pan values
above use the drained per-sample counters. See `profile-summary.json` / `profile.json`.

### Large-canvas ordering trial: rejected

Avoiding repeated move-to-end operations preserves exact final child order and skips
stable tree moves (25 structural checks). Pilot provides no speedup in matched phases.
Its late viewport changed from 1328x920 to 1328x1359, so the full timing comparison
is invalid and excluded. Original source is retained. Subsequent fixtures set the
unresizable style before assigning window size and reject any later size change.

### Retained advance-slot index: rejected

Index live/library-live/frozen slots during submit, preserving visibility checks,
hidden tails and the all-slot wet-material update. Red/green edge tests pass 20 checks;
initial prototype fails two additional hidden/reclassification cases before correction.
Twelve whole-station native frozen comparisons at three zooms are byte-exact.

An exploratory nine-phase pair improves 27.309 -> 27.067 ms, but final full-action
comparisons fail repeatability: 26.679 -> 26.737 ms (-0.22%), reverse order
27.113 -> 26.624 ms (+1.80%). 15,120 frames, all 42 states and cameras exact,
unchanged settled texture counter 1,946.077 MiB, still 0/42 candidate phase gates pass.
P95 improves 9/21 and 12/21; candidate worst frame is 107.190 ms in the first pair.
The first pair saves ~58 us in live-room callbacks while increasing content preparation
~9 us. This small local reduction does not establish repeatable FPS or pacing benefit.
`advance-v2-fullanalysis.json` records both comparisons. No index code is installed.

### Large-context identity trial: rejected

LargeRoom.Context advertises `props_rebuilt_each_configure` although Studio.live_props
explicitly shares immutable dictionaries until revision/cache replacement. Removing
only that opt-out allows the existing cheap slot-key path; Cryo's separate opt-out stays.
No new cache or array index. Private submit contract fails before and passes after:
35 checks for prop ownership/identity, wrapper reuse, replacement, operating/quarter/
apply-serial invalidation, input immutability and the independent Cryo behavior.
Nine exact state/camera pairs: 27.350 -> 27.260 ms (~0.33%), p95 improves 5/9.
Large-prop callback reduction is only ~7 us on average, with mixed whole-frame phases.
This is below useful attribution confidence; no production admission or native
appearance acceptance is claimed. Further full-action runs were not justified.

### Companion topology: small CPU cleanup admitted

An instrumented Main-only current-release run separates crew costs at 1x/2x/4x:
companions ~612-633 us, Branforth update ~273-301 us, Branforth preflight topology
~159-166 us, hazards/repair/construction ~186-190 us, passage ~48 us; other
preflight/social groups are small. Margot and River each perform two topology reads
per update; Branforth performs one preflight and one nested update read. `crew-analysis.json`.

Companion update validates topology, handles fire safety, then its internal behavior
helper validates again. FireSafety.advance's false returns precede mutations; true
returns bypass the helper. Rebuild ends by refreshing signature/locked cells.
Candidate passes a checked-state argument along this synchronous path, keeping the
helper's default live validation for direct callers. No persistent topology cache.
Independent source review found no intervening topology mutation. Initial guard
fixture parse error (override signature) is excluded; corrected original fails four
expected redundant-read checks, candidate passes 21 checks. Expanded installed test
passes 25 checks, including lock changes, direct calls, inactive/paused/stopped/zero-
delta exits, fire retreat and Josh water powerdown. Existing companions, companion
water, personality and repair tests all pass with zero failures. Water/personality
fixtures report shutdown CanvasItem/ObjectDB leak warnings; no script errors.

The initial release adapter correctly rejects cached old companion source. BugReport's
compile-time preload chain reaches Companions through PerformanceMonitor/Bill/WardRepair.
A QA-only early pack proxy now mounts before those scripts compile, verifies scratch
profile, installs the original guarded reporter, and lazily loads fixture dependencies.
One proxy parse error and one lifecycle exit are excluded. Source hashes are checked
after Main loads; final runs also check each actual companion instance. The proxy
mounts in its constructor, then installs/calls the guarded reporter on tree entry;
all fixture preloads become lazy for this comparison. Production BugReport and
delivery files are unchanged. Valid mounted pilot: nine exact states, means
27.248 -> 27.085 ms, idle 1x 24.222 -> 24.019 ms; p95 improves only 3/9.
Instrumented companion work falls from 632.556 to 402.533 us at 1x (~36%), with
Margot and River each reading topology once instead of twice. This is a component
CPU result, not a whole-frame percentage. See `crew-topology-analysis.json`.

Two full pairs cover idle, pan, zoom, lighting, placement, demolition and interface
at 1x/2x/4x, 180 frames per phase: 15,120 valid frames and 42 exact state/camera
pairs. Means are 26.735 -> 26.437 ms (1.11%) and 26.704 -> 26.661 ms (0.16%).
Idle 1x is mixed: 24.289 -> 24.521 ms and 24.261 -> 24.165 ms, still about 41 FPS.
P95 improves 27/42 phases; candidate passes 0/42 of the 60 FPS phase gates.
Settled texture counter remains 1,946.077 MiB. Second pair uses the valid reference
retry: its original reference was minimized and rejected; the completed candidate
remained valid and all 21 states/cameras match the retry. See `companion-fullanalysis.json`.

Lighting p95 worsened in both full orders, prompting two focused 360-frame pairs.
One is nearly flat; the other candidate has broadly slower CPU drawing and GPU
timings despite identical state and draw counts. The cause is unresolved. These
results do not establish a pacing/stutter improvement; the admitted change is scoped
to the verified local CPU saving. See `companion-lighting-analysis.json`.

Twelve adjacent native frozen-image comparisons at fitted, 0.25 and 0.5 zoom are
byte-exact, after draining drone texture jobs. The fitted capture was visually
reviewed. This establishes frozen-image parity, not every animation frame.
`companion-parity.json` records the comparisons. Runtime source and actual companion
instance hashes were verified. Installed source matches the measured candidate:
SHA256 `768dcb8314d5defaae94a3a5b1af5d4b871d9888db337999938d005c9d2cd775`.
See `admission.json`; all private rendering candidates remain excluded.

All 61 completed owner guards preserve all 2,948 files. Installed test logs contain
no script/engine errors. Independent final source/test/index review found no
actionable issues; scoped whitespace checks pass. Failed/invalid attempts remain
separate from accepted evidence. The previous Windows candidate is intact.

## Next action

The next drawing targets remain large-room base callbacks (~2 ms), ordinary retained
contents (~2 ms) and door/light validation (~1.25 ms); retain exact compositing and
animation. Branforth's preflight topology (~160 us) is another CPU target, requiring
the same complete-input/locked-cell contract. Earlier rejected Tidal/static splits,
waveform triangles and this task's three drawing candidates must not be repeated
unchanged. No further optimization experiment is pending in this task.

Full 60 FPS, endurance, save/relaunch, target-PC and native-Mac acceptance remain open.
