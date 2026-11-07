# Volcanic ash material study

Blocker follow-up: `tests/playtest_volcanic_ash_blockers.gd` places the existing
connected basalt renderer over this patch in an isolated fixture. The run passes
three capture resolutions, cutting-motion and frozen-pixel checks, notch/deeper
clearance and paid rebuilding. The reviewed `interior-cleared.png` shows basalt
faces and exposed edges distinct from the ash; companion rocks remain decorative.
Evidence is in `output/volcanic-ash-blockers-v1/` and its adjacent `.log` file.
This resolves the blocker-contrast check described as pending in older notes below.
No normal-run blocker placement or gameplay balance changed.

Packaged follow-up: `output/environment-export-v6/` verifies the two volcanic
sources as part of 76 library PNGs and 52 runtime textures. The isolated executable
captures the new habitat and its image was reviewed. This supersedes earlier
packaging-pending notes; blocker-specific visibility and owner approval remain open.

Current status: integrated as a fixed decorative patch at cell (14,10), radius
(3,2.5), with three sparse porous-rock placements. The renderer uses the existing
feathered mesh and world sampling. Its two source selections are ledger-audited.
Earlier study notes below preserve the production history.

`tests/playtest_volcanic_ash_station.gd` captures room overlap at 1280/1600/2560,
checks both textures load and confirms unchanged occupancy/resources. Evidence is
`output/volcanic-ash-station-v1.log`; the 1600 group capture was visually reviewed.
Rooms and companion rocks remain readable. Actual clearance-blocker visibility,
packaged export and owner approval are still pending.

One preserved source explores dark charcoal volcanic sediment with small porous
grains. It contrasts with the pale shell shoal and rusty iron seep through material
and value, without lava or active hazard cues. The exact brief and immutable source
hash are recorded beside the image; no source pixels were edited.

Source review: quiet large-scale contrast, overhead projection, small irregular
grit pockets. Native repetition, dark-ground readability under habitat tint,
matching props and station integration remain pending. This is not a certified
seamless tile or an integrated ninth habitat. Prior packaged evidence predates it.

Next review should keep dark blockers and small debris visible against this ground
without brightening the whole material into ordinary grey sand. Review original
and tinted repeated surfaces at the same cell scale used by existing habitats.

## Native comparison

`tests/playtest_volcanic_ash.gd` now produces four panels: ordinary/mirrored
sampling crossed with source/runtime tint. Each repeat spans four cells, with
existing support debris at 0.68 cell and limestone at 0.4 cell. This isolates
sampling from tint, unlike a comparison that changes both simultaneously.

The 1600x900 image `output/volcanic-ash-v1/repetition-and-contrast.png` was reviewed.
Mirroring shows some small symmetric grain motifs but no strong large bands.
Limestone remains visible; the thin turquoise support becomes faint under its
normal tint. Do not infer dark blocker readability from this light stone sample.
Companion props, actual blocker/room overlap and station integration remain pending.
The native log is `output/volcanic-ash-native-v1.log`; its PASS covers loading and
capture, not full visual acceptance. Raw-PNG export warnings remain.

## Porous volcanic rock companion

`porous-rocks-v1.png` adds three unequal low stones with broad grey faces and dark
vesicles. The original transparency and source hash pass the immutable audit in
`output/volcanic-ash-source-audit-v2.json`. The exact brief is preserved separately.

The updated four-panel native preview shows this prop at 0.5 cell width:
`output/volcanic-ash-v1/porous-rock-contrast.png`. It remains distinguishable from
the ash under normal habitat tint through broad surface value, without glow.
`output/volcanic-ash-native-v2.log` records loading/capture success. This is a
decorative rock source, not the room-sized clearance blocker. Live integration,
blocker overlap and packaged verification remain pending.
