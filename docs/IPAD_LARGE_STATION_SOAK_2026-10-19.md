# iPad large-station memory and performance test — October 19, 2026

**Result: no crash or logged game error, but the large-station frame-rate gate is not passed.** Tested installed Validation2 `brinespace-0e63ab6e9c2e7500` on physical iPad13,18 (A14,4GB,iPadOS27.2). Source baseline remains81b2f9a4a36eb0e3162d86ccfb4e9ef735836122 plus accepted uncommitted work on `codex/ipad-memory-placement-2026-10-17`. No game-source/art/signing/install changes, commits, pushes or frozen/public Mac/Windows changes in this pass.

## Workload and limits

Created a disposable 40-room rendering fixture from a copied cycle64 save, including Moonbay, Tidal Power Plant, Hydroponics Farm and Storage Depot: four multi-cell rooms,52occupied cells. Generation used isolated native execution against the exact exported PCK, free setup and seeded reserves. The fixture was saved with both test flags off; the normal installed runtime was used on the iPad. Footprint constraints were checked during synthetic assembly; full door connectivity/organic gameplay progression was not certified. This is rendering/memory stress evidence, not acceptance of a naturally built fully connected40-room game or many-crew workload. One crew member was present.

The monitored wall window lasted733.54s (~12.2minutes). Discovery dialogues briefly paused play and were dismissed; it is not uninterrupted active time. The saved fixture progressed cycle65→180, retained40rooms/onecrew/100%integrity, and was still running with no unpowered rooms at that save. Materials depletion correctly blocked a late placement attempt.

## Measurements

700valid nominal1Hz memory samples: peak2323435328B (**2.32GB**), end2296467216B (**2.30GB**). First/last60s medians2205945496/2295508752B: +89563256B (**85.4MiB**). Memory fluctuated; this short run does not establish a leak, no-growth result or hours-long headroom. Texture counter at the last sampled bucket1159.62MiB.

Eighteen active approximately one-second frame buckets sampled every30s ranged **9.68–25.65FPS**, median20.32FPS. These are sampled buckets, not the full-run FPS distribution. Three automatic reports all cite under20FPS for2seconds; automatic capture caps at3, so unchanged report count does not prove no later slowdowns. Manual capture at the end supplements recent history. All reports and sampled breadcrumbs show zero game errors. End-of-soak Save69.627ms/result0. Largest retained frames in the three automatic reports183/217/117ms; no claim every frame was retained or that all stalls are fixed.

First40-room station setup5.774s: interface/grid2.910s, restore1.982s, interfaceart0.596s, scene0.752s. Multi-second loading toasts were also observed. Some slow-frame samples show ~3100drawcalls and substantial grid draw/render-boundary intervals; an8192×8192lightmap appears in the report. These are profiling leads, not proof that a particular renderer or GPU stage is the root cause. Next useful work is controlled attribution of large-view rendering/lighting/invalidations alongside texture/cached-frame memory.

## Placement and restoration checks

A fresh40-room copy accepted a normal paid Storage Bay order at(25,19), rotation0. It remained queued; completed construction was not observed and is unaccepted in this larger fixture. The fixture's topology/crew access may matter, but the cause was not established. Save/Continue preserved cycle108,40rooms, resources/cards/draw/discard/rerolls/corruption/timer and the queued order. Placement-phase Save66.860ms/errors0; largest retained frame192.692ms in that report, which is not a full placement-latency distribution.

Excluded attempts: the initial target planner checked footprint only and omitted door matching. It was replaced with `get_placement_problem`; rejected targets spent no materials. A coordinate-scale hypothesis was tried and did not establish a bug; no touch-mapping defect is claimed. No new physical pinch/pan/two-finger rotation/lock acceptance.

## Owner save and evidence

All five original save/checkpoint files restored and hash-verified before launch. After Continue/Save, full gameplay state and timer match the backup: cycle64/sevenrooms/speedindex2/timer1.11834893097652. Only _path/event_history/saved_at differ. FinalPID9907alive, original station paused/menuclosed. The same helperPID64358 remains active (1h06m53s at final check), with no further authorization; leave it running between checks.

[Portable summary](ipad-memory-placement-evidence-2026-10-19/large-station-soak/SUMMARY.json). Full local evidence, failed/excluded attempts, screenshots, raw memory samples and owner backups: `/Users/Shared/BrineSpace-ipad-optimization-20261019/large-station-soak`. Raw saves and private process inventories remain outsideGit. Initial native fixture guard refusal from a missing expected-profile environment variable is retained; setting the correct scratch-profile variable allowed the guarded run. All native probes retained owner-save fingerprints.

Remaining gates: large-station FPS, longer/more representative connected/multi-crew memory tests, completed construction in the larger fixture, initial/first-use loading and outstanding gesture coverage. This test does not clear the iPad for release.
