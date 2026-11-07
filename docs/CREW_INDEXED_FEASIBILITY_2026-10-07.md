# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: crew memory representation feasibility

## Objective and acceptance

Find a large lossless memory remedy without cropping, reducing animation frames, changing filtering or adding per-frame uploads. Full PC/Mac performance and release scope remains active. Offline storage estimates do not establish runtime savings or visual acceptance.

## Accepted decisions and constraints

Original PNGs, selected manifests, effective filters, wrapper metadata/identity and normal runtime stay unchanged. Preserve RGB even under zero alpha. Reject rendered pixel differences rather than waiving them as visually small. No automatic quality changes or public upload.

## Current state

Private artifacts under `output/drone-compiled-2026-10-07/`: `audit-crew-indexed-feasibility.py`, `crew-indexed-feasibility.json`, `crew-indexed-linear.gdshader`, `crew-indexed-render.gd`, `run-crew-indexed-render.py`, input/index/palette PNGs and result/log/owner files. No normal game source/art/candidate package changed.

## Verification

- Reused existing complete actual packaged matched run inventory rather than rerunning performance for metadata. All8,188 first-source hashes/dimensions/decoded byte counts match physically frozen source. Pool decoded storage1,610,154,592bytes (~1.500GiB), not full engine/driver residency; excludes generated/mirrored/nonpool images.
- Offline exact RGBA color census completes all8,188 records in14s; no source exceeds65,536 colors,8 fitR8 and remainder RG8. Full canvas plus palette estimates691,858,736bytes (~659.808MiB) less payload; all records beneficial. This is potential representation saving, not achieved GPU allocation or release budget closure.
- Requested filter groups: inherited-only1,462 records311,620,704bytes/potential139,607,600bytes; explicit linear6,626 records1,270,848,768bytes/potential539,981,440bytes; mixed100 records27,685,120bytes/potential12,269,696bytes. Inherited filter is not automatically certified nearest. Mixed source storage must support every requesting wrapper.
-12 sources selected by largest savings across distinct packs: encoded index/palette reconstruction exactly preserves every original RGBA byte. Native Compatibility/RTX4070Ti240 draw pairs:2 filters,5 scales(.25/.5/.73/1/1.37),2 fractional origins and nonwhite tint/alpha. Hardware nearest120/120 exact. Manual four-color bilinear78/120 nonidentical, maximum1/255; **general linear indexed crew replacement rejected**. This test does not certify motion, effects, clips/regions, full crew consumers, other GPUs or performance.
- Initial shader helper referenced fragment-only TEXTURE outside its scope, causing compilation error; preserved setup-error log/results, corrected by explicit sampler argument. Setup failure is not render evidence. First working nearest texelFetch path33/120 nonidentical (max166), rejected; preserved fetch results. Hardware nearest branch uses actual texture sampling and fixes that boundary drift. Final engine run clean, exit0; Python output has Pillow getdata deprecation warnings only, unrelated to engine/art correctness.
- All2,936 owner non-log files unchanged. Native probes resolve isolated user directory before engine writes. Processes terminal; no release assertions/quality changes.

## Next action

Do not install general indexed crew storage or chase driver-specific interpolation rounding as accepted quality. Nearest-only has smaller potential (~133MiB before accounting), needs actual inherited filter/consumer/ownership/effects coverage and would not independently close the large scene budget. Prioritize measured steady rendering/preparation costs and the existing exact compressed-slot provider's remaining Studio ownership/loading costs; preserve its full consumer/save/motion requirements. Original frame p95/p99, memory, loading responsiveness, nine bugs, endurance, target PC and native Mac certification remain open.
