# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: activity cache path attribution and six-sheet lossless proof

## Objective and acceptance

Continue full PC/Mac performance/release readiness. Identify the actual resumed-activity texture cache growth and test lossless storage/upload reduction while retaining source pixels, atlas coordinates, frame count/timing and selected quality. No normal provider admission.

## Accepted decisions and constraints

Private artifacts only. Preserve original PNGs/runtime declarations and the frozen six-source provider. Do not infer CPU growth from GPU cache counts. Extend indexed storage only after exact reconstruction/native checks; eventual integration still requires filtering/material/layering/fallback/lifetime and matched workload acceptance.

## Current state

- Path inventory evidence: `output/scene-dependency-warning-2026-10-06/cache-paths-two-*`.
- Encoding/probes/results/source hashes: `output/drone-activity-indexed-2026-10-06/`, six named sheet subfolders. Preparation/runner scripts in the dependency-warning evidence folder.
- New private RG8 indices/RGBA palette PNG sidecars for South/West/East wheel layers, East/South driving and South right steering. Original art unchanged; no runtime catalog/backend edits yet.

## Verification

Native path inventory passes 210 checks with zero failures/errors/exit warnings. Summed per-path bytes equal each cache's counter at every recorded boundary. Fresh before fixture mining: ordinary cache empty. After first selected exercise: South/West wheels (48,168,960 bytes each) plus one 4-byte empty image. After Continue but before further simulation: only the empty image. Subsequent activity loads East wheels/driving, South steering/driving/wheels and placeholders; selected exercise then adds West wheels and evicts East drive from that bounded cache.

Settled ordinary cache 96,337,924→240,844,816 bytes is accounted for exactly by three additional 48,168,960-byte sheets (East wheels, South right steering, South drive) plus 12 placeholder bytes. The earlier North-work hypothesis is rejected for this specific growth. The North work atlas remains a separate previously measured upload concern. No RGBA fallback is indicated by the ordinary entries, which are regular images. This does not fully attribute the CPU static-memory step.

All six sheets are 2688×4480/60 original cells. Palettes retain 18,937–35,510 unique RGBA values; RG8 index capacity suffices. Every original decoded RGBA byte reconstructs exactly, including transparent pixels. No atlas rearrangement, frame removal, downscaling or lossy color conversion.

Six native probes: 360 exact pairs each, 2,160 total, zero mismatches/errors/warnings. Every cell tested at three fractional/native scales and mirrored/unmirrored, original tint/alpha. Nonempty guards and selected captures verify actual output. Drive-South indexed capture inspected. These are individual-sheet nearest-filter proofs, not full-station material/fallback/motion certification.

Aggregate original RGBA payload 289,013,760 bytes (275.625 MiB); new RG8 plus palettes 145,075,200 (138.355 MiB), ~49.8% smaller. One isolated upload observation per source: original 10.729–13.390 ms; indices+palette 5.200–5.880 ms. Do not treat these as repeated whole-game frame-time improvements or include encoding time in loading claims. No CPU peak improvement established.

All 2,936 owner non-log files unchanged in both completed native lanes; processes terminal. No normal source/art edits, export, commit or publication.

## Next action

Create a physical private twelve-source provider by extending the existing six-source catalog; retain fixed release-safe PNG loads and minimal shader preparation. Run actual composition/filter/flood/fallback and Main lifecycle checks, then matched current 40-room activity traces including CPU peak, decode/upload timings, FPS and cache ownership. Accept only measured gains with selected quality intact. Original memory/loading/frame/packaged bugs/endurance and actual Windows/Mac release gates remain open.
