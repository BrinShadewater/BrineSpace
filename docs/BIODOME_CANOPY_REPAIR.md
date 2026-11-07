# Biodome canopy finishing

Status: one exterior notch and two enclosed tree-canopy gaps repaired and
integrated. Individual packaged Biodome checks pass at all three sizes. Its first
mixed-station tour failed in crew traffic; a subsequent targeted controller repair
passes a fresh tour (see `BATTERY_TRAFFIC_JOIN_REPAIR.md`). Fine margins and owner
review remain.
All walls remain at the accepted low height. No layout, collision, source raster,
effect, room economy or furnishing profile changed.

## Finding and repair

The matched offline contrast renders in `output/biodome-foliage-current-v1`
exposed a pale wedge between the tree's upper central and right leaf clusters.
The source-coordinate crop `(320,180,50,45)` at integer nearest-neighbor zoom 10
confirms donor floor rather than a planter highlight. It is preserved at
`output/biodome-tree-notch-source-v1.png`, with coordinate/hash metadata alongside.

The tree's outer contour now follows that open notch. This does not remove every
enclosed gray gap deeper in the canopy. Nearby leaf shapes and pale planter
construction remain; neither neutral-color removal nor regeneration was used.
The original RGB donor remains unchanged:
`88FEDA3D0E5DABB1C2CBAF70D5A1D0E0ECCBA7982F2265F6073101E5E0C2D070`.

Exterior-notch-only renderer SHA-256 (historical v5):
`7E896B630E8E7DE11084542AFEC6EBFA532FE168ED36EEB0CB52C139C0E8743F`.
Furnishing profile SHA-256:
`1F4ABAC18697F2B70378D7EB25297555667B80C8A2D00D9EDF6BDB08C71AB2A0`.

## Evidence

- `tests/test_biodome_canopy.gd`: three excluded floor samples and four retained
  leaf/rim samples in every quarter. The actual old contour failed all twelve
  background checks (`biodome-canopy-red-v1`, child 1); the repaired contour passes
  (`biodome-canopy-green-v1`, child 0). This is sampled coverage, not complete
  foliage segmentation or image-difference acceptance.
- `output/biodome-canopy-repair-v1`: ten 800-square native offline prop renders.
  Both tree captures changed. All eight fern/aquatic/processor/cart images are
  SHA-identical to their matched baseline. Repaired dark tree close-up reviewed;
  source pixels outside the changed tree region were not exhaustively compared.
- `output/biodome-canopy-native-v1`: 65 PNGs from the native 1600-width fixture,
  including four room crops. Child 0, no engine/script errors. Five assemblies,
  host-local operation/offline/pause, four actual economy cases per rotation,
  containment and 808 socket-route samples pass. All four room crops reviewed.
  This is not autonomous crew traffic or owner visual approval.
- `biodome-card-canopy-v5.png`: fresh 512-square offline card, visually reviewed,
  selected in station/card mappings and the batch-two manifest; prior cards kept.
  SHA-256 `6F0F5C138E6704A1B7593E10B6E72B476034AF7CDCFB707F011BF2D1615A1882`.
  Git attributes report LFS. Batch-two source/card consistency and all ten
  composition dependency checks pass. These are not packaged loading checks.
- Native editor import completes with child 0 and no engine/script errors;
  the new diagnostic/test scripts have generated paired UIDs.

## Pipeline addition

`tools/capture_source_detail.gd` writes a new diagnostic crop and provenance JSON,
not production artwork. Its overwrite and out-of-bounds probes both exit 1 as
intended; the rejected bounds probe creates no output. The positive crop was
visually inspected. The project and installed repair-loop references document
its use. Existing bible guidance already requires preserving leaves and planter
construction, so this technical repair introduces no new aesthetic rule.

## Enclosed-gap follow-up: selected v6

`output/biodome-enclosed-source-v1.png` is the donor crop `(310,205,70,70)`
at integer zoom 8. Two gray gaps above the brown branches contain source floor.
The renderer partitions the tree through both gaps at source y=230, then
subtracts their traced polygons. This keeps the draw pieces free of unsupported
inner rings. It changes only the rendered silhouette, not collision or pivots.
Other small margins have not been exhaustively traced.

The expanded canopy test checks seven excluded floor samples and seven retained
leaf/rim/branch samples across all four quarters. The actual pre-gap renderer
fails sixteen new background checks (`biodome-gaps-red-v1`, child 1). The corrected
renderer passes (`biodome-gaps-green-v1`, child 0). Both runs retain their logs.

`output/biodome-gaps-edges-v1` contains ten matched native diagnostics. The repaired
dark tree and new card were visually reviewed. All eight non-tree images remain
SHA-identical to the v5 comparison. Whole-tree outside-mask pixel equality is not
claimed. Donor raster and furnishing profile hashes above remain unchanged.

Current renderer SHA-256:
`575544C3B3399A8FE090D4D691D666C178A657566F412058F1D717EA64BD9C34`.
Selected card `biodome-card-canopy-v6.png`, 512 square, SHA-256:
`DB9622954895C75B8346AFED6BB77EF8F22B445881965DB2AB6E52A469F1FC6A`.
Both card consumers and the export manifest select v6; v5 remains historical.

### Fresh Windows evidence

`output/batch-two/biodome-canopy-package-v1` contains the exported debug build.
PCK SHA-256:
`1F2747312CE0AF3E832C07220BB591BE297EC5B94B2165B7A9A06BDCC41D4DCD`.
EXE SHA-256:
`8515CD8041A906BDF82A3C9926125E20F642A1062CB2A45A962F3A43DFFA41ED`.

Import, native furnishing preflight (35 catalog IDs, 33 views, 32 profiles,
492 references) and export completed without engine errors. The runtime loaded
20 selected source hashes, 40 raw PNGs, 29 extra component assets and 19 profiles.
Its controlled station tour **failed** at Battery Array `(25,20)` after 17
completed legs, with waiting-for-passage retries exhausted. Runtime child 1;
there is deliberately no successful whole-package verification.json. See the
traffic diagnostic record. Do not use the older Holo tour pass to approve this run.

The same PCK separately passes `biodome-canopy-export-{1280,1600,2560}-v1`.
Each verification.json records child 0, no engine/script errors, input-isolation
exercise and 61 dimension-checked full frames: **183** total at actual 1280x720,
1600x900 and 2560x1440. Four rotations, five assemblies, host-local motion,
offline/pause, four economy cases and 808 socket-route samples pass per fixture.
The 1280 functioning full frame was visually reviewed, including the draft and
inspector art. This does not certify autonomous crew traffic or every pixel.

The export bridge consistency suite initially failed because its expected station
body omitted the generator's necessary `process_frame` access adaptation for Node.
The test now allows that exact context conversion while retaining whole-body
equality; all six checks pass. No source gameplay assertions were changed.

Next: keep remaining art-margin/owner review distinct from the failed mixed tour;
investigate that concrete traffic state without weakening arrival or avoidance.
That investigation now has a recorded-position red/green test and a fresh clean
mixed tour in `BATTERY_TRAFFIC_JOIN_REPAIR.md`. The original failure stays recorded.
