# Art-pass consistency audit — September 27, 2026

## Repair follow-up

All five findings below addressed on September 27 at owner request. They remain
as the original audit record, not current unresolved findings. Glass now crops
proportionally at a shared scene scale; panel sampling repeats/crops uniformly;
manual floor-cell choices use actual atlas divisions and 24-unit modules. New
sage/bronze/outlet sources are installed non-destructively. Sage mean source
luma changed 0.468 to 0.297; bronze 0.351 to 0.265, preserving distinct hues.
Native checks: 48 selected-tile shape/rotation cases and glass aspect/scale
assertions; four floor runs of 288 views; four outlet orientations. All profiles
unchanged; all four locked launcher hashes match. Updated wall/floor comparisons
and outlet orientations visually reviewed. Owner visual acceptance pending.
See assets/room-risers-expansion-v1/consistency/repairs.json for source hashes.

## Original scope and verdict

Reviewed the current assets from this conversation, not every historical asset in the repository: 44 unique source PNGs comprising 28 expansion room risers, two special north-wall sources, 11 hallway sources (five wall atlases, four floor atlases, detail atlas and ocean-glass source), and three probe machinery sources. The hallway sources provide 12 finishes across 36 shape/finish registrations. Existing windows, doors and three reused hallway furnishings were reviewed in their room context; they are not counted as newly generated sources. Superseded generations and unrelated crew work are excluded.

Overall: coherent enough to keep developing, but not a clean consistency sign-off. The matte industrial construction and muted palette fit the September 26 art bible. The strongest problems are sampling/presentation, not a need to regenerate the collection. This is an audit; production artwork and rendering code were not changed.

## Prioritized findings

1. **Medium — window scenery is distorted in the low opposite wall.** `draw_glazing` fits the full source height (470 pixels) into an 18-unit cutaway. Wide spans exceed the source aspect ratio, so the panorama is compressed vertically; short raised spans crop correctly. Preserve scene scale and crop vertically for the low cutaway, or use a dedicated low glass sample. Keep the owner-requested matching frames. Static painted ocean is intentional; no animated/live exterior has been implemented.

2. **Medium — some wall texture detail stretches with the bay.** `face` maps a fixed panel sample directly into differently proportioned window/sign bays. For example, reinforced panels use a 384×170 sample; its details are stretched differently on long and short bays. Large construction reads well, but fastener and texture density are not strictly uniform. Prefer fixed-scale centres with separately fitted borders. Do not change the authoritative hallway footprint to fit the art.

3. **Medium — manual floor-cell mapping has an inconsistent path.** The ordinary alternate-floor path uses actual 8/6/7 atlas divisions. A cell with an explicit `tile/x/y` assignment bypasses that path, and the fallback still treats alternate atlases as a whole corridor texture in `add_polygon`. It also assumes eight divisions for sage/bronze. This is a code-inspection finding, not a reproduced Studio interaction; add a focused cell-override check before fixing it. Default-floor screenshots do not exercise this case.

4. **Polish — the floor options do not have equal visual weight.** Charcoal rubber is quieter/darker; sage steel is substantially brighter than the current steel; bronze is warmer and its repeated access covers are more conspicuous. Mean encoded RGB luminance of the source textures: steel 0.254, rubber 0.182, sage 0.468, bronze 0.351. These are descriptive source averages, not physical luminance or automatic acceptance thresholds. Their material differences are authorized. If floors should remain equally recessive, reduce sage/bronze contrast in a new candidate rather than globally darkening every material.

5. **Polish — outlet surface detail is denser than surrounding hull art.** The outlet samples 615 pixels across a 48-unit width (~12.81 source pixels/unit), compared with expansion risers around 4.90–5.17. At native display size its speckling and bright edge read more metallic/noisy than the matte wall. This ratio alone is not a pixel-density failure: source oversampling is allowed. Consider a quieter material revision, preserving the short top-down silhouette and buried attachment. The locked launcher remains untouched.

## Family review

