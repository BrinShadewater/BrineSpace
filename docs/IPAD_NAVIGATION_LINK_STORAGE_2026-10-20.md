# iPad canonical navigation links — October 20, 2026

Validation 2 **brinespace-4b8a6d033a718d09** is installed on the physical iPad. Original five
save/checkpoint files are SHA-exact after final launch. Owner cycle 64 / seven rooms
is paused at 4× with menu closed. Complete **99aa** remains the immediate rollback.
The compiled LF script is retained as `bill_npc.packaged.gd.txt`; the working copy
was restored to its incoming CRLF line endings after export to keep the integration
diff small. Normalized bytes match exactly (`source-eol-equivalence.json`).
This pass reduces a bounded CPU allocation; initial loading and total memory
remain release blockers.

## Change and proof

`scripts/bill_npc.gd` now generates canonical packed point-index pairs directly,
in original link order, rather than retaining nested two-element Arrays and a
second packed representation. Point order, weights, mutable per-actor graphs,
collision checks, door/lock policy, staged yields and revision invalidation remain.
The reference assembly reads the same canonical edges. Legacy in-memory fixture
admission releases nested links after conversion; there is no save-format change.

The exact previous PCK contains 55 templates / 49,937 nested pair Arrays and 399,496 B
of packed edges in the 56-room/four-crew checkpoint. The candidate retains the
same packed edges with **zero nested pairs**. All four ordered 18,514-point graph
hashes exactly match the prior PCK, including positions, weights and ordered
connections. Explicitly releasing the previous duplicate arrays in an isolated
native probe releases **8,185,048 B** of Godot-tracked CPU
allocations. This is not a fixed physical-iPad footprint saving or a GPU saving.
Native probe timings were diagnostic, sometimes concurrent with host build/tests.

## Tests and actual device

New storage regression: red 1/4 (nested arrays retained), then green 4/4. Nine actual
candidate-PCK suites pass: storage, prefix, room ownership, segment parity,
boundary reuse, station navigation, spent pod, crew-cache capacity and room-art
lifetime. Prefix: 1,488 checks / 301,104 records / 2,328 routes; segment: 153,824 comparisons;
boundary: 24,054 checks / 447 paths. Source/asset audits have zero missing/changed/unknown
entries. Strict signing passes; app PCK equals audited export. Four temporary
export configurations restored byte-exact. Real Mac owner-profile guards pass.
Initial harness rejections were unrecognized JSON PASS output and a missing
scratch screenshot directory; retained successful graph tests were not rerun,
and the affected UI suite passed after runner-only corrections.

Physical iPad13,18 / A14 / 4 GB, iPadOS 27.2, native Compatibility, existing VM1 sampler,
1920×1334 viewport. Same normal-rules 56-room/four-crew checkpoint, paused 1×,
prepared cache populated; recorded PNG rebuild jobs 0. One ordered comparison:

| Measurement | Previous 99aa fresh | Candidate fresh | Candidate same-process repeat |
|---|---:|---:|---:|
| Station setup ms | 9010 | 9700 | 6467 |
| Restore ms | 4001.995 | 3848.948 | 1496.151 |
| UI/grid ms | 2639.390 | 3479.959 | 2554.118 |
| Latest footprint MB | 2149.503 | 2146.832 | 2229.358 |
| Sampled peak MB | 2170.376 | 2185.170 | 2229.440 |

No initial-loading improvement or consistent whole-process RAM improvement is
established. Initial restore is slightly lower but crew-cache finish waits vary;
total fresh setup is slower in this pair. A prior 99aa fresh setup was 9.685 s.
Covered station setup excludes later first redraw; do not call these full
launch-to-playable timings. Startup/title forced termination notices are expected
from the controlled process restarts, not evidence of a spontaneous new crash.

Normal 1× active run completed **10.377 active
minutes** (12.358 wall minutes), cycles 70→105,
all four crew alive / errors 0. Resource costs/caps/failure conditions remain normal;
fixture initial reserves are seeded. Sampled peak 2294.796 MB,
end 2249.298 MB; first/last-minute median change
7.291 MB. Sparse active buckets median
12.92 FPS, maximum 336.124 ms.
The USB/HouseArrest collector was unavailable before timed acceptance; the active
run used network devicectl telemetry copies with fresh PID/epoch filtering.
The first memory minute includes dialogue/cache warming.
Endpoint-counted active duration excludes observed pauses; sparse buckets are not
full-run frame coverage or leak clearance. Branforth ends at 100 hunger/fatigue/maintenance and Marsh at 100 maintenance; the
fixture is not survival/balance clearance. Check activity/refuge reachability
before extending it; do not suppress normal failures.
This short run does not replace the
previous 30–40 minute revision-specific evidence.

Actual card return and Save/title/Continue/Save pass. Full serialized owner state
and exact paused timer match; only _path, event_history and saved_at may differ.
The existing Continue 1× reset is manually reselected 4×
for parity. Final five incoming originals are hash-exact after final launch.
Native navigation tests cover rotations/locks; no new physical multitouch
rotation, paid completed construction or background/resume certification is claimed.

## Identity, rollback and next work

Branch `codex/ipad-memory-placement-2026-10-17`, HEAD
`81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus dirty accepted work.
Compiled source SHA256 `4b8a6d033a718d0998f2031f4b7dbc7063f5e895f9838df349ab2fb0c6c87d11`.
PCK `a3087a3b6dc77b9246eb6bbf554973a4a663815ff1611a2ad134eaac70649f51`.
Signed executable `68a81417ffbb27ddd0bc5d6ae9b3fe3f43d5c2fdea930381c853b5711d075fc3`.
Native sampler `29b09ee6881320efa445452d84597c5186b0f44d568989d948d0505f76783b66` (unchanged VM1).

Complete candidate/evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261020/navigation-link-storage/candidate`.
Immediate rollback: `/Users/Shared/BrineSpace-ipad-optimization-20261020/restore-startup/candidate`
(99aa, signed app/export/source metadata retained and rehashed). All earlier
protected rollbacks/recovery donors, source/saves and frozen Mac/Windows releases
remain. No upload, merge or release candidate replacement occurred.
Portable results: `docs/ipad-memory-placement-evidence-2026-10-20/navigation-link-storage`.

Mid-run observation: compressed crew sources remain 140,535,542 B while presenter
and drone caches warm. The snapshot and GPU texture-accounting change are retained
in `cache-warming-observation.json`; cumulative decode/upload totals are not
retained RAM. Do not identify a leak from this alone.

Next isolate GPU/texture residency and crew-cache finish/restore waits with the
same checkpoint. This removes ~8 MB of CPU containers; the ~2 GB process footprint,
first redraw, active large-view frame rate and initial loading remain unresolved.
Not release-cleared.
