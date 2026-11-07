# Large-station frame cost and hitches

Updated: October 20, 2026 · BrineSpace · Targeted upload reduction complete

## Objective and acceptance

Reduce large-station frame cost and hitches against the frozen Windows candidate
`brinespace-ef1c732983837a49`. The retained change reduces returning-cargo upload
work; repeatable overall frame-pacing improvement is **not established**.

## Accepted decisions and constraints

Preserve gameplay, animation clocks, selected art,
owner data and the existing release. No rover body cropping or larger-cache retry.
The owner-accepted October 11 cargo sampling bound applies; body art remains whole.

## Current state

Evidence and reproducible drivers: `D:/bs-frame-cost-20261020/`.
Actual release comparisons use physical copies of the candidate EXE/PCK, narrow
overlays verified before scene loading, and the corrected
mixed-station fixture from the preceding performance work. Runs cover 40 rooms,
1920×1080, idle and lighting at 1×/2×/4×, 180 frames per phase, alternating order.
All test profiles are isolated. `invalid-minimized-candidate/` is excluded.

Retained changes: eight whole-path entries in `tools/build_drone_cargo_storage.py`,
regenerated `scripts/drone_cargo_storage_catalog.gd`, eight new carry PNGs in
`assets/mining-rover-v1-2026-09-26/cargo-storage/`, and expanded
`tests/test_drone_cargo_storage.gd`. Existing UID retained; new raster paths use
Git LFS. Source/assets only: the delivery EXE/PCK and signed ZIP are unchanged.

## Verification

The first reference run's 184.030 ms frame includes two 144,506,880-byte mining
body uploads taking 81.226 ms in the sampled process frame; simulation takes
1.857 ms. Another 94.140 ms frame includes returning north/south cargo sheets,
each 48,168,960 bytes. These are direct CPU upload intervals, not an additive
accounting of the complete GPU/frame cost.

### Water trial

The Moonbay trial retains fixed ribbon seeds, x coordinates and base angles in
a bounded, canvas-owned cache. Positions, color and tessellation remain animated.
It preserves double precision until the original Vector2 conversion. Partial
water levels use the original path.

Native regression: 521 checks, zero failures; the new cache assertions fail four
times against the original implementation. Full room composition: 135 checks,
zero failures. Pixel comparisons include scale, tint, pumping, water levels,
cache eviction and owner release.

**Water cache not retained.** Three alternating station pairs produced candidate
means 28.863/30.971/31.228 ms versus reference 33.815/32.190/37.947 ms, but unrelated
simulation timings also shifted. A same-process alternating CPU test in the
actual release runtime gives median 1.035→1.011 ms per draw, only about 0.025 ms.
The isolated test is headless CPU command generation, not a frame-time benchmark.
The evidence does not justify attributing the large station differences to this
small cache. Both Moonbay and its test were restored byte-for-byte to their
pre-trial contents; trial copies and all measurements remain in the evidence folder.

### Returning cargo

Returning cargo extends the existing accepted cargo method to eight 60-frame
returning sheets. Their total decoded storage is 385,351,680→2,364,480 bytes.
The generated catalog retains original/derived hashes and Windows-only selection.
Original art and rover body sheets are untouched.

The extended native test covers all returning headings and uses each sheet's
actual middle frame. Red: nine missing-coverage assertions. Green: 538 checks,
zero failures, including original-image access, unsupported-context fallback,
hash invalidation, session release and sampling bounds. Of 144,855 examined scaled
pixels, 1,164 use a neighbouring source pixel, within the previously accepted
half-source-pixel bound; scaled output is not claimed byte-identical.
All 16 source-sheet hashes match the frozen candidate's originals.

Two actual-release pairs, reversing run order, complete with no engine/art errors.
Each lane measures 1,080 frames. Four cardinal carry sheets are exercised in these
station runs; all eight headings are covered by the native regression.

| Metric | Pair 1 reference → cargo | Pair 2 reference → cargo |
|---|---:|---:|
| Recorded carry payload, MiB | 505.31 → 4.00 | 459.38 → 4.00 |
| Recorded carry upload work, ms | 110.535 → 13.566 | 70.562 → 15.792 |
| Mean frame, ms | 32.228 → 25.936 | 25.128 → 26.504 |
| p95 frame, ms | 48.704 → 36.573 | 36.627 → 38.202 |
| Maximum frame, ms | 151.139 → 77.937 | 77.427 → 104.910 |
| Frames over 50 ms | 53 → 12 | 6 → 13 |

Payload includes the existing diagnostic's small storage-wrapper creation records
as well as actual frame texture uploads; it is not a hardware bus measurement.
Small frame creation records replace whole-sheet transfers (389 versus 10–11
carry records). No full carry fallback upload appears in the candidate traces.
Final engine texture counter is 1,968.448 MiB in all four runs; no total-memory
reduction claim. Whole-station pacing remains mixed and every phase misses the
existing combined gate.

All 12 phase comparisons have identical cameras and identical captured gameplay,
room, drone, resource and animation state **except** surveyed-water cells,
comms seen entries and the new pilot's initial decision RNG. These differences
remain in the raw reports: survey is throttled by `Time.get_ticks_msec()` and
the pilot constructor randomizes its RNG. Therefore this is not full deterministic
state parity or a clean causal FPS comparison. Isolating those fixture clocks is
necessary before attributing small whole-station gains. Final candidate station
capture reviewed; the native cargo test establishes the sampling acceptance.

Generator `--check`: 16 sheets, zero failures. Scoped `git diff --check` passes.
All 2,971 owner files are hash-unchanged; signed ZIP size/mtime unchanged.
QA copies were cleaned by the maintained hash-checking runner; delivery retained.
Water trial source/test are restored byte-for-byte. Final free space:
C 20.25 GiB, D 26.14 GiB. `FINAL.json` records checks and source hashes.

## Next action

Large-station ordinary frame cost and body/wheel upload hitches remain open.
Before another small rendering trial, make survey/comms/initial actor RNG
deterministic in a dedicated comparison fixture while retaining their work.
Do not infer a broad speedup from the cargo payload reduction. No 60 FPS,
hitch-free, endurance, Mac or refreshed release acceptance is claimed.
