# Save fingerprint cost — October 16, 2026

Production Save falls from **62.331–65.122 ms to 11.724–11.815 ms** in the three
per-speed diagnostic samples, an **81–82% reduction**. The unchanged four-run
40-room fixture independently measures Save action frames falling from
**95.836–113.938 ms to 42.521–51.259 ms**. Those fixture frames include an immediate
verification readback as well as rendering; they are not pure production Save time.

Private Windows candidate **brinespace-d3cfa1890bafefe7**:

- Physical source: `D:/bs-save-hitch-20261016/source/`.
- Delivery: `D:/bs-save-hitch-20261016/windows/BrineSpace.exe` and adjacent PCK.
- Source SHA256: `d3cfa1890bafefe7e5b1a8c4e3f4f01f52e19d1e250701c27832d52b675e7514`.
- PCK SHA256: `49a95db92f2382f52b56034a5af4515746a464d2695e2aa1e150ca83d0c09b12`.
- Baseline: preserved e54e8a0eb8d58f65 from [the previous Windows validation](FIXED_RELEASE_VALIDATION_2026-10-16.md).

This freezes the accepted e54 source selection plus this narrow fix. No commit,
upload or release promotion. Original Windows/Mac deliveries remain preserved.

## Attribution and change

The expensive work was repeated decoding and hashing of the same compressed James
cargo frames. Even an empty return plan binds the complete two-gear bank: 26
bindings, sharing 24 unique compressed frames. Its fingerprint pass cost
**50.310–52.176 ms**. Base capture was approximately 1.1 ms, validation 2.8–2.9 ms,
serialization/checksum below 1 ms each; individual file replacement stages were
submillisecond in these samples. Disk writes were not the dominant cost.

Three runtime files change relative to e54:

- `scripts/crew_storage/frame.gd`: retain one legacy byte digest per compressed
  source, with an owned exact compressed-byte copy and reconstruction-layout key.
  Pixel replacement or in-place edits invalidate it. No decoded Image is retained.
- `scripts/james_cargo_checkpoint.gd`: reuse that digest only for CpuFrame sources,
  including their CanvasTexture wrapper. Other/mutable textures keep the fresh
  hash path. Pivot, height, timing, gear, stage, clock, return plan, floor pixels
  and floor PNG identity remain freshly captured/validated.
- `scripts/grid_canvas.gd`: prewarm the fixed bank after compressed source adoption
  during existing loading, so the first real Save receives the same benefit.

Schema, binding/version strings, legacy digest encoding, backup/error handling and
crew/render logic are unchanged. No artwork changes. The measured owned key copies
total **490,230 bytes (478.7 KiB)** across 24 sources at every diagnostic speed.
Per-resource cache metadata adds overhead beyond that byte count; this is not an
OS memory measurement. There is no decoded-image cache, global history or new GPU
texture cache. Original fingerprint computation still occurs once during loading.

| Profiled work | e54 baseline | Candidate |
| --- | ---: | ---: |
| Actual production Save | 62.331–65.122 ms | 11.724–11.815 ms |
| Diagnostic capture | 54.512–56.733 ms | 4.033–4.164 ms |
| Complete bank fingerprints | 50.310–52.176 ms | 0.125–0.142 ms |
| Immediate production readback | 8.364–10.168 ms | 9.574–11.668 ms |

One diagnostic Save per speed (1×/2×/4×), same external fixture. The instrumented
RunSave copy adds clocks and extra writes, so its phase FPS/maxima are excluded
from headline performance. Instrumented packets equal production packets at all
three speeds after removing only saved-at/path fields. Evidence: `profile-v2-stages.json`
and `candidate-profile-stages.json` under `D:/bs-save-hitch-20261016/`.

## Primary benchmark

