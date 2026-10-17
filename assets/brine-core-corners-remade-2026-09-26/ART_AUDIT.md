# BRINE Core remake audit — 2026-09-26

## Conclusion
Not ready to replace the originals. Color is too dark/warm, the pair's shape and export density differ, and the saved north-door placement has too little lateral margin. Artwork and owner layouts were not changed by this audit.

## Color and art style
Visual comparison against the original core corners and room card confirms warm gray/beige drift, strongest on NE. Masked pale, low-saturation pixels have median RGB NW 208/200/192 versus original 225/221/215; NE 192/186/174 versus 223/218/212. This threshold-based comparison supports the visual finding but is not a semantic color calibration. Target the original pearl-white coating; do not globally brighten teal glass, seals and shadows. Bevels, screen outlines and cylinders remain harder/shinier than the accepted painted cabinet reference. Reduce those local highlights and uniform dark borders; keep useful seams and broad diffuse shading.

## Density and size
Exports: NW content 376x343, canvas 384x351; NE content 360x350, canvas 368x358. Equal maximum-box export does not give equal world density. At the owner's q0 sizes, visible width density is approximately 2.53 px/world unit NW and 2.40 NE: about 5.5% difference. Use shared world density when rebuilding exports, rather than normalizing each independently to a bounding box. Actual crew usability remains untested.

Retaining current registered widths and owner scales gives NW 148.65x135.60 and NE 150.16x145.99 world units for candidate content. Original registered extents are 148.65x136.87 and 150.16x139.32 respectively. NE therefore extends about 6.67 units farther down the side wall at the same width. Do not stretch the bitmap to correct this; correct the geometry or choose a proportionate size within a reviewed placement.

## Door approaches
audit-results.json records merged defaults and owner saved positions for all four rotations. The candidate scenario reuses old collision fractions provisionally, not a new registration. In q0, NW has only 4 units of horizontal gap to the 72-unit north lane; NE has zero. Adding a conservative 10-unit lateral margin exposes deficits of 6 and 10 units respectively. Both old and candidate corner boxes leave the north door's exact navigation node clear, so this is a tight approach/visual margin issue, not evidence of a blocked door. Side-lane gaps are 20.40 NW and 10.01 NE before padding; NE leaves essentially no surplus after 10 units.

Recommended remake envelope: keep the exterior wall-contact edges fixed and shorten the north runs inward ends to x<=-46 on NW and x>=46 on NE. Preserve useful control/module size by simplifying or redistributing modules instead of shrinking every detail. Shorten the NE return to the original depth, with a little extra margin if feasible. These are proposed corrections, not edits to owner layout data. Final registration, native door/circulation check and visual room review remain required.

## Evidence
audit.py is reproducible and read-only for owner data. Its JSON records approximate masked color statistics, all placement scenarios and provisional door-node calculations. The existing generic counter clearance checks are not applicable to these registered core corners. Original assets and candidate masters are preserved.
