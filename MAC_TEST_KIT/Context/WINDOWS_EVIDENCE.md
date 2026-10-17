# Windows evidence to carry forward

These results help prioritize Mac testing. They are not Mac FPS or acceptance.
The latest candidate is **brinespace-d3cfa1890bafefe7**, source SHA256
`d3cfa1890bafefe7e5b1a8c4e3f4f01f52e19d1e250701c27832d52b675e7514`.
Its runtime PCK SHA256 is
`49a95db92f2382f52b56034a5af4515746a464d2695e2aa1e150ca83d0c09b12`.

## Save and large station

Official Godot 4.7.2 Windows release, RTX 4070 Ti, Compatibility/OpenGL. Corrected-v3
40-room fixture, same camera/composition/four active actors, eight actions at
1×/2×/4×, two runs each at 1600×900 and 1920×1080. All four candidate runs valid:
96 phases / 11,520 measured frames. It is a dedicated manual-simulation/free-build
fixture; normal flags are restored for actual Save calls. OS/disk cache uncontrolled.

| Measurement | e54 baseline | d3 Save candidate |
| --- | ---: | ---: |
| Actual Save, one profiled sample per speed | 62.331–65.122 ms | 11.724–11.815 ms |
| Bank fingerprints | 50.310–52.176 ms | 0.125–0.142 ms |
| Primary Save action frames, includes readback/render | 95.836–113.938 ms | 42.521–51.259 ms |
| Primary 1× idle FPS | 44.97–45.69 | 46.51–46.95 |
| Primary 4× idle FPS | 40.35–41.43 | 41.23–42.56 |
| Primary 4× zoom FPS | 35.57–35.93 | 36.26–36.92 |
| Primary 4× placement action frame | 53.069–60.336 ms | 52.781–54.851 ms |

Following 60 frames after primary 4× placement: candidate max 39.976 ms, none >50 ms.
Original candidate **100.372 ms 4× idle** frame retained. One warm normal-speed
zoom/placement sequence was 8–9% slower. A separate contemporary two-repeat 1080p
A/B reproduced Save improvement but ordinary timing varied in both builds:
candidate Save frames 42.840–52.244 ms; several later ordinary phases 2–4% slower,
while earlier idle differences went the other way. No general FPS gain or blanket
absence of small regression is claimed. Rare idle stalls/render costs remain open.

Actual Save is measured separately from immediate QA readback. Diagnostic copies
add clocks/extra writes; their phase FPS/maxima are not headline benchmark data.
All three instrumented packets equal production after removing saved-at/path.
Do not compare Windows profile/benchmark totals against a Mac manual Save without
accounting for this difference.

## Correctness and packaged normal process

- New cache regression: 18 checks, red then green; fresh legacy hash equality,
  no repeated image decode, whole/in-place invalidation, mutable/wrapper/LA8 paths,
  fresh timing/metadata/live state and detached returned data.
- `test_run_save`, `test_save_integrity`, native `test_crew_pose_cache` and
  `test_crew_router_pixels` pass.
- Normal cargo checkpoint probe: 424 checks, ten cases, 30 presentations. Both
  gears, before/after/midpoint/terminal/idle; actual Save/read/staged restore,
  rejection of wrong bindings and exact restored pixels/clock/contact/plan/floor
  ownership plus finite completion. Windows native result; repeat targeted Mac checks.
- d3 actual normal-process packaged 12-room 4× canary: 60.014930 s / 3,598 frames,
  39 checks pass. Mean 59.9517 FPS; p95/p99 16.781/17.142 ms; max 38.045 ms;
  zero ≥50/100 ms frames/errors/invalid interval flags. Normal costs/failures,
  Save/Return/Quit and scene release pass. Not a two-hour d3 acceptance.
- Exact Windows package audit: same 36,430 manifest entries; only three intended
  scripts changed, no added/removed assets. 35,942 asset checks clean; 431 selected
  and 421 additional frozen scripts audited; additional scripts unchanged.

## Longer soak belongs to e54

e54 Windows actual normal 12-room 4× run: 7,200.001270 s / 431,838 frames, 39 checks;
zero expired router references across 1,441 censuses. Final-hour objects
32,604–32,631; late process private memory 2,627.180–2,627.711 MiB. Mean 59.9775 FPS,
p95/p99 16.767/17.193 ms. Two hitches 59.524/52.327 ms; none ≥100 ms. Active crew
alive/moving; normal scene exit/Return/Quit pass. Release orphan counters unavailable.

This confirms that targeted Windows lifetime cleanup in e54, not every possible
leak, a 40-room 60 FPS target, native Mac stability or a two-hour d3 run. Do not
transfer Windows private-byte counters to unified-memory/GPU residency claims.

## Evidence in the kit

`evidence/` contains compact JSON/CSV analyses, exact build/parity/source metadata,
the unchanged Windows benchmark fixture and normal 12-room fixture, selected native
cargo captures/verification and full reports. Raw multi-hour histories and huge
Windows trace directories remain archived on the Windows machine. Original local
paths in reports are provenance; copied files in this kit are the portable subset.
All original failed/slow cases remain represented in summaries; no outlier is
silently replaced by the follow-up cohort.
