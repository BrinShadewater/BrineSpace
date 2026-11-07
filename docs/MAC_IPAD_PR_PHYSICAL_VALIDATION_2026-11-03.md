# Merged build physical iPad validation — November 3, 2026

**Result.** The merged build passed the fresh-loop gameplay and touch-driven
Save/Continue check on a physical 10th-generation iPad.

The signed Merge QA app used the separate bundle
`com.shadewater.brinespace.mergeqa20261103` and its own save container.
The test package was built from runtime commit `8a1f6fefd` with build ID
`brinespace-e5375c2dc6db147f` and PCK SHA-256
`4d4d7f003f236707244fdabab6dbc5627a8d385b09ef80ad97fdf5a9c0013773`.
The subsequent branch cleanup affected documentation and historical artifacts.

## Device checks

1. Started a fresh loop with Major Bill using the physical iPad's touch UI.
2. Selected, rotated, and placed a Solar Array. The paid order deducted four
   metal, from 18 to 14. Resumed play, advanced opening comms, and reached cycle 1.
3. Tapped **Save Game** and confirmed the cycle 1 save message. Tapped
   **Save & Return to Title** and confirmed **Continue Loop** showed the saved
   two-room station.
4. Tapped **Continue Loop**, then the loading screen's **Continue**. The station
   resumed paused at cycle 1 with BRINE Core and the completed Solar Array.
   Tapped **Save Game** again and returned to the title screen.

The three checkpoint reads passed their integrity checks. The run ID, cycle,
exact timer, placed-room records, Solar Array rotation, resources, crew count,
blueprint hand, zoom, running flag, and selected rotation matched across the
round trip. The restored station had 14 metal and 100% integrity. All five
owner save files matched their pre-test SHA-256 hashes.

This first check covers a short fresh loop and a title-screen Save/Continue
round trip. The follow-up below covers cold relaunch and two longer runs.
Extended placement remains a separate validation item.

Local evidence is in
`/Users/Shared/BrineSpace-mac-ipad-pr-qa-20261103/touch-testing`, including
`gameplay-receipt.json`, checkpoint summaries, and touch screenshots.

## Cycle 95 follow-up

A later cold relaunch on the physical iPad restored the isolated 56-room station.
A ten-minute run at 1× advanced from cycle 69 to 95 with four crew and 100%
integrity. The cycle 95 checkpoint was then copied into separate diagnostic and
playable QA apps for the follow-up.

### Marsh recharge

The cycle 95 checkpoint had Marsh already docked at 42.8% battery with zero
reserve Power. The original movement watchdog warned about the stationary
recharge goal. The fix exempts docked Marsh from that watchdog while his trip
to the pod still uses it. The Mac battery regression reproduced the false
warning and passed with the fix. On the physical iPad, the fixed watchdog
stayed quiet while Power was empty. Adding three Power to the isolated probe
let the charging controller fill the battery and release Marsh for work.

### Wide-view fog

Fog was the only individual environment pass whose suppression lowered median
frame time against both adjacent normal wide-view samples in the diagnostic.
The candidate reuses a terrain lookup and skips lighting calculations with
zero contribution. The native Mac comparison matched all 4,915,200 pixel
channels across 16 cases.

Two same-process comparisons on the physical iPad measured wide-view median
frame-time gains of 1.3 and 4.0 ms at 56 visible rooms. The first close-view
comparison improved by about 0.7 ms. The second close-view run had one
unmatched baseline and was excluded from the paired result. Slow-frame
results varied across launches.

### Playable build and save preservation

A separate signed build, `com.shadewater.brinespace.cycle95fogplay20261103`,
used the merged runtime package with the Marsh and fog fixes and the normal
gameplay scene. On the physical iPad, touch Continue and Resume started a
600-second run at 1×. It reached cycle 125 with 56 rooms, four crew, 100%
integrity, and zero logged errors. Two gameplay performance reports captured
stretches below 20 FPS, and one recorded a 500 ms frame. Peak physical footprint
was 2,197 MiB across 572 samples. The first and last 60 samples had medians
of 2,056 and 2,160 MiB. This run began at a different cycle from the earlier
soak and cannot isolate a memory effect from the shader.

