# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: cumulative performance candidate

## Objective and acceptance

Measure the complete accepted source in an actual debug=false PC/Mac candidate.
The original performance, memory, loading, bug, endurance and platform gates remain
open. Controlled component improvements do not certify cumulative gameplay FPS.

## Accepted decisions and constraints

Use the maintained release exporters and identical physically frozen inputs.
Preserve selected pixels, timings, filtering, layering, owner layouts and saves.
No publishing, broad cleanup or renderer upgrade is authorized by this milestone.

## Current state

Physical source: `D:/bs-release-20261009/source`. `freeze.json` records SHA256 of
57,759 copied files and selected runtime dependencies: 36,246 files / 3,593,525,562
bytes. Source Git commit eb1cb03b1f34384362546daeac517508a00c6cae plus working changes;
the commit alone does not identify the frozen source. Independent snapshot Git
metadata uses read-only object alternates with LF line endings. A failed metadata
setup was repaired without recopying or changing the selected source.

Local drivers: `output/renderdoc-tools-2026-10-08/`. The initial Windows exporter
session 63490 failed; full import 51813 and resumed exporter 21008 succeeded.
Its manifest identifies build `brinespace-60b400041c69f41a`, 36,245 shipped
entries / 3,593,488,256 source bytes; the snapshot additionally contains the export
plugin/preset and verification support inputs. Windows delivery candidate is in
`D:/bs-release-20261009/windows`; PCK size 3,623,027,405 bytes. EXE SHA256
7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76;
PCK SHA256 e8aefdd0e6b3ccc7c10cd9aae877164b8cbf2e969ffdcac5a9456b5ac866f1c3.

## Verification

Physical source hash verification complete; owner fingerprint 2,936 files unchanged.
Release manifest tests 10/0, assertion safety 2/0, Mac exporter selection 2/0.
Resolved export user directory verified under isolated D: profile. Mac selected
template matches the SHA512-verified official archive and Godot 4.7.2 editor.
Windows raster roles: 63 resource-imported, 33,804 raw keep. Export has reached
Godot initialization, then asset scan and first font import. Windows Event 1000
records Godot access violation 0xc0000005 at offset 0x3e0bf12; no script error in
the export log and no package produced. Owner 2,936 unchanged after failure.
Minimal import with the exact font bytes and import parameters succeeds (exit 0),
so corrupt font input is not established. Separate full-project import succeeds
with no engine/script errors. Resumed maintained exporter succeeds with the same
source fingerprint. This staged build passes; the original crash cause remains
unexplained. Preserve failed-first-export-engine.log and the Windows crash record.

Independent isolated PCK audit: 35,779 raw entries checked, missing/changed/remapped/
unexpected all zero. Actual release normal-entry smoke: zero failures, debug=false;
intro, New Game architect selection, dialogue Continue, simulation advances,
visible station, F8 pause/report/snapshot/checkpoint preservation all pass. No
missing-art placeholders or captured engine/script errors. 1080p gameplay and
report screenshots visually reviewed; this does not close all UI/visual reports.
Fixture SHA256 acc09fe570fa50d26660d1f09cfe2a987961354676b8d98d310047a0abe2e75d.
First smoke driver failed before launch on a helper-name typo; corrected to the
maintained prepare_release_copy helper. That setup failure is not gameplay evidence.
Audit, import, export and successful smoke each retain owner 2,936 unchanged.

Maintained Mac export session 89218 completed successfully, including Universal 2
bundle structure. All 36,245 selected source entries match Windows. ZIP SHA256:
9465a5f431ba6c51602c0a4d1205d236a35661558249217041bae5dcea746b9a.
Extracted bundled Mac PCK is byte-identical to Windows (e8aefdd0...); independent
Mac PCK audit session 73421 passes 35,779 raw entries, zero missing/changed/
unexpected. Owner 2,936 unchanged. These checks ran on Windows; native Mac
gameplay, Developer ID signature, Gatekeeper and notarization are unverified.

