# Navigation UI asset and integration lessons

Owner direction, September 8: dark petrol teal plates and gunmetal borders;
clean satin enamel icons with little distressing. Codex computer is aged cream,
Archive ochre, Diagnostics jade, Journal autumn orange, Menu blue/ochre/jade.
This is UI-specific, not a universal room-material rule. Preserve some color
without neon, bloom or excessively bright highlights.

## Asset pipeline
Retain raw generations, exact prompts and versioned candidates. Inspect actual
RGB/RGBA channels: a checkerboard drawing is not transparency. Repeated image
edits can retain it and alter accepted colors; do not keep regenerating solely
because a transparency prompt failed. Use the authorized tools for cleanup.
For these convex badge plates, runtime octagonal UV clipping excludes the
exterior while preserving source files. This is a rendering solution, not an
alpha export; source revisions require rechecking each silhouette's coordinates.
Do not use this shortcut for irregular props or internal transparent holes.

## UI workflow
Keep native Button actions, keyboard focus, shortcuts and accessible labels.
Render text and counts at runtime. Place Archive, Diagnostics, Journal and Menu
in that order in one top-right row, with badges above compact labels. Archive
stays visible at zero unread records. Top resonance and cycle displays are removed;
their gameplay mechanics are not retired by this visual change.
Review final dynamic labels after refresh, not only constructor text. Capture
1600x900 and960x540 and inspect clipping, text overlap and resource-bar space.
Check changed signals and row order. Record unexercised controls honestly;
native screenshot acceptance does not imply an exported build passed.

Current implementation/evidence: scripts/navigation_badge.gd,
tests/test_navigation_badges.gd, docs/NAVIGATION_BADGES_2026-09-08.md.
Never serialize image-generation data URLs into text logs; use generatedImage
for display and retain only paths/metadata/prompts in tool text.
