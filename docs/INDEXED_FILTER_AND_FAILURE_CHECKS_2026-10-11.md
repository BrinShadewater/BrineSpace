# Indexed renderer filtering and failed loads

Updated: October 11, 2026 · Project: BrineSpace · Task: performance readiness

## Objective and acceptance

Check the private provider's original-texture fallback, failed decoding and supported
filter/flood rendering in the actual release executable. Preserve pixels, selected
effects, identity and truthful memory accounting. This is not full release acceptance.

## Accepted decisions and constraints

Private candidate only; keep selected art/default effects. Muted secondary display,
isolated profiles, owner fingerprints, existing executable/assets reused. No owner
data or art changes. Keep test output small.

## Current state

New private bank/motion/display variant:
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/indexed-failure-filter-validation/`.

Reproduced the previous Display.original_texture failure with a missing source:
actual debug=false emitted `Invalid image: null` and returned null. Display now uses
the maintained SafeImage diagnostic placeholder when the original is unavailable,
records actual image bytes plus indexed storage and notifies cache bookkeeping once.
Valid fallback pixels/identity remain unchanged. Missing art stays reported; a
placeholder does not make missing art release-acceptable.

Bank adds a shared PNG preflight/decode helper: missing files, truncated headers,
invalid signatures, failed decoding and empty images return null; selected channel
conversion occurs only after decode succeeds. Motion uses it for synchronous and
worker decode before the existing bank validation/fallback path.

`validated-resources.json` names all three revised scripts with the unmodified
selected catalog; `source-identity.json` retains their hashes. Temporary corrupt
fixture bytes are only in the failed-decode test overlay, never the integration map.
No production source changed.

## Verification

Actual Windows Godot 4.7.2 debug=false executable, RTX 4070 Ti:

- 35 filter/fallback checks pass. Twelve rendered cases compare complete 80×80
  viewport pixel hashes: R8/RG8, direct and inherited nearest/linear filtering,
  unknown/default filter fallback, and flood material. Cases include transparency,
  tint and fractional transform. All twelve exact. Backend selection exact; original
  texture identity stable; allocation callback occurs once with actual bytes; missing
  original produces a valid drawable placeholder, correct bytes and a recorded warning.
- 18 failed-decode checks pass: test-only eight-byte PNG-signature files replace one
  index and one palette in a small overlay. Bank records the correct decode stage,
  preserves original pixel hashes and bytes. Immediate and actual worker index loading
  both finish with ordinary storage and consume their jobs.
- 64 selected-catalog checks pass on the changed decoder/display: all 21 real assets
  use indexed storage, preserve dimensions and exact storage bytes, with no fallback.

117 final checks, zero failures. The filter suite has one expected missing-art warning;
no engine errors in final suites. The baseline null-image error remains in baseline.log.
The initial all-catalog result destination was corrected to its own new directory and
rerun; final result.json matches the final native log.

Evidence in `indexed-failure-filter-validation/`: `baseline.log`, `missing-fixed.log`,
`filter-native.log`, `filter-result.json`, `decode-native.log`, `decode-result.json`.
All-catalog evidence in `indexed-failure-valid-catalog/{native.log,result.json}`.
Runners live under `output/renderdoc-tools-2026-10-08/check-indexed-*.py`.

Both final owner fingerprints: 2938 before/after, zero changes. Jobs terminal,
runtime override restored. New directories approximately 0.141 MiB; C: 124.20 and
D: 70.69 GiB free. No large image captures or asset copies.

## Next action

Use the new integration map for representative real-station rendered comparisons
with the deterministic survey fixture. Synthetic filter tests do not certify all
selected animation joins, art, arbitrary custom materials, parent-material inheritance,
all flood states or real-station pixels. Also cover both indexed and original artwork
unavailable in the motion path and PNG corruption beyond the header preflight.

Then measure floor/lighting rebuild and upload hotspots for FPS. Do not claim previous
performance timings certify these changed loaders. Keep provider private; broad frame,
workload, endurance, target-hardware, packaging and Mac gates remain open.
