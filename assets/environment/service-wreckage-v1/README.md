# Exterior service wreckage

Current export evidence: `output/environment-export-v5/` verifies all 74 library
PNGs and 50 runtime textures in an isolated Windows debug executable. It captures
all four service groups, including the visually reviewed fallen receiver. Earlier
notes describing its export as pending are superseded by this result. Owner art
approval remains separate.

Five individual decorative assets: collapsed support, torn cable harness,
ruptured pressure tank, detached hatch and collapsed sensor mast. They share oxidized turquoise steel,
localized rust and restrained biofouling with the existing pipe-fragment source.
The original PNGs remain unscaled and unedited by local scripts.

`generation-record.json` preserves four built-in image_gen briefs. Three additional
tank records preserve camera and alpha revisions. Tank v1 was too front-facing;
v2 corrected the camera but painted an opaque checkerboard, and v3 retained that
background. Fresh v4 supplies an overhead transparent sprite. Including the mast,
eight sources are preserved; `manifest.json` selects five and records their hashes.
Requested margins were not honored uniformly, but the selected silhouettes are
complete within their original canvases. Runtime keeps those full canvases.

The renderer adds four authored groups to the existing seabed: a three-piece
broken service frame at (24.5,23.5), a two-piece failed pressure line at (13.5,23.5),
one detached cover at (27.5,14.5), and the fallen receiver at (26.5,21.5).
Canvas widths span 0.24–0.68 room cells.
Group positions are fixed, preserve the previous scatter and habitat layout, and
use no gameplay RNG. No per-sprite rotation changes the lighting or projection.
Source aspect ratio and center pivots remain intact.

These small fragments sit beneath rooms and add no collision, salvage yield or
hazard effects. Normal paid construction can cover them. Room-sized wrecks and
connected basalt blockers retain their authoritative clearance rules. Existing
saved runs see the decorative groups without save-data changes.

## Reproduction and evidence

Run `python tools/audit_environment_pack.py assets/environment/service-wreckage-v1/manifest.json output/service-wreckage-v1/source-audit-new.json`
with a new report filename. The audit verifies expected hashes, visible/transparent
prop pixels and the runtime source map, without rewriting the ledger.
`python tools/build_environment_catalogue.py assets/environment/service-wreckage-v1/manifest.json`
rebuilds the local catalogue after the same checks.

The native fixture is `tests/playtest_service_wreckage.gd`. It isolates player
saves and title settings, captures source colors and all three groups at
1280×720, 1600×900 and 2560×1440, checks actual dimensions and unchanged occupancy,
and exercises paid construction over the broken frame. See `review.json` for
the current results, logs and visual findings. Owner approval and packaged-export
verification are separate from native checkout evidence.

PNG files inherit Git LFS tracking. `addons/brine_raw_export/plugin.gd` includes
the environment directory. Rights remain governed by the repository's NOTICE.md.
# Fallen acoustic receiver addition

The pack now includes a fifth selected asset, `collapsed-sensor-mast-v1.png`,
preserved unchanged with its exact prompt in `sensor-mast-record.json`. A bent
turquoise arm supports a cracked receiver face and attached loose cable. This
small fallen assembly is decorative; it adds no clearance or resource mechanic.

The authored receiver group sits at cell (26.5,21.5), at 0.55 room width. Native
evidence in `output/service-wreckage-mast-native.log` covers five alpha textures,
four groups at three resolutions, unchanged occupancy and normal paid construction
over the existing debris fixture. The receiver's 1600 capture was visually reviewed.
The source audit is `output/service-wreckage-mast-audit-v1.json`. Earlier export
and review evidence below predates this addition; new packaged verification and
owner approval remain pending.
