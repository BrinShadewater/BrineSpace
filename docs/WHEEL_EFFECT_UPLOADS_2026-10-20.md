# Wheel and effect upload handoff

Updated: October 20, 2026 · Project: BrineSpace

## Objective and acceptance

Reduce large-station wheel/effect upload hitches while preserving exact animation
timing and current artwork. Retained a narrowly verified East mining-effect
storage extension; wheel upload churn and the overall pacing gate remain open.

## Accepted decisions and constraints

East now uses the same full-size, lossless two-channel storage already used by
North/South/West. No runtime algorithm, frame selection, clock or original PNG
changed. Unsupported drawing contexts retain the existing original-art fallback.
Windows remains the enabled platform. No pose holds or delayed publication.

Wheel sheets have independent RGB and transparency; the prior channel audit in
[current upload context](DRONE_CURRENT_UPLOAD_CONTEXT_2026-10-10.md) rules out
applying this two-channel conversion to them. Do not repeat rejected cropping,
indexed sampling, cache growth or broad prewarming without new evidence.

## Current state

Changed files:

- `tools/build_drone_effect_storage.py`: include East in the lossless generator.
- `scripts/drone_effect_storage_catalog.gd`: generated East entry.
- `assets/mining-rover-v1-2026-09-26/effect-storage/mine-east-effects-la.png`:
  84,539-byte derived asset, covered by Git LFS.
- `tests/test_drone_effect_storage.gd`: require all four directions and East.
- This handoff and `docs/CURRENT_STATUS.md`.

Original East decoded payload is 137.8125 MiB; derived payload is 68.90625 MiB.
All four original PNGs hash-match the frozen release. Existing dirty files were
preserved. The unsigned release candidate and signed delivery were not rebuilt.

## Verification

Generator check failed as expected before generating the missing East asset,
then passed all four sheets with exact reconstruction. Native test passed
**106 checks, zero failures**, covering sampled raster equality, supported and
fallback contexts, immutable original pixels, accounting and resource release.

Evidence: `D:/bs-wheel-effect-20261020/`; native test logs:
`D:/bs-frame-cost-next-20261020/east-effect-green.*`.

Four valid packaged-release fixture runs compare the frozen
`brinespace-ef1c732983837a49` runtime plus accepted cargo/mask overlays, changing
only the effect catalog and East derived asset. Order: reference, candidate,
candidate, reference. Each measures 1,080 frames at 1920×1080 across idle/lighting
and speeds 1/2/4. Runs are muted, native, non-debug, scratch-profile isolated.
Deterministic fixture clocks and seeded behavior match; automatic report capture
is disabled only in the private comparison fixture to avoid diagnostic workload.
The first minimized reference attempt is excluded, replaced by `reference1b`.

| Metric | Reference 1 | Candidate 1 | Reference 2 | Candidate 2 |
|---|---:|---:|---:|---:|
| East upload interval, ms | 19.611 | 5.288 | 13.963 | 6.210 |
| Sampled wheel uploads | 19 | 18 | 19 | 19 |
| Sampled wheel payload, MiB | 872.813 | 826.875 | 872.813 | 872.813 |
| Sampled wheel upload time, ms | 120.505 | 90.688 | 99.100 | 94.342 |
| Mean frame, ms | 25.959 | 24.069 | 23.324 | 22.911 |
| p95 frame, ms | 42.367 | 36.172 | 32.868 | 31.283 |
| Maximum frame, ms | 101.781 | 64.821 | 66.480 | 74.083 |
| Frames >50 ms | 20 | 10 | 3 | 2 |
| Sampled texture peak, MiB | 2760.853 | 2668.978 | 2760.853 | 2668.978 |

Each run samples one East upload and five effect uploads total. No sampled
effect-original fallback occurs. All 12 paired phase saved-state/camera checks
match; all 2,160 paired frame samples match drone positions, clocks, phases,
displayed states/headings/frames, including deposit work-face heading.

The repeatable result is half the East payload and a shorter measured upload
interval. Mean/p95 improve here, but maximum frames are mixed; all four runs
still pass zero of six pacing phases. Wheel volume reduction is not repeatable.
These are bounded CPU-side upload events and sampled engine texture accounting,
not complete GPU transfers, within-frame VRAM peaks or endurance certification.

Final protection guard: all 2,971 owner files unchanged, signed ZIP size/mtime
unchanged, temporary release EXE/PCK copies cleaned. Free space C: 23.90 GiB,
D: 25.98 GiB. Scratch profiles were used throughout.

## Next action

Wheel churn remains roughly 827–873 MiB across 18–19 sampled uploads in this
fixture. Use the existing per-path lifecycle evidence to target recurring wheel
residency/eviction without increasing the accepted memory budget or changing
sampling coordinates. Any new remedy must demonstrate exact pixels and timing,
then survive both comparison orders; this task establishes no wheel fix.
