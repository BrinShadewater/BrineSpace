# iPad hidden crew commands and first-redraw capture — October 20, 2026

Installed **brinespace-19db95fa680a52e5**, unchanged VM1 sampler, on the physical A14
iPad13,18 / 4 GB / iPadOS 27.2. Source HEAD remains
`81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted uncommitted work.
This is scoped validation, not release clearance. Initial redraw and memory growth remain open.

## Changes and verification

Crew pose routing previously retained immutable image leases and canvas commands
when an owner or its ancestor became hidden. Visibility retirement now clears the
hidden canvas commands before releasing its leases and requests a redraw for reveal.
Visible peers retain their images. Normal exit disconnects the visibility callback.
No in-flight image is mutated. `--reference-hidden-crew-leases` disables only retirement.
Bounded scalar diagnostics report hidden owners/leases and retirements.

A bounded capture records layout/centering under the loading cover and five
post-draw intervals after it leaves. These are CPU/render-signal wall intervals,
not GPU execution timestamps. Existing waits, pause/reading behavior and simulation
ordering are preserved. Weak scene references cancel capture on scene replacement.
Grid microsecond counters are since the performance monitor's last read, potentially
including multiple canvas draws; they are not independent exact per-frame GPU costs.

Red/green: hidden direct/ancestor leases failed before the fix; expanded native
pixel/peer/eviction/reveal test passes 13 checks. Redraw capture passes 11 checks,
including cancellation and caller-dictionary ownership. All **21 actual-PCK suites**,
source/asset audits and strict signing pass. The final source audit has 440 selected
scripts, 433 known extras, zero missing/changed/unknown. Asset audit checks 36,191
entries with zero missing/changed/unexpected. Isolated native tests preserve the
owner profile; export configuration is restored byte-exact.

An earlier pre-install candidate was superseded only to add covered-render timing;
it was never installed. A reused audit scratch directory caused a false positive
from a test PNG on disk; the audit was rerun from a fresh empty directory and passed.
No asset was removed from the package to bypass the check. The loading-covered
native test briefly overlapped a rejected export attempt and is not the sole gate;
the final exact-PCK loading transition test passes independently.

Fresh-process comparisons deliberately terminate the exact validation PID through
devicectl. The resulting unclean-session notice is an expected test artifact;
it is not by itself evidence of an iPad crash. Notices were dismissed through UI.

## Physical loading comparison

Same package, separate fresh processes, same paused 56-room/four-crew checkpoint,
normal rules and seeded initial reserves; reference retirement off → candidate on.

| Load | Station setup ms | Covered reveal ms | First uncovered interval ms |
|---|---:|---:|---:|
| candidate-first | 9202 | 66.490 | 766.027 |
| candidate-repeat | 6088 | 69.638 | 192.250 |
| same-pack-reference | 8027 | 76.917 | 754.640 |
| candidate-after-reference | 8083 | 66.785 | 814.790 |

Reference/candidate latest sampled process footprint:
**2088.095 → 2078.281 MB**;
engine texture accounting **893.462 → 893.462 MiB**.
These ordered samples do not establish a fixed RAM saving. Loading/first redraw
shows no improvement from retirement. Fresh first uncovered intervals remain
about 0.75–0.81s; the warmed same-process repeat is lower. Grid CPU accounting is
large in the first interval, but finer stage/driver attribution is still required.
Do not add overlapping grid counters and render-signal intervals.

## Longer run and owner restoration

Normal 1× 56-room/four-crew test: **20.120
endpoint-counted active minutes**, 22.606 wall minutes,
cycle 70→133. All four crew active/alive;
health evidence is retained in `soak-health.json`.
Logged errors **0**. Sampled footprint peak **2225.557 MB**,
end **2187.563 MB**; first/last-minute median difference
**17.375 MB**. Sparse active bucket median
16.72 FPS, maximum sampled frame
316.670 ms. Dialogue pauses were handled through actual
UI and excluded from conservative active duration. One-second memory samples and
sparse frame buckets are not continuous capture or long-term leak clearance.

Actual card return and Save/title/Continue/Save pass, with complete gameplay state
and exact paused timer preserved. Final five original files are SHA-exact after
final launch. Owner cycle 64/seven rooms, paused 4×, menu closed. No new paid-building,
multitouch or lifecycle acceptance is claimed in this pass. Complete b770 rollback,
frozen Mac alpha/Windows builds and recovery donors remain unchanged.

Hidden command retirements reached 133, with
16 hidden owners and 0 hidden leases at end.
Crew cumulative decoded bytes 5245.137 MB are separate from its
18.475 MB retained cache; uploads 31,574. Drone uploads
25,347, retained cache 62.742 MB. This identifies
substantial bounded-cache churn, without assigning all charged growth to it.
This synthetic workload is not long-term balance or crew-care clearance.

VM snapshots changed GPU-driver tag 100 residency 726.532→746.078 MB and
malloc-small tag 2 residency 68.452→163.791 MB from paused load to post-run. These
mapped categories may alias and cannot be added to or substituted for physical
footprint. Allocation-stack attribution remains open.

## Investigation limits and next target

A native 56-room probe exercises hidden-owner retirement with unchanged cache-byte
accounting; its allocator difference is not a physical RAM guarantee. The old 113,886
navigation segment memo entries cost about 10.24 MB in a focused native probe, so no
cache-capacity change was adopted as an explanation for the prior 108 MB malloc-small
increase. An Allocations attach to fresh device PID 7477 failed with 'Cannot find
process'; there is no successful allocation-stack attribution. A separate native
heavy-draw probe completed but did not retain the startup stall; exclude it as a
first-redraw benchmark. VM tag residency can alias and is not additive to footprint.

Next isolate first-visible static/grid/content work and allocator churn with bounded
stage instrumentation, retaining the reference switch and exact pixel/lifetime gates.
Do not claim that hidden retirement resolves startup or sustained memory growth.

## Identity and evidence

- Source SHA-256: `19db95fa680a52e50cc76892a58553ce39fe96c4dee6aee107a38fab3a22c6cf`
- PCK SHA-256: `d95f9d13b56f2ba38776e9b707b3b574c140cf76c8ef399064a7867951aec9ad`
- Executable SHA-256: `7d954fd3d24bb237b9ced85b65dc25925d00e14e7490f27101c63a6c445ebdaf`
- Native sampler SHA-256: `29b09ee6881320efa445452d84597c5186b0f44d568989d948d0505f76783b66`
- Complete candidate/evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261020/allocation-redraw-pass/candidate`.
- Immediate complete signed rollback: `/Users/Shared/BrineSpace-ipad-optimization-20261020/navigation-template-rows/candidate` (b770).
- Raw saves, reports and traces remain outside the repository. See
  `FINAL_VERIFICATION.json`, `comparison-summary.json`, `pack-tests.json`,
  `pack-audits.json`, touch logs/screenshots and `soak-health.json`.
