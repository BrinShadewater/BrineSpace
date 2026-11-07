# iPad canonical door source sharing — October 20, 2026

Installed **brinespace-87a7abf2fc3e6117**, unchanged VM1 sampler, on the physical
A14 iPad13,18 (4 GB). Source checkout HEAD remains
`81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted uncommitted work.
This is scoped validation, not release clearance.

## Change and evidence

Hallway and default door skins uploaded the same raised/low PNG sheets independently.
Styles now borrow an existing upload by complete source path, while keeping separate
style objects, animation progress, cropping and draw tint. Existing per-style lookups
own all aliases; the existing last-owner cleanup clears them all. No second strong
source cache, source-art edits, reduced quality or normal gameplay changes.
`--reference-door-source-sharing` retains the former storage path for comparison.
Bounded `door_storage` diagnostics count unique image identities and source paths.

Meaningful red: 8 checks / 3 failures before the fix. Native expanded regression:
88 checks / 0 failures, including all registered styles, original source pixels,
raised/horizontal/vertical geometry, opening positions, nearest/linear filters,
independent progress, overlapping-owner release and reverse-order scene reentry.
Ten actual-PCK regression suites, raster/source audits and strict signing pass.
Native runs used the real display, isolated profiles and final owner fingerprints.
Exporter configuration was restored byte-exact before project tests.

## Physical comparison

Same package, fresh-process sharing disabled → enabled, same 56-room/four-crew fixture:

| Measure | Reference | Sharing |
|---|---:|---:|
| Door image identities / sources | 11 / 10 | 10 / 10 |
| Door RGBA capacity bytes | 69185248 | 62895136 |
| Engine texture MiB | 901.459 | 893.462 |
| Latest sampled process MB (decimal) | 2078.232 | 2076.086 |
| Station build ms | 8651 | 9018 |

Installed-baseline station build: 9065ms;
candidate first: 9835ms;
candidate same-process repeat: 6314ms.

These are ordered measurements, not a fixed process-RAM bound or controlled loading
speedup. RGBA capacity, engine allocation counters, GPU VM regions and process
footprint measure different things; region pages may alias. Build timing excludes
later first redraw. Full raw timing/VM records are in the evidence directory. The deliberate harness
process stops produced the existing unclean-session notice; it was dismissed
before Continue and is not counted as a spontaneous app crash.

Normal 1× fixture: 10.370 endpoint-counted active minutes
(see raw completion record for exact duration), 56 rooms/four crew; sampled process
peak 2190.250 MB, end 2159.595 MB.
First/last-minute median difference 7.193 MB.
Sparse active buckets median 14.06 FPS,
maximum frame 200.019 ms. Errors 0.
Endpoint accounting excludes observed pauses but is not continuous frame capture;
first-window warming prevents interpreting growth as a leak rate.
All four crew were active and alive at cycle 105. Crew health and exact cycle
endpoints are in `soak-health.json` and the summary.

Actual card-return clearing passed. Save/title/Continue/Save passed complete-state and
exact-timer comparison (only `_path`, `event_history`, `saved_at` differed).
All five incoming owner save/checkpoint files are SHA-exact after the final launch.
Owner cycle64/seven rooms is paused at4×, menu closed, no room selected.
No new physical multitouch, completed paid construction or long-duration leak
clearance is claimed. Initial loading/first redraw, low large-view FPS and memory
headroom remain open. Next isolate the checkpoint restore subphases (apply, crew
restore, finish) before changing their behavior; the existing coarse span remains
about four seconds on first load.

## Identity, rollback and locations

- Source SHA-256: `87a7abf2fc3e6117ffacd3053426828255acd1eeab42982de186b76c7c3524e6`
- Export/app PCK SHA-256: `8f33a1e063677dda92de0ea1c9d768568b3ce6d36c6d812f5a7978127a259fc4`
- Signed executable SHA-256: `441bb1a5a2acff1f7a1d9522abee0c5238f527a9dbc008540d478ca4d0a8cf68`
- Sampler SHA-256: `29b09ee6881320efa445452d84597c5186b0f44d568989d948d0505f76783b66`
- Complete candidate: `/Users/Shared/BrineSpace-ipad-optimization-20261020/door-source-sharing/candidate`
- Immediate full rollback **f478**: `/Users/Shared/BrineSpace-ipad-optimization-20261020/corridor-source-sharing/candidate`.
  Its executable and PCK hashes were checked again at final acceptance.
- Original owner backup: `/Users/Shared/BrineSpace-ipad-optimization-20261020/door-source-sharing/candidate/immediately-before-install`
- Portable evidence: `docs/ipad-memory-placement-evidence-2026-10-20/door-source-sharing`.

Frozen Mac/Windows releases and earlier protected rollback/recovery donors unchanged.
