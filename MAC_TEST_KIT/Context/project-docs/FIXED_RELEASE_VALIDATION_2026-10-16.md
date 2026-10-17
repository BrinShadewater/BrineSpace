# Fixed Windows candidate and matching Mac validation — October 16, 2026

Candidate **brinespace-e54e8a0eb8d58f65**, Godot 4.7.2 Compatibility/OpenGL.
Physical selected source: `D:/bs-object-growth-20261016/source-fixed/`;
Windows delivery: `D:/bs-object-growth-20261016/windows-fixed/`;
new evidence: `D:/bs-release-validation-20261016/`.

Source SHA256: `e54e8a0eb8d58f6578cca3d4753e72405cd93edc4af93e55261893bbd992de97`.
Windows PCK: `880bac9f98d153ad583217ad2fb9ae41c937711d9297fcfb3280426371b3ea4c`.
Only production change from the preserved b0b5d1b031c6ec29 candidate is the
crew canvas-router registry cleanup described in
[Object lifetime investigation](OBJECT_LIFETIME_2026-10-16.md). This validation
adds no production code, art or crew behavior changes. Earlier deliveries remain.

## Two-hour normal Windows 4× soak

Actual packaged release, 12-room copied checkpoint, 1600×900 native secondary
display 2. Normal process/timers, costs and failures remain enabled; Continue,
4×, Resume, comms-Minimize, Return to Title and Quit use production handlers.
QA is silent with physical input disabled. This is a VSync-limited station
stability run, not the uncapped 40-room performance workload or physical-input/
audio acceptance.

The new QA observer uses a fixed 50,000-bucket microsecond histogram, bounded 512
hitch rows and streamed 5-second JSONL observations. No raw frame or periodic
history remains in the game. A 60-second canary retained raw intervals solely to
verify exact histogram equality; all 39 checks passed. The long run's histogram,
hitches, aggregate counts and elapsed time also reconcile exactly. No frame is
discarded. Source, helper hashes, window/process flags and owner guards are saved.

| Check | Result |
|---|---|
| Completed duration / frames | 7,200.001270s / 431,838 |
| Assertions / interval flags | 39 pass / all 431,838 flags 0 |
| Mean / p95 / p99 | 16.672922 / 16.767 / 17.193 ms |
| Average FPS | 59.9775 |
| ≥50 / ≥100 / ≥400ms frames | 2 / 0 / 0 |
| Two hitches, both retained | frame 3: 59.524 ms; frame 337497: 52.327 ms |
| Expired canvas / tracked-owner references | 0 /0 in all 1,441 censuses |
| Objects, initial → final | 32,060 → 32,616; initial warming included |
| Objects, final hour / final 10 min | 32,604–32,631 / 32,610–32,631 |
| Textures after 5 min | 1,564.588 MiB throughout |
| Windows private memory, 6 min → last warm sample | 2,625.094 → 2,627.711 MiB |
| Windows private memory, late 10 min range | 2,627.180–2,627.711 MiB |
| Recorder maximum streamed write | 0.363 ms; no retained histories/overflow |
| Logged errors / warnings / foreign games | 0 / 0 / 0 |
| Return / gameplay instance freed / normal Quit | Pass / yes / pass |
| Returned-title object census | 2,356 with this observer |
| Protected owner files | All 2,948 unchanged |

Branforth, Margot and River remain alive and keep moving/changing goals. Only
the known economy advice stuck key is present. One automatic report already
existed before measurement; no additional report was triggered during the soak.
Neither hitch coincided with a report worker. Short render-gap values do not
attribute these hitches to a particular system or prove GPU completion.

The registry's prior 75–76 expired references/min growth is absent. The final-hour
object slope is 0.133/min within a 27-object range; it is not mathematically flat.
Private-memory samples include engine/OS/cache state and exclude exact frame
attribution or GPU residency. Release orphan/static-memory counters are unavailable;
their zero values do not establish general leak freedom.
The 16.767 ms p95 still exceeds the existing 16.7 ms pacing threshold. Duration,
stability and registry-lifetime checks pass; this is not a pacing-gate pass.

Evidence: `soak-2h-v1{,-summary,-provenance,-memory,-owner,-process-guard}.*`,
`soak-2h-v1.json.periodic.jsonl`, `soak-analysis.json`; full logs preserved.

