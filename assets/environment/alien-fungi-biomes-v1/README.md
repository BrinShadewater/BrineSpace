# Alien fungi and biome sediments

Five selected assets: fungal shelf colony, spore rosettes, alien sieve pod,
olive kelp sediment and dark fungal sediment. Built-in image_gen sources and
exact prompts are retained. Six masters include the rejected cloudy first
shelf study; five packaged runtime PNGs are registered in manifest.json.

The style is matte detailed painting, strict overhead relief, muted slate,
sage, bone and ochre. Props retain fine texture at measured native scale:
270 physical pixels/cell at .45 zoom in a 1600x900 window. Shelves occupy .38
cell, rosettes .25, pods .22; compare the existing .65-cell mycelium mat in
the native sheet. Source previews in index.html are enlarged specimens.

bake.py checks immutable master hashes, crops transparent margins and resizes
isotropically with LANCZOS. No RGB grading, alpha repaint or thresholding.
Runtime prop widths are 512px; ground rasters are 1024 square. Existing native
tint supplies the submerged appearance. Some source edge flecks remain, with
no conspicuous exterior cloud or fringe observed in the native review.

fungi_biome_view.gd names whole raw-PNG paths and caches saved habitat geometry.
Fungal ground patches in sulfur/iron habitat are drawn through the sub-biome
under-prop hook, then the normal habitat props; low fungi and pods follow.
Kelp sediment replaces kelp-ground through the existing feathered mesh.
Continuous world UVs are retained. Mirrored sheet panels are diagnostics only.
Growth stays clear of the starting anchor, static, decorative and unoccupied.
No simulation RNG, collision, discovery, reward or new save state is added.
The concurrent mineral-habitat-refresh mappings remain selected.

Native source/tint/light/dark sheet and station captures at .25/.45/.65 zoom
were reviewed. Station samples are deliberately positioned near two lit rooms
to establish scale and production fog/lighting; they do not establish visibility
throughout every seeded site. Stable placement, all five raw-PNG loads, selected
kelp pixels, continuous UVs and unchanged occupancy passed. Runtime environment
regression: 93 checks, zero failures. Latest evidence:
output/alien-fungi-checks-20260930-110201. APPDATA/LOCALAPPDATA were scratch;
2,914 non-log owner files remained unchanged. Source audit: five identities,
11 rasters, zero unregistered candidates. Owner visual acceptance and export
remain separate. Broader ocean asset work continues.

See docs/ALIEN_FUNGI_BIOMES_HANDOFF_2026-09-30.md for the next useful scope.
