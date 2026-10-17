# Window consistency review

September 27, 2026. Read-only audit of the 14 current window designs and their
existing native room captures. No artwork or runtime bindings changed.

## Verdict
The set belongs to the station visually, but is not yet fully consistent in
detail density or surface finish. Palette and placement are stronger than the
texture treatment. Previous native test passes established loading, fit and
door exclusion; they did not establish style acceptance.

## 1. Detail density — needs refinement
Measured registered window sources contain **17.81–34.75 source pixels per
displayed world unit** in their representative mounts. The sampled room walls
use **4.92–5.59**. Window sources therefore undergo substantially greater
reduction. Examples: compact octagonal steel 34.75, round steel 32.16, dark
green compact 31.09, square frames approximately 18.5–19.6. Corridor density
depends on the available segment; the audit uses representative long mounts.

Both the live renderer and native review select nearest-neighbor filtering.
At native scale, thin retaining rings, tiny bolt highlights and detailed rocks
often resolve into isolated pixels rather than the broader material shading
seen in the wall panels. The octagonal/round steel, twin-port blue and oval
brass designs are especially worth comparing during cleanup. Wide windows
also lose much of the seabed detail once fitted to their shallow mounts.

These numbers measure source sampling, **not an authored pixel-art grid**.
Different source resolutions alone do not make artwork inconsistent. The
native visual evidence is what makes normalization worthwhile. Camera-motion
shimmer has not been tested and is not claimed as a confirmed defect.

Recommended next step: retain masters and produce calibrated render exports
for the actual mounting sizes using one consistent reduction method. Compare
a compact port, a wide window and a center square in native rooms before
rolling that treatment across the set. Avoid stretching or giving every
window the same output dimensions regardless of its displayed size.

## 2. Color — broadly coherent, with localized outliers
- Dark green correction works: the compact, wide and square frames separate
  better from the olive wall panels and remain recognizably green.
- Equivalent top-frame sample patches now read #1d3a2d, #16372b and #1d3729;
  previously #6c7d65, #758c71 and #7c8d75. This is a reasonably close family.
  These are descriptive median swatches, not whole-frame palette definitions
  or formal contrast/accessibility scores.
- Blue frames align with the scientific room equipment; ivory aligns with
  warm cladding. Preserve those departmental differences.
- The oval brass port is the strongest warm/highlight accent. Its trim reads
  more polished and decorative than the surrounding practical matte fittings.
- Ocean panes share a teal family, but their exposure varies: some blue/steel
  panes read brighter cyan, while small round ports become nearly black at
  native size. Do not globally darken the family; tune individual panes only
  where their depth/readability diverges.

## 3. Art style/materials — partially consistent
Shared construction is convincing: recessed gaskets, retaining lips, pressure
fasteners and restrained front-facing depth. Current scale and vertical placement
fit the panels, and the large center windows no longer dominate the riser.

Surface treatment varies too much between variants. The dark-green compact
frame has conspicuous mottled wear; the dark-green wide frame is relatively
smooth; the square is between them. Darkening improved contrast but did not
standardize the material. Brass also has stronger continuous reflective edges.
Several ocean sources use much finer rock texture than the clean, broadly
shaded construction of the accepted props. Glass may be softer than metal,
but should not read as an unrelated photographic image pasted into the frame.

Recommended finish: maintained matte enamel with a few controlled seams and
fasteners; restrained steel edge definition; broad painted seabed depth with
less microtexture. Keep the new dark green, current silhouettes, sizes and mounts.

## Evidence and limits
- `consistency-audit.json` records all 14 source hashes, measured bounds,
  representative sizes, density ratios, wall ratios and green swatches.
- `audit_consistency.py` is a read-only reproducible audit.
- Reviewed current native Galley, Cold Store, Salvage Workshop, Biomass
  Digester and tee captures, plus source artwork already inspected during
  production. These show all window families across their room uses.
- Style authority: `docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md`, its locked
  reference board/catalog, and existing furnished rooms. The bible requires
  detailed hand-painted matte industrial art; a coarse pixel-art conversion
  would be the wrong correction.
- No new Godot run, generation, save access, art edit or package rebuild was
  needed for this audit. Motion, zoom shimmer, all-lighting behavior and owner
  visual acceptance remain unverified.

## Suggested repair order
1. Native detail-density pilot across three shapes.
2. Consistent matte finish on the three green frames; restrain brass glints.
3. Match perceived ocean exposure/detail across small, wide and square panes.