Godot 4.7.2 Windows release, Compatibility/OpenGL, RTX 4070 Ti. Same corrected-v3
fixture bytes (`3a98f6bcff0744276c973da28fc38c67c7d09d159896bbb3d2ca1bde348c38de`),
camera/recovery fixture, 40-room composition and four active actors as the preserved
baseline. Two runs each at 1600×900/1920×1080, eight actions at all three speeds:
**four valid candidate runs, 96 phases, 11,520 measured frames**. Dedicated manual
simulation/free-building fixture, with normal flags restored for each actual Save.
OS/disk cache uncontrolled; this is not ordinary recovery gameplay certification.

| Metric, range across four runs | e54 | Candidate |
| --- | ---: | ---: |
| 1× idle FPS | 44.97–45.69 | 46.51–46.95 |
| 4× idle FPS | 40.35–41.43 | 41.23–42.56 |
| 1× zoom FPS | 37.17–37.93 | 34.37–38.65 |
| 4× zoom FPS | 35.57–35.93 | 36.26–36.92 |
| Save action frame, all speeds | 95.836–113.938 ms | 42.521–51.259 ms |
| Save action CPU including readback | 72.187–80.732 ms | 20.731–22.625 ms |
| 4× placement action frame | 53.069–60.336 ms | 52.781–54.851 ms |
| Max of following 60 placement frames, 4× | 35.988 ms | 39.976 ms |

All four 4× placement action frames are lower in this cohort; their action CPU
costs are **2.322–2.580 ms** versus 2.323–2.390 ms. Following 60 frames have zero
>50/>100 ms frames in both builds. Placement-phase p95 is **34.416–38.116 ms**
versus 33.853–35.897 ms: lowering the action peak does not establish a general
placement-pacing improvement.

All outliers remain. Candidate has **49 >50 ms / one >100 ms** frame, baseline
68/eight. The candidate's **100.372 ms** maximum is 4× idle, not Save. The baseline
idle maximum is 89.424 ms, with the pre-existing idle-burst investigation still
open. One candidate repeat has 1× zoom/placement FPS 8.2%/8.8% below its preserved
pair. Draw counts are effectively identical; several CPU stage and render timings
rise together during that sequence. This does not identify an OS/driver cause or
prove a patch-induced regression. Do not attribute small steady-state gains to a
cache that runs during loading/checkpoint work.

Peak reported texture memory is byte-identical per paired run, **2602.2–2609.0 MiB**.
First-load scene-request-to-ready remains **10.613–11.429 s**; repeat loads
5.252–5.267 s. Cache/OS conditions differ from a true cold boot. Loading and all
96 strict 16.7 ms pacing gates remain open; this is not large-station 60 FPS acceptance.
Raw cohort: `candidate-v1/`; analysis: `benchmark-analysis.json`, `phases.csv`,
`actions.csv`, `paired.csv` under the evidence root. Preserved baseline:
`D:/bs-release-validation-20261016/mixed-fixed-v1/`.

## Follow-up variation check

Contemporary e54 then candidate, two 1920×1080 runs each, full unchanged fixture
including first/repeat loads: **four valid runs, 48 phases / 5,760 frames per build**.
This cohort remains separate; no original outlier is replaced.

| Follow-up metric | e54 | Candidate |
| --- | ---: | ---: |
| 1× idle FPS | 45.65–45.93 | 44.66–45.33 |
| 1× zoom FPS | 37.81–38.48 | 36.98–37.03 |
| 1× placement phase FPS | 38.93–45.65 | 43.73–44.15 |
| 4× idle FPS | 40.95–42.34 | 40.73–41.16 |
| 4× zoom FPS | 35.71–35.85 | 35.83–35.85 |
| Save action frame, all speeds | 92.133–109.854 ms | 42.840–52.244 ms |
| Save action CPU including readback | 70.784–75.701 ms | 21.068–23.215 ms |
| 4× placement action frame | 52.690–54.081 ms | 54.236–54.461 ms |