| Family | Size / perspective | Art style / colour | Disposition |
|---|---|---|---|
| 28 expansion risers | Shared 400×82 registered face; x sampling 4.90–5.17 px/unit. Current hashes match. Four-orientation sheets reviewed. | Consistent painted frames and department families. Muted Cargo/Cinema/Music/Fitness revisions retained. | Broad visual pass; not owner approval. |
| Diving/airlock north wall | Door/hatch arrangement reviewed in existing native four-view sheet. | Dark steel and restrained hardware match diving equipment. | Broad visual pass; historical capture, not a new gameplay test. |
| Probe north wall and launcher | Integrated north-facing locked study reads connected; old other-direction props are visible in rotation sheets. New mechanics explicitly run only at q0. | Cohesive charcoal/petrol steel; detail denser than general wall panels. | Preserve lock. Do not describe all rotations as the same reanimated assembly. |
| Exterior outlet | Registered 48×42.4, 12-unit buried length; four orientations reviewed. | More speckled/shiny than neighbouring wall. | Material polish candidate; no geometry change proposed. |
| Hallway metal walls | 60-unit raised wall vs 82-unit room riser is intentional narrow-hall geometry, not an accidental mismatch. | Neutral frames and muted sage/clay/slate variants fit the brief. | Keep silhouettes; improve bay sampling. |
| Glass walls | Full-height north glazing, 18-unit opposite cutaway, intentional thin/ribbed/heavy frames. | Ocean softness is appropriate, but stretched cutaway scenery is not. | Correct sampling before lock. |
| Four hallway floors | Actual grids steel/rubber 8×8, sage 6×6, bronze 7×7; all mapped to 24-unit modules. | Distinct materials, matte overall; sage/bronze louder. | Size pass for default path; manual-cell path needs check. |
| Maps/gauges/marine detail panels | Fit independent wall bays at native view. | Match construction; small detail is intentionally simplified. | Broad visual pass. |
| Reused bench/cart/crate and hallway doors | Viewed beside hall walls/floors; no obvious oversizing. Earlier route evidence covers 12 rotations. | Dark-grey doors consistent; light cart and warm bench provide useful contrast. | No new defect identified; no fresh crew-scale or navigation test performed. |

## Pixel density interpretation

The project uses detailed painted sprites, not a mandatory coarse pixel grid. Master resolutions are not required to match. What matters is visible seam/bolt/texture size at the same world scale. Floor source densities are steel/rubber 6.531, sage 8.708, bronze 7.464 pixels/unit, all at 24-unit tile size. Launcher base uses ~13.225 px/unit with selected source bands; it must not be diagnosed as a vertically stretched whole image from its bounding box alone. The cradle uses ~34.19 px/unit. These differing master densities warrant native review, not automatic resampling.

## Verification and limits

- Fresh read-only metadata scan of 44 PNGs; SHA-256, dimensions, alpha extrema, opaque-pixel colour summaries saved in audit.json.
- All 36 corridor registrations' face/cap/low/return/panel/vent rectangles lie within their source images.
- Recorded hashes for 28 expansion and two special-north sources match current files.
- All four accepted launcher lock hashes match, including the mechanics script and animation.
- Reviewed four expansion native sheets (112 historical views), special north four-direction sheet, six launcher motion poses, outlet four-direction sheet, all twelve current hallway finish comparisons, and four same-layout floor captures.
- Existing native geometry checks are evidence from their recorded revisions. No fresh Godot run, motion playback, live crew measurement, alpha-fringe proof, or release validation was performed during this audit. Screenshot sheets do not prove moving fin clearance; the existing accepted lock does not need to be reopened for this review.
- Native comparison PNGs preserve captured pixels without resizing; the webpage may scale them to fit. Historical expansion sheets are labelled as such. Retired assets remain preserved.

Recommended correction order: glass sampling, panel sampling, manual-cell UV mapping, then optional floor/outlet material polish. Preserve the accepted launcher and department colour variety.
