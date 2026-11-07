# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: native lossless mask/alpha effects

## Objective and acceptance

Reduce effect texture storage/upload work without palette-shader/command-backend
cost. Preserve pixels, sampling, timing and unsupported-context original fallback.
Private feasibility only; full performance/release goal stays open.

## Accepted decisions and constraints

Nearest white-RGB contexts only for initial integration; linear MUST use original
art after native mismatch. No shader, source art, frame count, size or quality
changes. Normal renderer untouched. Native tests muted/secondary/isolated, bounded.

## Current state

Three derived LA PNGs: binary luminance encodes black vs(135,139,125), alpha retains
original bytes. Constant color supplied through native draw tint. Original PNGs
and hashes untouched. Scripts in `output/renderdoc-tools-2026-10-08/`:
`build-native-effect-masks.py`, `check-native-effect-masks.py`,
`check-native-effect-masks-all-frames.py`, `check-native-effect-mask-memory.py`.
Artifacts under `benchmark-input-isolation/native-effect-masks/` and adjacent
`native-effect-mask-pixels`, `native-effect-mask-nearest-all`, `native-effect-mask-memory`.
Only250668bytes of new PNGs; no screenshots/runtime copies.

## Verification

PNG roundtrip reconstructs EVERY original RGBA byte of all three sheets, including
transparent RGB:144506880bytes/source, dimensions2688×13440. Native PNG loading
detects FORMAT_LA8/data72253440bytes, versus originalRGBA8/144506880bytes.

Native debug=false broad oracle2304 mixed-image pairs:2303 exact, ONE mismatch
normal material/linear/white draw RGB/white parent RGB context. All sampled nearest,
colored-tint/inherited-RGB and flood contexts exact. That does not admit linear
or prove every color/context combination. No engine errors. Failed exit1 correctly
means broad acceptance failed, despite script allowing mismatch reporting.

Separate exhaustive nearest/white-RGB oracle8640 image-byte pairs exact, zero
failures: all180frames of all THREE real sheets drawn together; normal/flood,
three scales, mirrors, opacity.137/1,parent alpha.37/1, ordinary background and
following translucent line.4320 comparisons each normal and existing flood shader
at waterline220/depth.5/clock.7. Other flood states/materials still need coverage.

Memory probe six resource uploads: reported engine increments192675644bytes per
RGBA sheet vs96337822 perLA sheet, exactly half for all three. Images have NO
mipmaps. Initial probe wrongly equated monitor increments with decoded data and
failed6 expectations; corrected observable allocation/ratio probe passes, records
both raw and reported fields. No whole-station memory/loading/FPS claim.

Primary source inspection of matching engine reveals a reporting discrepancy:
[texture initialization](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/storage/texture_storage.cpp)
passes mipmap-count+1 into
[Image's boolean mipmap-size argument](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/core/io/image.h).
For no-mipmap images this requests full-chain estimated bytes; actual upload loops
one level. This explains observed monitor increments; infer accounting overhead,
do not assert physical driver residency or silently relax release memory gates.
Keep existing counter and add separate explicit resource accounting if needed.
No engine change/upgrade.

All owner fingerprints2938unchanged; native jobs terminal, override restored.

## Next action

Build a private native-texture adapter on ORIGINAL DroneAnimation/Grid pipeline,
without palette Group or collection look-ahead. Preserve worker decode, required
loading, frame objects/texture identity and session lifetime; account lazy original
fallback bytes. Initial allow nearest/white inherited/draw RGB, existing flood or
no material; other contexts originalRGBA. Test filter/material transitions,
additional flood states, teardown and loaded-source guards before matched mixed
station timing. Keep full original performance/bug/endurance/PC-Mac gates open.