The Save benefit repeats. The original 8–9% candidate warm zoom/placement drop
does not repeat as a consistent pattern: the old build itself has a slow warm
placement sequence (35.651 ms p95), while candidate placement p95 is
23.672/24.288 ms at 1×. However several candidate ordinary phases are 2–4% slower
in this later cohort; primary idle differences went the other way. These samples
do not establish a steady-state FPS gain or a blanket absence of small regression.
There is no new cache call in drawing or ordinary simulation; attribution remains
limited by variation across multiple untouched CPU stages and uncontrolled clocks/OS.

Follow-up idle maxima: baseline **90.124 ms**, candidate **79.583 ms**. The original
100.372 ms candidate frame remains in the primary results. Follow-up candidate
placement phase also contains **64.101 ms at frame 96**, with 0.003 ms action CPU,
outside both the frame-30 placement and following-60 interval. Nothing is excluded.
Following 60 frames after 4× placements peak 37.242 ms, with zero >50 ms frames.
Evidence: `baseline-followup/`, `candidate-followup/`, `followup-analysis.json`.

## Correctness and package verification

New `tests/test_cargo_binding_cache.gd` + paired engine-generated UID: **18 checks**,
first demonstrated repeated decoding, then passed. Covers complete legacy digest
equivalence, reused values without image reads, whole/in-place compressed changes,
wrapper replacement, raw LA8 bytes, mutable-texture fallback, fresh metadata and
timing, detached packet/plan state and unpoisoned subsequent captures. Save test
index updated. `test_run_save` and `test_save_integrity` pass.

Native `test_crew_pose_cache` and `test_crew_router_pixels` pass. Normal cargo
checkpoint probe: **424 checks, ten cases, 30 presentations**, both gears and
before/after/midpoint/terminal/idle phases. Real Save/read/strict admission/staged
restore, exact restored source pixels/clock/contact/plan/room ownership, finite
completion and negative binding trials pass. Two restored world captures were
visually reviewed. Independent read-only review found no concrete remaining issue
after the owned compressed-key safeguard.

Short actual normal-process packaged 12-room 4× canary: **60.014930 s, 3,598 frames,
39 checks pass**, mean 59.9517 FPS, p95/p99 16.781/17.142 ms, max 38.045 ms;
zero frames ≥50/100 ms and all interval flags zero. Normal costs/failures/process
flags remain intact; Save/readback, Return to Title, gameplay scene release and
normal Quit pass; no logged errors. All 13 router censuses have zero expired
references. This is a short correctness check, not a new two-hour soak or a strict
16.7 ms gate pass. Earlier two-hour acceptance belongs to e54.

Maintained exporter passes. **36,430 manifest entries**, exactly the three scripts
above changed, none added/removed. Exact asset audit: 35,942 checked, zero missing,
changed or unexpected. Packed source audit: 431 selected + 421 additional frozen
scripts, zero failures/unexpected; all additional scripts unchanged from e54.
`minimal-runtime.patch` records the runtime delta. Physical source inputs and full
Git index/tree verification are recorded in `source-inputs.json`.

Retained harness issues: the first profiling transformation refused an ambiguous
match before launch. The old cargo harness opened a second game before freeing
the first; the external adapter now waits for observable scene/router teardown.
Its native run passed 424 checks; a Python post-check miscounted 40 result records
as ten cases, corrected offline into ten checkpoint results plus 30 presentations.
Raw failures and corrected verification remain; no production router change was made.

## Remaining acceptance and preservation

Final owner/delivery/storage guards are recorded in `final-guards.json` in the evidence root. No tests
target the player's profile. QA binary duplicates are removed only after hash
verification against the preserved canonical candidate; helpers and evidence stay.

Rare idle stalls, general large-station render/CPU costs, loading and target-hardware
acceptance remain open. The owner-run Mac ZIP is still preserved e54
(`D:/bs-release-validation-20261016/mac/BrineSpace.zip`); it does not contain this
new Save patch. No new Mac build/native Mac acceptance is claimed. A matching Mac
export and native checks are needed before promoting this candidate across platforms.
