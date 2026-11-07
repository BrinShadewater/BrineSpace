# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: compressed crew startup cost attribution

## Objective and acceptance
Resolve loading overhead before admitting the large exact-pixel crew memory
prototype. Full release frame/memory/loading, endurance and PC/Mac gates remain.

## Accepted decisions and constraints
Keep lossless pixels, independent frame identity/metadata/filtering, PNG loading,
James inheritance and Bill unchanged. Prototype remains private. Do not interpret
OS-cache-uncontrolled initial launches as certified cold results.

## Current state
Driver `output/compressed-crew-2026-10-06/measure-crew-startup.py`; summarizer
`summarize-crew-startup.py`; evidence in `output/crew-startup-measured-2026-10-07/`.
Six native processes: normal/compressed initial profile, then two learned-order
launches per profile, second pair reversed. Private preferred spill Slots/Router
and physically selected flood helper used; original bytes restored.
Original interrupted tool created only `output/crew-startup-2026-10-07/probe.gd`;
no matching live process or result/log existed; original source hashes confirmed
before running the new measured artifact. No running workload restarted.

## Verification
Initial new-game loading only: benchmark exits after readiness, without synthetic
40-room construction. All three pairs full crew state, loaded counts and request
counts match; six clean logs/exits; all router releases succeed. Current normal
replacement-crew loading method compared with private method: only bank creation,
CPU player selection, bank adoption and router activation differ. Selected manifest
declarations unchanged; diff retained in selected-loader-diff.txt.

Learned-order launch median request-to-ready normal6,775.696ms vs
compressed7,839.350ms (~1,063.655ms slower). Scene load normal2,546.859/2,589.057ms,
compressed2,505.900/2,504.493ms. Post-instantiation readiness normal4,084.659/
4,137.447ms vs compressed5,239.702/5,234.945ms. Excluding scene load would hide
the actual request-to-ready gap; warm6s gate not passed.

Compressed learned PNG work255.878/262.250ms, compression1,152.765/1,149.141ms,
bounds575.968/573.700ms. Both lanes12,645 worker submissions/hits and zero unused
results. Prefetch peak decoded storage~91.3–93.6MiB; not a whole-process RAM budget.
Compression is a concrete main-thread cost comparable to the warm loading gap;
not proof of exclusive cause or a guarantee that parallelization saves it all.

First profile launches normal30,386.374ms vs compressed17,263.831ms request-to-ready;
run order/OS caches uncontrolled, do not claim a cold improvement. Previous normal
12.9s baseline does not describe this run. Compressed initial PNG6,248.741ms,
compression1,362.654ms,bounds573.647ms.

Reported ready textures normal2,439.292MiB vs compressed1,082.994MiB in all runs
(1,356.298MiB less). This is initial few-room gameplay, not12/40-room acceptance.
After game exit both80.055MiB in all runs, no title scene. Owner2,936 files unchanged,
all temporary source bytes restored, all processes terminal; no normal source edits.

## Next action
Prototype bounded worker preparation for surviving crew paths at batch finish:
independent image decode/hash/lossless compression/used bounds; consume results on
main thread without mutating shared storage or using non-thread-safe global caches.
Preserve request order/diagnostics/progress, drain pending jobs on failure/exit,
and compare source bytes/metadata/ownership before matched loading measurements.
No permanent all-assets cache or destructive art conversion. Parallel compression
is a measured hypothesis; reject if overall readiness/memory/stutters regress.
