# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: collection storage and upload pacing

## Objective and acceptance

Continue full PC/Mac performance readiness. Verify exact native output and measure whether lossless storage reduces the normal-game drone upload stalls without worsening overall memory or frame budgets. Prototype evidence only; no normal provider admission.

## Accepted decisions and constraints

Original pixels, frames, clocks, filter choices, effects, source artwork and owner layouts preserved. Existing twelve-source private provider already includes South/West mining bodies/effects: these four sheets were revalidated, not four new savings. Four new sources are South/West collection body/cargo. Both matched station branches use the installed normal Moonbay water batching and the same existing private crew/dock provider support. Do not compare their texture totals to normal-source totals as though only collection storage changed.

## Current state

`output/drone-normal-cache-2026-10-06/`: eight source-hashed exact encodings, per-frame native probes, expanded sixteen-source provider, complete composition fixture, matched twelve/sixteen station lanes, and actual title/save/Continue fixture. Changed normal runtime files: none. Source art unchanged. Existing private twelve-source files copied with hashes retained in provider-provenance.json; only four collection paths added.

## Verification

- Native eight-sheet probes: 7,200 exact raster pairs, 6,083 visible and 1,117 blank pairs. All authored cells, three fractional sizes and mirrors; sparse effects account for blank output. Zero errors/failures/leaks/warnings. Isolated original uploads total202.226ms versus encoded+palette82.492ms; not whole-game latency certification. All written RGBA pixels reconstruct exactly, including transparent RGB. Mining bodies about28ms→13–15ms, effects28ms→7–9ms, collection21–23ms→9–10ms in this isolated lane.
- Complete sixteen-source composition: 4,704 checks/840 exact pairs, clean native exit. Includes mine/collect/drive/steer, cargo, inherited nearest/linear fallback, dry/flood/unknown shader, modulation, transforms, overlap, source identity, fallback byte accounting and last-owner cleanup.
- Matched native mixed40: all six full crew/drone/door/light/power/zoom states equal; no missing art, engine errors or selected ordinary duplicates. Actual diagnostic module/catalog counts12/16 verified. Final screenshot retained and inspected. Owner2,936 files unchanged throughout all lanes.

| Phase | Twelve-source p95 ms | Sixteen-source p95 ms |
|---|---:|---:|
| Idle1× |38.811|39.960|
| Pan1× |43.010|43.146|
| Idle2× |39.138|39.967|
| Pan2× |41.657|41.046|
| Idle4× |42.513|44.601|
| Pan4× |53.570|45.596|

Sampled frames over50ms decrease5→2; maximum60.934→54.910ms. Total ordinary/indexed uploads41→40, upload time120.171→102.235ms. Final texture endpoint2,715.11→2,777.51MiB (+62.40MiB): no overall memory gain. At that endpoint two ordinary West collection sheets disappear (-183.75MiB), two encoded replacements total~91.93MiB, but three other ordinary travel/stop sheets and a pose remain (+138.58MiB). Cache bookkeeping delta+46.76MiB differs from engine total; held draw resources are not fully accounted by cache tables, so do not claim the engine difference completely explained. Earlier five endpoints equal; new sources become active only in final phase. Mixed pacing/no60FPS acceptance.

Actual two-cycle New Game/title/save/Continue with Studio, crew/fleet restoration and all four new collection allocations:244 checks pass, zero failures/errors/leaks/exit warnings. Old collection weak references release, title indexed factory/jobs/textures/bytes empty. Initial fixture returned to the earlier twelve-source title, causing second-cycle backend mismatch and invalid property access; exact failed process stopped, logs/source preserved. Corrected one private Main title path; successful lane replaces failed evidence, not a normal gameplay bug fix. Two cycles are not endurance, large-scene memory acceptance, packaged or Mac certification.

All native handles terminal. Profile fingerprints unchanged. Native body/station captures inspected; no blanket motion or packaged-art acceptance.

## Next action

Resolve mixed cache residency/held-command accounting and remaining dock/full-room/flip/type/fallback coverage before normal provider admission. Continue larger sustained CPU/rendering costs: even frames without uploads remain above budget. Refresh actual release checks after accepted changes; normal memory/loading/frame gates, original nine packaged reports, two-hour large soak and actual Windows/Mac certification remain open.
