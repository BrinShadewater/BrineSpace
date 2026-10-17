# Master consistency check — latest west walk

Reference: owner-approved veld-side-foundation-v1 west master. Candidate:
veld-west-walk-master-v3, all four frames. Review only; no artwork changed.

## Result
Not yet a close enough master match for promotion. Intra-cycle size is much
steadier than the mixed-source attempt, but relative proportions have drifted.

| Area | Finding | Priority |
|---|---|---|
| Head/face proportions | Head/collar band is31-32px versus master27px at comparable standing-derived scale. Enlarged comparison shows a broader/larger face silhouette. This band is a coarse proxy, not a precise skull measurement. | High |
| Face rendering | Warmer/oranger and brighter cheeks/nose, with stronger highlight contrast than the master. Facial rendering reads slightly more exaggerated. Visual judgment, not a calibrated skin-colour measurement. | High |
| Hair | Brown bun and separate silver streak preserved; streak is more prominent across the forehead. Hair/crown silhouette participates in the larger head scale. | Medium |
| Graphite/blue/steel | Material families remain recognisable. Some silver highlights read brighter; no broad palette-family swap. Local painted texture differs. | Medium |
| Equipment | Left scanner retained. Frame3 exposes a larger far-side canister cluster; exposure changes abruptly across frames. Shoulder symbol/patch and small fasteners vary with arm pose and generated detail. | High |
| Body size over cycle | Opaque height147/147/149/149px versus master148px; head/collar band31/31/32/32px. No large half-cycle scale jump. Bounding height can legitimately change with gait. | Improved |
| Gameplay scale | Department, bun and scanner remain readable around45px standing height. Equipment detail variation becomes flicker rather than readable design. | Review needed |

## Evidence and limits
master-all-frames.png compares equal export scale, enlarged face regions and
gameplay scale. measurements.json contains the alpha-bound measurements.
Inspected raw master and raw generated source as well as all exported frames.
This is an appearance audit, not a new foot-plant or native runtime test.
Source and candidate pixels are unchanged; no production selection changed.

## Recommended correction order
1. Match head/face proportions to the master without resizing the whole body.
2. Preserve the master's warm skin shading and less prominent highlight treatment.
3. Hold scanner/canister shapes and attachment positions through the cycle.
4. Add motion in-betweens only after these keyframes match.

Use targeted authored edits; do not treat the drifted walking sheet as a new
identity authority or declare numerical size checks alone an art pass.
