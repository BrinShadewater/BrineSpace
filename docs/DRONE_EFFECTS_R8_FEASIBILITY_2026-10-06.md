# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: lossless mining effects R8 feasibility

## Objective and acceptance

Reduce measured huge effects uploads without altering selected particles/alpha/clocks/coordinates/filtering. Continue full PC/Mac release and performance plan.

## Accepted decisions and constraints

Private probe only; normal art/runtime unchanged. Both selected effect sheets use152 distinct exact RGBA colors, including transparent RGB/alpha values. Full-coordinate R8 indices plus256x1RGBA palette preserve every source byte, original sheet dimensions and hardware nearest sampling. No color quantization, frame removal, downscale or atlas rearrangement. Linear/unsupported materials still require original fallback before integration.

## Current state

output/drone-effects-indexed-2026-10-06/{prepare.py,prepare-r8.py,inventory.json,west/,south/}. Per-heading encoding/results/owner JSON, native logs, PNG index/palette assets, native probe/runner and selected original/indexed captures. First inventory RG8 superseded by single-channel R8. Source hash recorded, exact reconstruction across all144506880RGBA bytes each. R8 index PNG47,267/45,430bytes; palette1024decoded bytes. Final index+palette36127744bytes vs144506880original (~75% smaller, about103.36MiB less each). These are per-resource payloads, not measured whole-station residency savings.

## Verification

Both native tests1080exact comparisons each, zero failures/errors, clean exits:all180cells×3scales×2mirrors. Each source90nonempty/90empty cells. At1x every nonempty cell must produce visible original and candidate output; smaller scales can legitimately sample away tiny particles, and all empty-cell images compare exactly. Full600px viewport/correct mirrored bounds avoid earlier West-body fixture blank flaw. Explicit PNG buffer loading and Image.FORMAT_R8 conversion; palette RGBA PNG decoded normally. Python PNG index roundtrip exact. Original source frames/pixels unchanged.

Upload-call timings: Westoriginal26.929ms vsR8indices7.372+palette.044ms; Southoriginal28.632 vs6.794+.039ms. One isolated pair per sheet, cold/warm state uncontrolled; not three gameplay runs or guaranteed runtime savings. Existing original-coordinate nearest pipeline unchanged; no indexed linear filtering claim. Full copies coexist for reference in test, so no actual scene memory reduction established.

Selected West frame60 indexed capture visually inspected (small faint original mining particles, retained at selected scale/tint); matching original/indexed captures retained for both. Both owner2936non-log fingerprints unchanged, terminal processes. No normal code/tests admission or release certification this turn.

## Next action

Extend existing private West-body session provider to source-keyed weak wrappers for both effect sheets and South body. Separate RG8(body) andR8(effect) shader decoding, including current flooding shader, while preserving unknown-material/linear original fallback. Decode indexPNG on workers, GPUupload only aftercompletion, accountallindex/palette/fallback bytes under sharedpressure; avoid ordinary duplicates and redecoding churn. Validate complete body/wheels/cargo/effects/native layering/lifecycle and matched mixed40-room4xupload aggregates before admission. Remaining North start/wheel uploads and regular renderer/system costs still require measured remedies; full release gates remain open.
