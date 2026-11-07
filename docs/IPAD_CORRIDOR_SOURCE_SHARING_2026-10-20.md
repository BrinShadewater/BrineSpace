# iPad corridor source sharing — October 20, 2026

Installed **brinespace-f4787e18790c179f**, unchanged VM1 native sampler. Full **4b8a**
signed app/export remains the immediate rollback. All five original save files
are SHA-exact after final launch; owner cycle 64 / seven rooms, paused 4× / menu closed.
Frozen Mac/Windows releases and earlier recovery donors remain unchanged.
Not release-cleared: loading, large-view frame rate and process memory remain open.

## Cause and change

`rooms/underwater/corridor_wall_art.gd` cached by variant ID. Its 36 registrations
select regions of just five immutable PNG sheets; each variant could upload the
same sheet again. It now caches by the registration's complete source path.
Region selection, dimensions, filters, colours and authored PNGs remain exact.
The existing last-owner lookup cleanup owns the sole cache: no hidden second
source lookup or extra resource owner was added. A reference CLI flag preserves
the original per-variant path for comparison. Performance breadcrumbs record only
bounded scalar source/texture counts and RGBA capacities, without pixel readback.

The direct-scene native 56-room probe had three separate 6,292,144 B uploads of
`alternate-walls.png`; the candidate has one, a 12,584,288 B capacity reduction.
The full physical title→station path loads more wall variants, so it has a
different working set. Same-package physical reference→sharing verifies
**13→3 cached textures for 3 sources**, removing
**62,917,376 B (60.003 MiB)** of duplicated RGBA texture capacity.
Physical engine texture accounting is **79.971 MiB lower** in this pair.
These are texture capacities/counters, not a guaranteed fixed process-RAM saving.

## Verification

The first meaningful native regression failed 33/40 checks before the fix, then
passed 40/40. Expanded final regression passes 112 checks: all 36 wall variants render
identical native pixels under nearest and linear filters, original source pixels
match, reverse loading shares, overlapping owners retain images, final exit
releases weak references and reentry shares again. No raster assets changed.

Nine actual-PCK suites pass: corridor sharing 112, transit material 618, session
art 26, session material 18, shared floors, initial surface loading 16, navigation
storage 4, navigation prefix 1488 and large-room lifetime 43. Raster 36191 and
source 439 selected / 433 extras audits have zero missing/changed/unknown entries.
Strict signing and app/export PCK equality pass. Four export configurations are
restored byte-exact; native profile fingerprints protect the real Mac saves.
One host check accidentally overlapped export's temporary configuration and was
stopped by the profile guard before BugReport/save access; it is not a product
crash or a passing test. Final acceptance uses the immutable actual PCK.

Physical iPad13,18 / A14 / 4 GB, iPadOS 27.2, native Compatibility, 1920×1334. Same normal
56-room/four-crew checkpoint, paused 1×, same restored owner metadata and populated
prepared cache. Recorded PNG rebuild jobs 0. Ordered measurements:

| Run | Setup ms | UI/grid ms | Restore ms | Textures / sources | Engine texture MiB | Latest process MB |
|---|---:|---:|---:|---|---:|---:|
| baseline | 8987 | 2650.455 | 3806.757 | not instrumented | 981.430 | 2153.304 |
| candidate-first | 9766 | 3471.188 | 4000.116 | 3 / 3 | 901.459 | 2085.130 |
| candidate-repeat | 6898 | 2762.944 | 1619.444 | 3 / 3 | 908.130 | 2167.623 |
| same-pack-reference | 8749 | 2789.929 | 3735.689 | 13 / 3 | 981.430 | 2137.608 |
| candidate-after-reference | 8948 | 2698.515 | 3685.412 | 3 / 3 | 901.459 | 2080.542 |

No controlled improvement to initial loading is established. Covered station
setup excludes later first redraw. Crew-cache finish/restore waits still dominate;
first-process and same-process repeat are separate workloads. Latest footprint
and VM walks are sparse ordered samples, not statistical bounds or leak clearance.
Separate requested VM samples: off: process 2143.637 MB, mapped GPU-driver tag100 resident 795.148 MB; on: process 2080.509 MB, mapped GPU-driver tag100 resident 733.381 MB. Region pages may alias and are
not additive to charged footprint; exclude the walks from timing comparisons.

Normal 1× active fixture completed **5.327 endpoint-counted
active minutes** (7.947 wall minutes), cycles 70→89,
all four alive / errors 0. Normal costs/caps/failures remain enabled; initial reserves
are seeded. Sampled peak 2222.821 MB, end 2206.912 MB;
first/last-minute median change 53.445 MB. Sparse active
buckets median 14.31 FPS, max 166.893 ms.
Observed pauses are excluded from the active counter; endpoint sampling is not continuous frame coverage.
The first memory minute includes dialogue/cache warming. Its median difference
is not a leak rate or directly comparable to another revision's starting window.
This short run is not long-soak, survival/balance or release clearance. The known
large fixture can accumulate high crew needs; inspect its saved health before
extending it rather than disabling normal failures.

Actual card return and Save/title/Continue/Save pass. All checkpoint fields match
except `_path`, `event_history` and `saved_at`; paused timer matches exactly.
The existing Continue 1× reset is manually reselected 4× for parity. Five incoming
originals are hash-exact again after final owner launch. No new paid-construction,
physical multitouch or background/resume certification is inferred.

## Identity and continuation

Branch `codex/ipad-memory-placement-2026-10-17`, HEAD
`81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted uncommitted work.
Compiled source SHA256 `f4787e18790c179f7d6ff5e6f84f59bd7e9065a797ef9306fae92d4b22a2b077`.
PCK `a59e90bc7586dc986a50903461f366b9f8e6bfca8b3cda9de36558a1f3c7cd7c`.
Signed executable `ef45977bbe5ad1ef9eeb70a5aa5fc716497ce011b11598d9cc2bb553ba895aaa`.
Native sampler `29b09ee6881320efa445452d84597c5186b0f44d568989d948d0505f76783b66` (unchanged VM1).

Complete candidate/evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261020/corridor-source-sharing/candidate`.
Immediate rollback: `/Users/Shared/BrineSpace-ipad-optimization-20261020/navigation-link-storage/candidate`.
Keep 99aa, 7bf9, f729, 500, 4ec, 7675, 7bb and all recovery archives as well. No commit,
push, merge, public upload or frozen-release replacement occurred.
Portable evidence: `docs/ipad-memory-placement-evidence-2026-10-20/corridor-source-sharing`.

Next isolate the remaining crew finish/restore and first redraw costs. Check
other immutable source factories for duplicate uploads before trying lossy or
lower-resolution artwork. Keep measurement conditions matched; memory counters
alone do not establish faster loading or a safe release footprint.
