# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: combined crew storage in actual release runtime

## Objective and acceptance
Continue full PC/Mac readiness. Validate combined lossless crew storage against actual debug=false execution before admission. Full performance, peak/lifetime memory, loading, bug/UI, endurance and platform gates remain open.

## Accepted decisions and constraints
Keep this prototype isolated. Low free disk space (~2.55 GiB at start) prevented another full ~3.6 GB PCK without cleanup. Instead, use a tiny text-resource diagnostic overlay with the retained physical QA release copy. This is actual release-executable evidence, not a new fully audited delivery build. No normal runtime/art/layout/archive changes or publication.

## Current state
`output/all-crew-storage-2026-10-07/packaged-startup/crew-storage.pck` contains individually hashed shared helper scripts and physical current Main/Grid/scenes for control/candidate. Dynamic overlay loading occurs before scene load; no script reload. Both lanes compress Veld/James/Marsh; candidate adds Bill. Explicit runtime checks require debug=false and candidate Bill's actual subclass path; required bank adoption executes outside assert. Identity files retain EXE/base PCK/overlay/individual inputs and exact physical adapter hashes. Previous delivery and its frozen source stay intact.

## Verification
Actual release startup pair: 1751.229 -> 1060.765 MiB, saving 690.464 MiB; both settled exits 128.863 MiB, session router released, missing=0. Request-to-ready 9.371/8.950 seconds; one uncontrolled-cache diagnostic path, not normal title loading or cold/warm acceptance. Candidate compresses 1,610,154,592 raw-equivalent bytes to 139,203,414 bytes. These raw-equivalent counts are not retained decoded RAM measurements.

Active 40-room 1920x1080 uncapped release pair: 9 phases ×60 frames per lane, idle/pan/zoom at1/2/4x, four active crew including real legacy Bill, drones/production. Exact crew snapshots, drones/phases, doors, lights, powered-room counts, zoom and large-prop state match at all endpoints. Candidate presents73 Bill/215 James/63 Marsh/138 Veld distinct frames, missing=0. Both logs clean. Every phase saves690.464MiB; candidate endpoints1672.527–2346.686MiB (~1.63–2.29GiB), end2102.737MiB. Endpoints are not transient peaks or memory certification.

Candidate p95: idle/pan/zoom1x34.020/39.158/44.338ms;2x34.340/35.230/67.090ms;4x46.532/48.555/56.146ms. Four phases improve, five regress; no reliable FPS gain established. All phases fail16.7ms. Candidate16 measured frames>50ms, none>100ms, max82.491ms. Earlier native100.879ms burst remains unresolved, not closed by this short run.

Worst frame sampler520 corresponds to completed519: three drone atlas uploads on519 total337,182,720bytes (~321.56MiB)/29.406ms. Aggregate drawing58.786ms/260callbacks includes exterior-actors39.704ms and live-rooms13.771ms; labels overlap and must not be summed with upload/render scopes. This worst frame has coincident uploads, unlike the previous native redraw-only worst. Both causes remain. Automatic reports saved1 per lane; their exact pregame/fixture timing is not certified here and must be accounted for in broader startup/overhead acceptance.

Candidate screenshot viewed: station art, card hand, portraits/meters and interface present; synergy popup and cards occlude station. No full motion/original-nine-bug visual acceptance.

All child processes terminal. Both owner fingerprints2936unchanged; QA benchmark adapter restored byte-identically after each run. Evidence: `packaged-startup/{identity,owner,control,candidate}.json`, `packaged-large/{identity,owner,control,candidate,comparison}.json`, logs and PNGs. Raw comparison retains all worst-frame profiler fields.

## Next action
Continue12-room and repeated transition/peak/lifetime evidence, more Bill arrival/rise/cargo paths and normal title/Continue entry. Prepare a separately frozen complete candidate and exact outside-checkout PCK audit before normal admission/certification. The new memory headroom supports investigating bounded drone working-set residency, but any budget change requires measured peaks and matched upload reduction. Address redraw-only live-room/floor/terrain bursts alongside atlas uploads. Do not treat one pair or a diagnostic overlay as release readiness; target hardware/Mac/signing/notarization/endurance and all original gates remain open.
