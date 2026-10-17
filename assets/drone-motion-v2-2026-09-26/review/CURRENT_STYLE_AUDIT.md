# Current drone visual audit — 2026-09-26

Scope: eight travel poses, cardinal work comparison and job transition board,
against accepted v10 identity and the visual bible. No source/frame edits or
runtime integration. This is agent review, not owner acceptance.

## Findings

- Perspective: recognizable overhead view throughout. East/west chassis read
  flatter and shallower than the diagonals; southeast shows substantially more
  front housing. Some foreshortening is expected, but chassis depth/top-plane
  consistency deserves a focused reference-led pass. No numeric camera angle
  is specified by the bible; do not invent one.
- Sizing: both arms and large casings remain readable. East/west silhouette widths
  are 175/174 export pixels; north/south 206/202. These are whole silhouettes,
  including articulated tools and propellers, not chassis measurements or proof
  of a size mismatch. NW now has the requested inward tool bend. Its short
  apparent tool length should be judged with foreshortening, not bbox normalization.
- Style: muted cyan/steel and mechanical identity agree with accepted v10.
  Strong black contours, bright casing edge highlights and smoother broad panels
  remain closer to the accepted drone than the more textured locked machinery.
  Refinement should soften material contrast and add restrained painted variation
  while retaining the owner's accepted silhouette. Do not blanket recolor cyan.
- Density: all eight pose canvases are 256x256 and manifest scale is 0.34 world
  units per library pixel (2.941 pixels/unit). This establishes sampling scale,
  not identical authored detail density. At the 0.34 review inset, bolts and jaw
  details merge, while body, tool and propellers remain identifiable. East/west
  and NW broad panels read smoother than south. No coarse pixel-art conversion
  is appropriate for this bible.
- Physical size: nominalSouthHullWidthWorld=69.12 remains provisional. The
  south opaque silhouette measures 202px (~68.68 units at alpha >64), showing
  that the nominal label must not be treated as a measured chassis-only width.
  Current-pack crew/room scale, clearance and gameplay zoom need a native scene
  review before physical size acceptance.

## Evidence and checks

New light/dark boards use actual export pixels, no individual bbox fitting;
small insets approximate 0.34 scale. Locked pump and valve exports are shown
at native library size, not equal physical size. Both locked SHA-256 hashes
match. Accepted v10 is explicitly normalized to 203px only for identity review.
Measurements are saved in current-style-metrics.json. Inspected the light board,
existing size-pass.png, job-transitions.png and earlier bible comparison.
No animation or gameplay tests rerun: only audit script/report/boards were added.

## Handoff

Changed: audit_current_style.py; review/current-style-audit-{light,dark}.png;
review/current-style-metrics.json; this report.
Remaining: focused camera/material consistency pass if pursued, followed by
current-pack native crew/room scale review. Existing animation behavior preserved.
