# Packaged Windows stall attribution

Updated: October 5, 2026 · BrineSpace · PC/Mac release readiness

## Objective and acceptance

Identify the cause of the approximately one-second packaged gameplay stalls before
changing runtime behavior. Existing frame, memory, visual and native-platform
release gates still apply. This is diagnostic evidence, not performance acceptance.

## Accepted decisions and constraints

Use isolated QA copies of build `brinespace-af8b5f00998283ef`, retaining its selected
art, default effects and simulation. Do not edit the frozen Windows/Mac pair or
owner preferences. No engine upgrade, art reduction or speculative runtime fix.

## Current state

Diagnostic helpers and raw results are under
`output/stall-attribution-2026-10-05/`. No production runtime changes this interval.
The QA reporter loads a derived performance monitor which records inclusive
monitor/report spans and a clock correlation. The external process sampler records
CPU time, page faults, memory, I/O and device-wide NVML data every 100 ms.

## Verification

- `probe-r2`: worst frame 945.367 ms, including 893.191 ms after the render
  signals. Overlapping monitor work at most 0.016 ms; no recorded report span.
  Bracketing 1.104-second OS samples show 0.188 CPU seconds, zero page faults and
  zero I/O bytes. Focus remained true.
- `probe-gpu`: worst frame 989.338 ms, including 933.119 ms after render signals.
  Monitor work 0.058 ms. GPU utilization drops to zero through most of the stall;
  this is a symptom, not proof of a clock/power-management cause. Peak device-wide
  GPU allocation is 7,218.762 MiB out of 12,282 MiB. No evidence of VRAM exhaustion
  in this run. Overall texture-budget failure remains independently unresolved.
- `audio-dummy`: a 1,030.846 ms stall remains with the real audio backend excluded.
- `accessibility-off`: a 945.179 ms stall remains with accessibility disabled.
  Both controls record an uncapped engine and low-processor mode off. These are
  QA command-line controls; shipped preferences remain unchanged.
- `probe-stacks`: 16 bounded native main-thread context captures. The longest
  frame is 934.412 ms. Captures at offsets 159 and 463 ms are in
  `NtUserPeekMessage`; at 664, 765 and 867 ms they are in `NtUserMessageCall`.
  The 911.677 ms and 882.013 ms frames also contain message-handling captures.
  A separate 385.911 ms frame has two captures in
  `NtGdiDdDDISubmitCommandToHwQueue`. This distinguishes at least two stall paths.
- `probe-stack-modules` repeats the message-path observation: an 887.845 ms
  frame includes captured instruction pointers in `NtUserSystemParametersInfo`,
  `NtUserMessageCall` and `NtUserPeekMessage`; an 894.008 ms frame also contains
  `NtUserMessageCall`. Advisory caller chains resolve to Windows `user32.dll`,
  `SHCORE.dll` and `uxtheme.dll`. They do not identify a third-party hook. Six
  earlier captures fall outside measured action frames and are excluded from
  action attribution. The owner check again reports 2,936 files, zero changes.

The stack sampler resumes the target immediately after obtaining its register
context, before unwinding. The instruction pointer is captured while suspended;
caller chains are advisory because the stack can subsequently change. Some
unwinds contain invalid addresses. Large export-symbol displacements are not
exact function identifications. Recorded `CallNextHookEx` callers warrant a
follow-up but do not establish which hook or component caused the wait. Maximum
measured suspend/context interval was 0.120 ms. Symbol initialization and external
sampling overhead prevent using these runs as matched performance comparisons.

Scratch APPDATA and the maintained runner protect the owner profile. The first
temporary wrapper failed to parse and was discarded; its owned child was stopped.
Successful runs and profile checks are retained separately. All 2,936 non-log
owner files remained unchanged in the completed stack run.

## Next action

Follow-up evidence now identifies the screen-reader status query, reproduces its
latency outside Godot and reproduces long stalls in a bare scene. Continue from
`docs/WINDOWS_QUERY_STALL_2026-10-05.md`; the earlier results above remain valid
within their stated sampling limitations.

Obtain a coherent wait/stack trace around message handling and system-parameter
queries. Inspect window-message triggers against the exact engine revision;
do not infer function identity from the nearest exported symbol. Establish whether the message-hook
path is environmental before editing game logic. Investigate the separate GPU
submission stalls and excessive texture storage independently. Re-run matched
uninstrumented workloads only after a justified change. Windows performance,
minimum hardware, Mac native testing, Developer ID signing/notarization and the
remaining gameplay/endurance gates still block release. No upload occurred.