Touch **Save Game**, **Save & Return to Title**, and **Continue Loop** restored
cycle 125 paused. A fresh touch save matched the serialized station state, run
ID, and exact timer. The timestamp and crew animation playback data differed
after Continue. All five owner save hashes and all five existing Merge QA save
hashes matched before and after the playable run. An earlier environment probe
triggered a Merge QA background save and backup rotation. Its decoded primary
checkpoint differed only in save timestamp.

Local evidence is in `/Users/Shared/BrineSpace-cycle95-probe-20261103`,
`/Users/Shared/BrineSpace-cycle95-env-20261103`,
`/Users/Shared/BrineSpace-cycle95-fog-ab-20261103`, and
`/Users/Shared/BrineSpace-cycle95-fog-gameplay-20261103`.

## Branforth exploration follow-up

A Mac replay traced the route bursts to repeated dry galley approaches while
Branforth chose an exploration target. One decision made 1,300 route calls,
including 828 inside galley approaches. Several outer targets triggered the
same authored approach, and adjacent approach gates retried the same graph
joins. The fix reuses failed approaches and joins within a single decision
and retries them on the next decision. The dry routing regression, service
reachability, and crew water station suites passed on Mac.

The physical 10th-generation iPad ran a separate signed diagnostic build,
`com.shadewater.brinespace.branforthroute20261103`, using the isolated cycle 95
checkpoint and the same profile harness and camera zoom as the baseline.
Both launches advanced from cycle 95 to 99 across two 35-second windows at
1×, with all 56 rooms visible. The first paused window in each launch drew
45 rooms and was excluded from the matched comparison.

| Metric | Baseline | Branforth fix |
|---|---:|---:|
| Peak route calls in one live frame | 1,349 | 641 |
| Live frames with at least 1,000 route calls | 8 | 0 |
| Longest Branforth update | 67.02 ms | 43.28 ms |
| Median live frame time | 50.22 ms | 46.96 ms |
| 95th-percentile live frame time | 55.78 ms | 52.24 ms |
| Median paused frame time with 56 rooms | 33.34 ms | 33.34 ms |

These were separate launches, so the frame-time comparison includes normal
run-to-run variation. The fixed run still recorded a 135 ms frame with one
route call, shortly after a 69.8 ms cycle advance. The diagnostic logged
zero errors. All five owner and five existing Merge QA save hashes matched
before and after. Raw evidence is in
`/Users/Shared/BrineSpace-branforth-device-20261103`.

## Cycle 116 automatic stall report follow-up

A native sample of the 205.3 ms cycle 116 frame found checkpoint hashing,
JSON encoding, and a scene-wide input scan on the main thread before the
report reached the ZIP worker. Automatic stall reports now capture the live
station and basic input state on the main thread and send the detached
snapshot to the worker for encoding, checksumming, and packaging. Automatic
reports omit the screenshot and the full input scan. Manual F8 retains both
and keeps its own pending capture.

The physical 10th-generation iPad ran two matched 10-active-minute replays
from the same isolated cycle 95 checkpoint at 1× and fit-station zoom. Both
reached cycle 125. The signed QA candidate was version 0.3.0 (1), bundle
`com.shadewater.brinespace.lifecycleqa20261104`. Only the reporter and
performance monitor changed between the two QA packages, including timing
instrumentation in the candidate monitor.

| Metric | Previous QA package | Stall report fix |
|---|---:|---:|
| Worst whole frame | 205.3 ms | 135.5 ms |
| Whole frames over 150 ms | 3 | 0 |
| Main-thread stall watcher at cycle 116 | 74.1 ms | 37.8 ms |

The separate QA trace write took 21.1 ms on the candidate's worst frame.
All three automatic archives opened and contained a valid live checkpoint
checksum and frame diagnostics. The soak logged zero errors. All five owner
save hashes and all five existing Merge QA save hashes matched before and after.

The measured improvement applies to this paired diagnostic replay. The QA
packages contain other performance work from the investigation. Device
validation used those packages, and the branch carries the stall report fix
and its regression coverage. Local evidence is in
`/Users/Shared/BrineSpace-ipad-prerender-20261104/lifecycle-soak/worker-wait/cycle116-stall-worker`.
