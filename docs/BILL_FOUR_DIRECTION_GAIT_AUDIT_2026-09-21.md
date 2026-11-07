# Bill four-direction gait audit

Updated September 21, 2026. Broad objective remains active.

## Objective and decisions
Distinguish selected pose defects from clock/turn discontinuity after east/west
integration. Preserve owner layouts and runtime art during investigation.
No generation, Higgsfield, controller change or release export.

## Evidence and current state
Evidence: output/bill-gait-audit-2026-09-21/.
- Current selected four-direction sheet and enlarged vertical foot poses inspected.
- Native audit compares grid and crew-player phase at all 12 directional turns,
  at four cycle fractions each: 48 cases, zero failures. Stationary holds pass.
  This proves clock fraction continuity, not corresponding anatomical pose continuity.
- 54 native samples show all four selected bare/helmet walks over two cycles,
  with moving ground references and actual distance-driven production playback.
- All directions have six poses and 900ms cycles. Side strides represent 92 source
  pixels per cycle; vertical strides remain 0.12 cells. No timing/stride changes.
- South ordering is suspicious: viewer-left boot extent leads in frame0 (171 vs158),
  then switches in frame1 (158 vs171), while frame3 is the opposite contact.
  Extents are image measurements, not inferred anatomical contact coordinates.
  Enlarged poses support reviewing order [0,4,5,3,1,2]: contact/down/passing on
  each leg instead of immediately jumping to the other leg after frame0.
- Order-only south candidate loads original runtime PNGs via a staged manifest.
  Native current/candidate capture: 27 frames, zero missing textures. Same pixels,
  dimensions, cycle duration and stride. This comparison uses static ground ticks;
  it is not a world-space foot-lock demonstration. It is NOT installed.

## Next action
Review south candidate upper/lower-body coordination and loop seam, then select a
reproducible bare/helmet ordering if it improves the whole gait. North has opposite
leg groups but limited within-group motion; inspect before declaring it repaired.
Actual stance sliding and anatomical turn consistency remain open. Do not change
shared playback timing based solely on this source-art finding.