## 40-room performance regression

All four serial native runs pass: 96 phases / 11,520 measured frames, actual
release with no foreign/minimized-run rejection, no missing-image placeholders,
no automatic benchmark reports, and all 2,948 protected owner files unchanged.
Reused the exact corrected-v3 dedicated fixture
(SHA256 `3a98f6bcff0744276c973da28fc38c67c7d09d159896bbb3d2ca1bde348c38de`),
both 1600×900/1920×1080, two repeats, all 8 actions at 1×/2×/4× and 120 samples/phase.
The synthetic completed Bill recovery ward is fixture setup only; this benchmark
manually steps simulation with free-build/failure fixture flags and does not
establish normal recovery gameplay acceptance. Preserve every measured outlier.

| Selected phase | Earlier candidate FPS | Fixed candidate FPS |
|---|---:|---:|
| 1× idle | 43.83–45.82 | 44.97–45.69 |
| 1× zoom | 36.95–37.73 | 37.17–37.93 |
| 4× idle | 40.45–41.31 | 40.35–41.43 |
| 4× zoom | 35.65–35.97 | 35.57–35.93 |
| 4× placement phase | 40.15–40.78 | 39.99–40.63 |

Ranges span both resolutions and both repeats. These small changes overlap the
prior spread and do not demonstrate a sustained average-FPS gain or regression.
All 96 phases miss the existing pacing gate; 60 FPS remains open.

4× zoom p95/p99 ranges: 39.459–39.984 / 48.831–51.553 ms; max 57.361 ms
(earlier maximum 53.940 ms). 4× idle maxima reach 89.424 ms; the earlier candidate
already had 73.220–90.781 ms spikes in the same phase. They are not discarded.

4× action-frame placements: 53.069 / 55.750 / 60.336 / 55.804 ms, compared with
54.243 /54.931 /54.335 /54.701ms previously. Action CPU work 2.323–2.390 ms;
the following 60 frames peak 33.853–35.988 ms with zero >50 ms or >100 ms frames.
Three of four paired action frames are higher; the largest increased from
54.931 to 60.336 ms. The following-frame burst did not recur. This four-run
comparison does not attribute that difference to the patch.

Across all speeds/actions, 68 frames >50 ms (also 68 previously), 8 >100 ms versus 5
previously; every >100 ms frame is in Save. Save maximum 113.938 ms versus 105.750 ms.
Loading/Save and large-station pacing gates remain unresolved. No frame is
filtered to improve the headline averages.

Evidence: `mixed-fixed-v1/` (exact fixture/build identity, raw phase samples,
frame traces, logs and owner guards), `benchmark-analysis.json`, `phases.csv`,
`placements.csv`, `benchmark-adapter.json`. Variable OS scheduling/disk-cache
state and two repeats per resolution limit causal/performance conclusions.

## Mac twin and remaining gates

Matching Mac ZIP export and static parity pass. New test ZIP:
`D:/bs-release-validation-20261016/mac/BrineSpace.zip` (approximately 3.301 GiB).
ZIP SHA256: `3f77d0a4615cc0cf84963a75c9bffb0b24725dc0c5086d90e646ecdf8775ec74`.
Use this build instead of the earlier b0b5d1b031c6ec29 ZIP, which predates the fix.

The official verified 4.7.2 template exports a Universal 2 bundle (arm64 and
x86_64), identifier `com.shadewater.brinespace`, executable mode `100755`, exactly
one PCK and no QA override. Its 36,430 manifest entries have no differences or
case collisions. PCK and build metadata are **byte-identical** to Windows, so the
earlier exact Windows asset/source audits apply to these same bytes. This does
not establish native rendering. The Mac README includes the separate-test-account
checklist; licensing sidecars, build metadata and checksums accompany the ZIP.
Final ZIP integrity and preservation evidence lives in `mac/zip-integrity.json`
and `final-guards.json`; no duplicate extracted Mac PCK is retained.

The owner already offered to run the ZIP on their Mac. Native launch/Gatekeeper,
controls/audio, rendering,
save/Resume, frame pacing and memory remain external checks; Intel needs its own
hardware result if it is to be claimed. Existing large-station 60 FPS, cold loading,
Save hitch and target-hardware gates remain open. No release promotion or upload.
