# iPad habitat and sealed Veld pod demand — October 19, 2026

Installed **brinespace-f829898722272cfe** in Validation 2 on physical iPad13,18/A14/4GB/iPadOS27.2.
Branch `codex/ipad-memory-placement-2026-10-17`, starting HEAD `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus preserved accepted dirty work. No commit/push performed. HEAD alone does not identify this build.

- Source SHA256: `f829898722272cfe05cbf5a66661e7f24763cb1f304c461203bd9a4ce0d71d2a`
- PCK SHA256: `ee61026b35cf26f7a2e1d0949141c0d35ec14dc0b6c33c748dc64c9592bfacb4`
- Executable SHA256: `bd84e03c5ff8673726df0b05e4df48164d040a614af0f88c2b2a7088e6625f99`
- Native memory-only sampler SHA256: `23fafafc323b69eaac670bbbc8e9e4fc7a05c03f4902e9246f8b761c272b2617` (unchanged).
- Local signed app/export and detailed evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261019/veld-pod-demand`.
- [Portable receipt](evidence/IPAD_HABITAT_VELD_DEMAND_2026-10-19.json).

## Change and evidence

Tablet habitat setup skips biome materials outside its used regions and skips an iron base-ground image fully replaced by its selected variants. Native 7/40-room full viewport pixels, meshes and RNG match the previous accepted source; engine texture allocations fell 5.333 MiB. Desktop eager loading and required material fallback are unchanged. This was intermediate bf39; it passed 22 exact-pack fixtures, signing/audits and30.177 active-minute normal1×soak65→158/errors0.

That baseline exposed a late sealed Veld pod admitting3186 source entries and 28,583,336 compressed bytes. `Architects.pod_for_display` now uses the canonical idle-south frame 0 while that tablet pod remains sealed, preserving its pivot, standing height and filter. A grid-owned texture releases with the session. Desktop, already-loaded, recovered and walking paths retain the full player; load failure falls back. Full animation work is deferred until needed, not removed from live crew. No artwork, gameplay costs/failures, station geometry or RNG changed.

New native tests compare actual pod viewport pixels through closed/opening/recovery/walking states, 7/10-second wake durations and reduced motion; getter spies assert full-player demand boundaries. All 23 exact-pack fixtures, asset/source audits and strict signature pass; all four temporary export configs restored byte-exact. Two scoped reviews found no production issues; the habitat test's missing native-lane registration was corrected.

Physical replay of baseline cycle 158 proved sealed-pod cache active, source entries **11920** and compressed bytes **102953537**, versus baseline 15,106 / 131,536,873. These are ownership counters, not an additive or controlled whole-process RAM saving.

## Physical tests and limits

Owner first/repeat Continue pass. Setup **4949/3099ms**, actual first redraw **2264.407ms**: still slow; no useful redraw/loading gain established. Restored card selection labels can appear as last_action during loading; they do not prove a placement caused that startup hitch.

Synthetic nine phases / 5,400 frames at 1/2/4× passed, maximum **483.086ms**, zero logged errors / image failures, all starting station bounds intersecting. It is method-driven, with profiler/free-build/failure bypass confined to that disposable fixture; not real-touch or normal-play clearance. Process samples peak1961430512B/end1946701272B.

Normal-rule 1×, 40-room / one-crew fixture completed **30.096 active minutes**,65→160, crew state recorded in receipt, errors0. Seeded initial reserves only; normal caps/costs/hazards. Sampled process peak **2156220008B**, end **2141490792B**; first/last-minute medians **2024508864→2140655208.0B**. Opening dialogue pauses excluded from conservative endpoint-counted active duration, but opening-window memory can include warmup. Sparse 15 s latest-bucket snapshots maximum **300.459ms** are not full-run histograms. Compare cache-growth JSON's like-duration windows, not unequal baseline/candidate peaks. The normal soak did not encounter the sealed Veld display (its cache flag stayed false); the separate cycle 158 replay verified that path. Discovery/hazard outcomes differ from baseline, so this is not a controlled RAM comparison. No leak clearance or organic multi-crew/release acceptance.

Actual UI card return, pinch zoom, rotation button, Codex drag, Home/reopen checks passed. Automated two-finger pan/tap is unsupported and not claimed. Save/title/Continue/Save compared complete station state and exact timer after manually reselecting 4× while paused following Continue's existing 1× reset; this does not establish automatic speed restoration. The native comparison covers the full serialized station state and exact timer; file path, write timestamp and diagnostic event history may differ and are recorded separately. All five incoming original save/checkpoint files verified SHA-exact after final owner launch; cycle 64 / seven rooms, paused at 4×, menuclosed; PID 47657. QA benchmark marker removed.

## Storage and recovery

Unused iOS 27.1 Simulator removed through simctl; physical iPad tooling retained. Completed installer cache matched 3,987 installed files before removal; HTTP and completed native-test caches are regenerable. 353 copied report ZIPs were consolidated using independent APFS clones after SHA and metadata checks. Old 1,201 automation action directories / 3,603 files are SHA-verified in `old-ui-actions-before-20261019-1700.tar.xz`; current actions excluded.

Older da3/dd89, intermediate bf39 and Oct17donor PCKs are preserved in full-stream SHA-verified recovery archives under `/Users/Shared/BrineSpace-workspace-cleanup-20261019-consolidation`. Keep all archives and the complete 7bb root donor in `texture-residency-pass`; `DONOR_RECOVERY_ORDER.md` explains restoring the archived Oct17donor before its dependent leaf archives. All 12 dependency paths verified. Source/saves/unique evidence/frozen Mac and Windows deliveries retained. Final free space approximately10.3GiB after the current build.

The maintained exporter now requires 7 GiB free on its output volume before preset/output mutation. Mocked 3 GiB preflight returned pending without creating output or changing the preset; real sufficient-space preflight passed. This is post-build tooling only and does not change the tested game artifact.

## Still open

Initial ~2.26 s redraw and intermittent stalls remain. Track source-bank ownership separately from presenter/drone caches and process footprint; decoded virtual-byte counts are not retained decoded RAM. Next profiling should resolve remaining decode/adoption/eviction/render boundaries before proposing another fix. This build remains validation-only.