Original report input recovered from `output/performance-bug-pass-2026-10-04/`
and copied to `D:/bs-release-20261009/benchmark-input/`. Report 20261004-015752;
SHA256 19d36365355c87ec7c8b10dea8457840a8081a29453b594077bc5044f0797a3b.
Current frozen RunSave reader validates it and confirms 12 rooms, without restoring
or changing it; owner 2,936 unchanged. The input is a digest-prefixed Godot binary
Variant save, not JSON; initial Python text inspection failed without writing it.

Full native Windows benchmark session 35863 completed, exit 0: fresh/reported/large,
1920x1080/2560x1440, three repeats, 180 measured frames per action/speed, all standard
actions, bounded trace enabled. Preflight found no competing engine/game process.
Exports and PCK audits finished before this batch. Temp/profile relocation uses D:
scratch. This is the owner's RTX4070Ti, not certification of GTX1650/M1 targets.
Evidence is `D:/bs-release-20261009/benchmark/` plus benchmark-launch.log. First
fresh 1080p run completed with valid marker/debug=false/no logged errors: 21/24
phases pass the combined gate; scene request-to-ready 13,278.982 ms, end textures
3,126.894 MiB, one automatic report. These are provisional single-run observations,
not release certification or a budget acceptance; phase actions can change room
counts and residency. Final batch acceptance below supersedes these provisional observations. Inspect completion markers, errors, resolved profiles and final owner
fingerprint before accepting runs. Loading labels retain uncontrolled OS disk-cache
scope; do not label fresh profile as a controlled cold-disk measurement.

Latest provisional observations: all six fresh runs completed cleanly. 1080p warm
request-to-ready 4,980.614 / 4,442.644 ms; 1440p warm 4,351.751 / 4,475.254 ms.
First fresh run starts with one room / no active actors and 3,096.769 MiB textures.
Crew pool startup totals: 16,296 requests, 8,188 uploads / 1,610,154,592 decoded
bytes uploaded; 7,593,675 us decoding and 842,018 us alpha bounds. This is upload
traffic, not a complete surviving-storage/GPU attribution. Cold prefetch has zero
worker submissions/unused results; review-file decode waste is not established.
One fresh placement frame 101.316 ms; grid work 73.805 ms and simulation 20.340 ms
reported. Nested draw stage timings overlap; do not sum them. Zoom p99 28.410 /
25.052 ms also fails in that run. Actor activity is sampled before the phases,
not a claim that crew stays inactive throughout the workload.

First two original 12-room 1080p runs completed cleanly, 11/24 and 6/24 passing
phases. End textures 3,587.550 / 3,591.808 MiB; request-to-ready 12,261.635 /
6,240.548 ms. Memory exceeds the 2 GiB scene budget. No matched older-package
comparison or batch-level owner acceptance yet; continue all repeats/resolutions
and large scene before selecting the next measured remedy.

Additional package lead: 1,320 `world-review` entries total 814,900,103 bytes;
sample manifest reasons cite crew_sprite_player.gd dynamic directory. Root maps
also have live external consumers in airlock, Bill, crew life and grid code; they
are not unused constants. Necessity/residency not yet established. Audit precise
catalog/frame/clearance/locker consumers before narrowing dependencies. Preserve
archives and runtime historical bindings; do not infer FPS impact from pack size.

## Next action

Benchmark complete: 18 clean runs, 77,760 samples, 177/432 passing phases,
1,512 frames >50 ms / 48 >100 ms, max193.314 ms. All owner 2,936 unchanged.
Large all144 phases fail; sampled texture maximum ~4.73 GiB. Private Bill
subclass-cache regression 26/16 red ->26/0 green, frozen source unchanged.
See [final batch and next implementation](CUMULATIVE_PACKAGE_BENCHMARK_2026-10-09.md).
Prepare lossless crew-storage trial against this exact candidate, including the
verified private lease fix and inheritance guard; require native visual/save/frame
and memory comparisons before admission. Match against the retained previous
normal package and attribute the remaining CPU/render bottlenecks.
Investigate dependency over-selection independently after benchmarking. Save/relaunch, all original bug reports,
endurance, target GTX1650/M1 hardware, native Apple Silicon gameplay, Developer ID
signing and notarization remain open. Retain prior packages for rollback.
