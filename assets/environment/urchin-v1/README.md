# Short-spine urchin

Current status: integrated as three static organisms on pale shell shoal near
cell (9.8, 16.6), at 0.25, 0.25 and 0.20 cell canvas widths. The terrain study
shows clearer silhouettes on pale sediment than on ash; placement is limited
to the pale habitat. Native station checks pass at 1280, 1600 and 2560 widths
with unchanged occupancy and resources. The 1600 capture was visually reviewed.
Evidence: output/urchin-terrain-v1.log and output/urchin-station-v1.log.
Packaged verification passed in output/environment-export-v12, including the
dedicated captures/life-urchin.png, which was visually reviewed. The build
verified 81 exact environment PNGs across thirteen packs and 56 runtime textures.
V11 remains failed evidence: it captured an intermediate renderer signature
mismatch during concurrent edits. Owner approval remains pending.

One original 1254 × 1254 RGBA source generated with the built-in image tool.
The exact brief is in generation-record.json and the immutable SHA256 is in
manifest.json. No image processing was applied.

The muted plum body and stout pale-tipped spines form a compact silhouette
distinct from seagrass and ribbon kelp. Native scale review compared source
colors and the existing plant tint at 0.15, 0.20 and 0.25 room-cell canvas widths.
At the smallest size it reads as a dark speck; the terrain trial selected
0.20–0.25 for pale-shoal placement. Transparent margins mean canvas width is
not body diameter.

Evidence: output/urchin-source-audit-v1.json and output/urchin-native-v1.log;
the 1600 × 900 capture is output/urchin-v1/organism-scale.png. True empty exterior
pixels are verified. All nonempty pixels have partial alpha; the subsequent
textured-terrain review established sufficient contrast on pale shoal.

It adds no moving fauna, collision, harvesting or hazard behavior.
Owner art approval remains pending.
