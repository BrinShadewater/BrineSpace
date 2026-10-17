# Cryo ward master and animation polish — September 30, 2026

Installed source revision: two repainted broken human pod masters and one pet
chassis with a separately painted full physical door. Matte ivory/graphite medical
materials, quieter highlights and dark failed inserts retain the selected family.
Door aperture is true alpha. Every pet endpoint uses the same stationary chassis,
door and registration; independent generated whole-pod states no longer morph.

Built-in image_gen source and exact prompt are in `sources/layers.png` and
`sources/layers.prompt.txt`, with hashed references/provenance. V3/V4 preserved.
`build.py` extracts four painted components, fixed human264px/pet160px family
heights, 512px canvases, floor pivot256,448 and standingHeight148. Door frame127px
high moves82px; its entire frame, tabs and runtime glass move together. Latest owner
correction raises it9px more, retaining9/91 glass pixels (~10%) over the chamber top.

`scripts/margot_cryo_art.gd` plays the existing selected Margot poses at unchanged
character density. Runtime composite512×640 retains the same pivot but adds lower
padding so navigation landing never clips Margot's paws at the actor handoff.
Startup0.6–3.8s; physical door3.8–4.8s; small seven-unit hop
4.8–6.6s; colour returns after landing, completing7.8s. Saved eight-second powered
recovery, pause, payment and actual navigation landing point remain authoritative.
25Hz sampled/cached composition replaces12.5Hz; no new character in-between poses
are claimed. Interior vapour remains in the aperture; three translucent painted
clouds surge out and linger at the base, fading by8s. Recovered pod stays open/empty.

Broken master bindings are in `scripts/companions.gd`; all encounter PNG paths are
whole literal paths. Runtime PNG loading keeps these independent of editor imports.
Raster paths covered by Git LFS. `.uid` script companions preserved.

Rebuild: `python character/cryo-ward-layered-v5/build.py`.
Native test: `python character/cryo-ward-layered-v5/run_native.py visual -s tests/playtest_margot_cryo.gd`.
Found-only inspection: same command plus `-- --found-only`.
Recovery regression: runner with `--headless -s tests/test_companions.gd`.
Review packaging: `python character/cryo-ward-layered-v5/package_review.py`.

PASS: four components, true door-hole alpha, fixed-scale endpoint registration;
101 native compositor samples, cat wake rim clearance, full physical travel,
startup, hop/colour timing, pause frame identity, single actor/landing handoff;
companion repair/power/pause/Save-Continue/no-duplication regression. Initial type
inference parse error corrected before successful runs. Agent reviewed master
board, six-phase animation contact, repaired/empty release station views.
Found-room artwork inspection uses the actual unpowered/worn native room pass,
with exterior fog omitted in the fixture; it is not exterior exploration visibility
acceptance. Current exploration fog is deliberately very obscuring. No gameplay
fog balance was changed.

Every Godot run isolates APPDATA/LOCALAPPDATA and fingerprints the real profile;
successful runs report no changed real files (active godot.log excluded). Full
logs/profile records/native screenshots are in output/margot-cryo-landing-v13.
Owner visual acceptance remains separate. No export, commit or upload.
