# Project handoff

Updated: October 15, 2026 | Project: C:/Users/Alex/Documents/Brine Space | Task: render submission/draw calls

## Objective and acceptance
Completed bounded drawing trial and large-station FPS/4x hitch comparison with
exact visual/state acceptance. Actual steady draw calls fall ~8 (0.4%); no useful
FPS/hitch improvement established. Keep waveform trial private, normal runtime unchanged.

## Accepted decisions and constraints
Reference includes prior private water V2, stable-ID V3, LOD/one spare. New reference
adds unchanged prepared screens as explicit file 23; other 22 match previous candidate.
All game runs serial and isolated; preserve every valid run/regression. No normal
native installation/export/Mac/package/commit/upload. Preserve crew, command/blend
order, all animation clocks and prop depth. Initial Node.hide/show attribution
invalidated retained commands and was discarded; raw RID visibility restores exactly.

## Current state
[Results](SUBMIT_CALLS_PERFORMANCE_2026-10-15.md). Evidence:
C:/bs-submit-calls-20261015; helpers output/submit-calls-20261015.
Only frozen prepared_library_screens.gd differs: final waveform AA trace uses
existing ordered stroke packet, same vertices/colors/order. Prepared owns bounded
topology; native absent uses script packet, rejection original polyline. Existing
water/stable native source/DLLs unchanged. No installed game source/UID/test changed.
Project docs: results, this handoff, CURRENT_STATUS top milestone, submit-calls plan.

## Verification
Native and script fallback each 369 checks / 186 exact raster pairs; physical 18 to 14 call
check for two waveforms. Correct RED screen-red2 observed; initial screen-red parse
error not acceptance. 1,920 guarded production frames / eight exact phase-state and
camera-path pairs. Normal idle 55.93 to 55.71 FPS; 4x idle 49.11 to 48.98; 4x placement
45.68 to 45.91. 4x action 56.857 to 55.660 / 55.758 to 56.726 ms; forward following p95
32.965 to 41.082 ms, reverse 35.882 to 31.956. One  >50 ms following frame in each lane,
two including action; 0/8 60 FPS gates. Seventeen station/first-paint pairs and 12
repeats exact; image inspected. Actual runtime PreparedScreens preload hash and
native packet counts confirm execution. Read-only review no blocker. Final audit
passes, all 19 owner / 11 stable / 11 water guards clean, final 2,948 files equal initial/prior
protected baseline. Existing incident caveat remains. Engine texture counters do
not establish native/RSS/long-soak acceptance. Only owner editor PID46624 remains.

## Next action
Raw RID probes calls2 / calls3 restore 2,114 root calls after every hide. LiveContents 442,
walls 200, terrain 156, floors 148, foundations 143 are marginal differences, not an
additive cost partition. Visible 24 eligible live slots sum 47 marginal calls and
have no specimen effects; proposed nine-circle packet NOT implemented. Next
inventory texture/material transitions in static props/structural groups, then
prototype one busy room's ordered batching or bounded atlas with pixel/sampling /
memory acceptance. Do not repeat monitor/absent-effect timing without new evidence.
Copied old native manifests retain original descriptor paths; native-snapshot.json
records relocated descriptor hashes, source/DLL still original. reference22.pck
preserves prior water candidate for diagnostic provenance.
