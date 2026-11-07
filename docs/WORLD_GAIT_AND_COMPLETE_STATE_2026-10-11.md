# World gait input installed; provider state blocker and survey fixture findings

Updated: October 11, 2026 · Project: BrineSpace · Task: PC/Mac performance readiness

## Objective and acceptance

Continue the complete performance/release plan. Install a verified animation-input bug
fix, remove the observed provider gait-phase mismatch without epsilon, and strengthen
the benchmark's checkpoint coverage/determinism. Renderer admission, frame gates and
platform certification remain incomplete.

## Accepted decisions and constraints

Animation distance comes from the physical foot before camera projection. Rendering
coordinates, source anchors, selected artwork, stride/timing declarations and historical
player/save identifiers stay unchanged. Keep indexed21 private. All tests muted on the
secondary display, input blocked, scratch APPDATA and owner fingerprints preserved.
Fixture survey-clock changes do not change gameplay survey code. Retain failed evidence;
do not retroactively declare earlier partial checks complete.

## Current state

Installed `scripts/grid_canvas.gd`: helper plus three Branforth playback inputs use
`foot / 384 - Vector2(0, .038)` directly. Bytes match the measured canonical grid.
New `tests/test_world_gait_input.gd` and paired engine-generated UID, registered in crew
and render-perf with a headless override. Existing UIDs/unrelated worktree edits retained.
Installed-source test passes 49 checks: physical input, zero stationary phase under
zoom, repeated paused sample and exact restore; fixture also reproduces old round-trip
error. No export, commit or upload.

Private indexed grid rebased onto current workshop retention/case/camera behavior and
the same canonical gait fix used by normal reference. Resources reuse existing encoded
art; no art rewrite or full source/package duplication.

## Verification

Actual selected bare/helmet cardinal walk banks: 144 cases / 10,224 sampled frames at
30/60/120 simulation-step rates and 1x/2x/4x, stationary/moving feet, repeated paused
samples and 144 playback restores. Helper equals canonical control; selected Texture2D
identities and playback snapshots match exactly. Live actor playback unchanged. This
is selected-bank/state coverage, not native frame-cap/focus or full save/Continue certification.

18 debug=false RTX 4070 Ti / 1080p native runs, three alternating pairs each on reported
12, frozen current 10 and deterministic expanded 40: 19,440 measured frames. All 108
paired phases match the older selected checkpoint subset exactly, including the six
previous Branforth gait discrepancies. All cameras and indexed backend scans pass;
no duplicate indexed/original storage or fallback draws in these default-filter runs.

| Map | Normal -> indexed mean ms | Texture MiB normal -> indexed | >50 ms frames |
|---|---:|---:|---:|
| Reported 12 | 12.354 -> 12.560 | 1558.872 -> 1528.343 | 0 -> 0 |
| Current 10 | 12.081 -> 12.122 | 1940.831 -> 1911.626 | 0 -> 2 |
| Expanded 40 | 25.532 -> 25.604 | 3028.007 -> 2629.355 | 54 -> 35 |

No measured frame over 100 ms. Large texture saving 398.652 MiB (13.17%); decoded upload
bytes 22017.000 -> 14750.918 MiB (33.0% fewer cumulative bytes), texture-creation CPU
2038.893 -> 1470.215 ms (27.9% lower). Mean FPS does not improve; p95 41.430 -> 41.358,
p99 53.958 -> 51.405 on large. Release frame gates remain failed. Current candidate's two
>50 ms frames remain to investigate. These are reused base PCK + current source overlays,
manual fixed-step/dedicated fixture economy, not frozen release or target-hardware evidence.

First provider visual pair: 27/28 exact, old 8,879-pixel boundary discrepancy remains.
Terrain trace rerun: 24/28 exact, four additional 4x pan/zoom differences. Inspection maps
the first extra difference to basalt cell (26,21), not an ordinary wreck. Node transforms
and last-painted size alone are insufficient to explain the output.

**Harness gap found:** previous matched_state omitted top-level checkpoint terrain,
surveyed water, RNG, comms and other fields. Do not treat its 108 matches as full-save
identity. Expanded capture uses all RunSave.capture fields except wall-clock saved_at.
A new paired trace has 28/28 image hashes and rock mesh/texture contexts exact, but 0/28
complete checkpoints match: differing fields are only surveyed_water cells. This is a
newly exposed blocker, not an accepted waiver.

Survey is throttled by Time.get_ticks_msec() at 250 ms while the benchmark advances
simulation with fixed deltas. Rendering/loading wall duration therefore changes when
it surveys moving lights. Surveyed-water memory feeds the green channel of the fog mask,
so output can differ with equal camera/light/terrain geometry. A fixture-only visibility
module substitutes round(unscaled simulation seconds * 1000), preserving the 250 ms
threshold. With that single clock correction: 28/28 complete checkpoints, image hashes,
exact terrain transforms, submitted/drawn mesh vertex/index/UV hashes and texture bytes
all match. This supplies concrete harness evidence; it does not retroactively certify
all older unexplained images or actual gameplay across FPS/platforms. Gameplay survey
clock remains unchanged.

Prepared (not started) `run-world-gait-indexed-complete-maps.py` and comparator use full
checkpoint capture and deterministic fixture survey clock for the next repeated gate.
The earlier performance table uses the original survey clock; do not silently substitute
the diagnostic results or claim full-state acceptance for those runs.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`world-gait-input`, `world-gait-indexed-real-maps`, `world-gait-indexed-pixels`,
`world-gait-indexed-terrain-trace`, `world-gait-rock-state-trace`,
`world-gait-survey-clock-trace`. Corresponding runners in
`output/renderdoc-tools-2026-10-08/`. 473.55 MiB added; last two traces save only suspect
PNGs while retaining all hashes. C 124.23 / D 70.84 GiB free, maintained 20 GiB floor.
Owner guards 2,938 unchanged. All jobs terminal; original QA override restored.

## Next action

Run the prepared complete-state repeated comparisons once, then proceed with indexed
filter/mipmap/flood/fallback/loading/late-work/session ownership and lifetime tests.
Keep required crew ready before gameplay and verify original frame identities/metadata.
Test repeated title/game/Continue resource release before any production renderer admission.
Review remaining fog discrepancies against complete survey state instead of uninstrumented
reruns. Actual gameplay survey/FPS behavior stays separate from fixture determinism.

The full plan remains: larger frame-time remedies, complete workload/resolution/target
hardware evidence, diagnostics/autosave overhead, endurance and original packaged bugs,
Windows release acceptance and Apple Silicon gameplay/Retina/input plus signing/notarization.
No Mac candidate or public release is certified by this milestone.
