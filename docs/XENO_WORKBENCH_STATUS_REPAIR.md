# Xeno workbench status strip

Status: integrated with native and three-resolution packaged state/rotation checks;
fresh mixed tour passes. Owner review remains separate. No source raster, geometry, floor, low wall,
furnishing profile, room cost or discovery rule changed.

The workbench's front recessed status strip remained bright when offline.
The existing violet-pixel source filter missed it: its pale, almost-white core
does not satisfy that filter's red-minus-green threshold. It is a visible fitting,
not a reason to remove neutral highlights across all machinery.

## Revision

The source-space lens `(951,929)` to `(999,935)` is re-sampled with uniform RGB
modulation: 0.24 offline and 0.85 operating. This keeps source variation and the
surrounding bezel, without changing blue paint or the existing animated work area.
It adds no blinking. `output/xeno-bench-strip-source-v1.png` preserves a 6x integer
diagnostic of source rectangle `(930,915,90,40)` with source/hash metadata.

Renderer SHA-256:
`BC267B5BFBD4CED6109C1739F64DCF9FE689F04F87A7A68994E793FB91DE187B`.
Unchanged donor SHA-256:
`9A6524C00D9049209DCEF3E3E7FEBA2F8FFB63C14CDE1829E6DF39B1DD622ADA`.
Unchanged furnishing profile SHA-256:
`64DCC35D6DA3E2830C81A9AF16D8FB9B0E384983B755FCC582DAA3EB8E2CA017`.

## Verified scope

- Actual baseline fails eight independent offline pixel samples in four quarters
  (`output/xeno-strip-red-v1`, child 1). The repair passes; the expanded test also
  checks that the strip lights when operating (`xeno-strip-states-v1`, child 0).
  Existing vessel source-coverage and recessed-surface variation checks still pass.
- Matched `xeno-finishing-edges-v1` and `xeno-strip-edges-v1` have ten native
  offline captures each. Eight non-workbench images are SHA-identical. Repaired
  workbench dark-background detail visually reviewed. Whole-workbench outside-mask
  equality and every remaining emitter are not claimed.
- `output/xeno-strip-native-v1`: child 0 with no engine/script errors; 53 full-frame
  state records at requested 1600x900 plus four reviewed room crops. Five assemblies,
  four rotations, host motion/offline/pause, three actual economy states and 404
  socket-route samples pass. All large props remain south-facing.
- New `xeno_lab-card-status-v5.png`, 512 square, visually reviewed and selected in
  station, alternate-variant, card and manifest consumers. SHA-256:
  `9E1090A114D60CBEC6747B7E1450D655BA19FED4767A44CCEB47F41F68DB8D23`.
  Prior organic-v2 is retained. LFS attributes are correct. Batch-two source/card
  agreement and all ten composition dependency checks pass.

The room skill now warns that hue-specific source audits do not establish complete
emission cleanup; pair them with rendered off/on checks. This implements the
bible's existing physical-lens rule, not a new art direction.

## Fresh Windows verification

`output/batch-two/xeno-status-package-v1/verification.json` records a clean
import, furnishing preflight, export and external-directory runtime. The scheduled
tour reaches 30 rooms through 84 reciprocal transitions with 6,352 movement/speed
samples at delta 0.1. Twenty source hashes, 40 raw PNGs, 29 component assets and
19 composition profiles load. Child 0, no engine/script errors.

PCK SHA-256:
`C471C81EA13D92554A496AF69857BAC63D92B8343E8C905097F30BF1A170C640`.
EXE SHA-256:
`8515CD8041A906BDF82A3C9926125E20F642A1062CB2A45A962F3A43DFFA41ED`.
Controller SHA-256:
`46757B6F6E6AEA6C370477CCACA46B792A176DA396406B8DA3ED3A595158F62B`.

The same PCK passes `xeno-status-export-{1280,1600,2560}-v1`: 53 full frames
per size, **159 total**, with actual PNG dimensions checked against 1280x720,
1600x900 and 2560x1440. Each verification.json records child 0, no engine/script
errors and the Escape/W/Space input-isolation exercise. Four rotations,
host-local motion/offline/pause, three economy states and 404 socket-route samples
pass per fixture. The 1280 powered full frame was visually reviewed, including
station, draft and inspector consumers. This does not approve every pixel.

The native flattened-material negative control still exits 1, with 24 flattened
surface failures and no script errors (`xeno-strip-flat-negative-v1`). All six
export bridge consistency tests and ten-profile dependency checks pass.

This is scheduled traversal, not autonomous destination selection, population-scale
crowd liveness or all 35 catalog identities. Further source-edge and owner review
remain separate from the verified status-light repair.
