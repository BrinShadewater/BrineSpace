# Project handoff

Updated: 2026-10-16 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: Pre-render stacks, interrupts and diagnostic I/O

## Objective and acceptance

Trace unexplained primary stalls with stacks/IRQ/I/O and repeat average FPS/4×
placement benchmarks without visual or crew changes. Requested investigation and
comparisons are complete; primary cause remains unresolved because it did not
recur. No runtime fix or release acceptance.

## Accepted decisions and constraints

Keep both frozen structural lanes private/unchanged. Retain all timing rows and
automatic diagnostics. Serial visible, muted secondary-screen native runs; scratch
APPDATA/user dir and owner fingerprints. No policy, priority, affinity or power
changes. Owner authorized WPR-helper retry after Windows canceled one prompt.

## Current state

[Full results](PRERENDER_PERFORMANCE_2026-10-16.md), CURRENT_STATUS top entry and
`output/prerender-20261015/` helpers. Evidence `C:/bs-prerender-20261015/`.
No normal source/UID/test/art/crew changes. WPR stopped; helper exited; only owner
editor PID 46624 remains. Frozen base EXE/PCK files share verified hard links;
do not overwrite them in place.

4,800 stack/IRQ frames: 93,323 target samples, 87,223 measured, one measured stack
missing; 1,037,209 valid IRQ rows, zero reported loss. Main scheduled residency
99.48–99.59%; recorded same-CPU IRQ union 0.277–0.300% of measured frame time.
All 27 >50 ms frames overlap drone texture creation; no >100 ms recurrence.
Module/RVA attribution only; no matching Godot symbols. CSwitch V5 auxiliary
fields remain unverified; nine sample points outside main residency retained.

4,800 separate I/O frames: monitor body mean ~0.04 ms, worst 6.909 ms;
error polling max 6.862 ms, breadcrumbs 0.921 ms. Forced report calibration,
outside benchmarks: 362.810 ms total; PNG 264.299, diagnostics 61.984, ZIP 28.931
(inclusive scopes). It explains a report amplification mechanism, not the primary.

3,840 untraced frames/16 exact pairs: normal idle 52.24→52.71 FPS; 4× idle
45.54→45.21; 4× placement 43.15→42.61. Action mean 59.207→61.503 ms, following
>50 ms 4→6, whole placement 8→14; 0/16 60 FPS gates. Keep candidate private.

## Verification

Final audit passes: 26 owner guards, 21+21 native/water guards, 2,948 protected
files unchanged from initial/prior; original lane sources/PCKs and native binaries
identical. All three cohorts have exact state/camera pairs. Parser model19,
JSONL round-trip and interval11 checks pass; independent accounting review passed.
Prior exact visual/cache evidence reused. Earlier test-profile incident caveat
remains in `docs/TEST_PROFILE_INCIDENT_2026-10-15.md`.

## Next action

Best measured pacing target: offload lossless PNG/report packaging while keeping
snapshot content and automatic capture behavior. Primary 5.24 s/435 ms stalls
remain open; preserve ETLs and use this recorder for a future recurrence. Matching
symbols/optimized symbolized diagnostic engine would identify repeated game RVAs;
do not infer functions from unsigned module offsets or treat residency as useful CPU.
