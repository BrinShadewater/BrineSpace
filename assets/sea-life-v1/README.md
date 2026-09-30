# BrineSpace sea life — installed first batch

September 29, 2026. Owner approved continuing from the first-pass direction.
All five species are installed in scripts/ocean_life.gd with procedural fallback.
Placement, epochs, fade, culling, encounter periods and quality counts are retained.
Glass Choir and Veil Kite occupy existing drifter slots, adding no encounters.

Twelve PNGs cover lantern body/core, ribbon body/head, tidewalker body/fin/sail/
lights, Glass Choir body/core and Veil Kite body/core. The manifest records grids,
pivots, fps, hashes, transformations and all 26 lights. Whole resource paths load
through SafeImage.raw_texture with dimension validation. Invalid art warns once per
file and retains the procedural renderer.

Exact built-in imagegen prompts and seven immutable sources are preserved.
Matte-v2 tidewalker removes the original baked dot chains. Small-creature loops
derive from one registered pose with periodic deformation; white glints follow
the same deformation. Additional species use static tissue atlases with runtime
rotation/banking. All animation uses the existing visual clock and freezes paused.

The current bible governs painted finish; Claude's handoff governs fauna anatomy.
The 1600x420 leviathan retains source aspect and detail. Its active painted width
is 1233 pixels over 13 cells: about 4.05 world units per art pixel. This large
distant silhouette has a documented density exception to the small-creature
approximately 1:1 target; upscaling would not manufacture more source detail.

Rebuild: python assets/sea-life-v1/bake.py
Packaging checks: python assets/sea-life-v1/validate.py
Isolated Godot gates/captures: python tools/check_sea_life_assets.py
Native review summaries: python assets/sea-life-v1/review/build_review.py
Full before/after game captures: python tools/check_sea_life_assets.py test_sea_life_review
The bake overwrites only derived pack files; immutable sources remain intact.
Native windows use screen 2; each test gets fresh scratch APPDATA/LOCALAPPDATA.

review/index.html provides atlas playback. review/native-review.jpg shows the
in-game family. Before/after and sampled motion PNGs are in review/native; three
native GIFs sit alongside the summary. The complete tidewalker overview uses a
lightweight native assembly fixture; gameplay close-ups are preserved separately.

Packaging passes 131 checks. Godot asset, quality, reliability and native ocean-life
gates pass; earlier owner-profile fingerprints were unchanged. A later full-game
capture retry timed out during startup while live-profile fingerprints changed
during concurrent activity. The assembly renderer passed separately; late profile
acceptance is inconclusive. See HANDOFF.md for exact evidence. Final owner motion
acceptance remains separate from first-pass continuation approval. The release
dependency manifest selects twelve PNGs and excludes source/review art. No playable
executable or PCK was exported.

Batch 2 lighting is next, followed by cards, screen maps and hazard/build sprites,
with the handoff's review checkpoints between batches.
