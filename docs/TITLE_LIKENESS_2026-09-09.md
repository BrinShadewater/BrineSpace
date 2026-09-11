# Starting-screen facial likeness handoff

Updated: September 9, 2026 · Project: BrineSpace · Task: BRINE title likeness

## Objective and acceptance
Owner requested that the starting-screen character look closer to the supplied
download.png cover, correcting facial feature drift. Reference preserved at
brineui/title/likeness-v2/owner-reference.png.

## Accepted decisions and constraints
Use the owner's cover face as the likeness authority for this revision. Preserve
title composition, logo, tank, body, hair silhouette, and independent animation.
Quieter blue-gray eyes and natural nose, mouth and cheek proportions replace the
previous stylized features. This selection is agent-reviewed, awaiting owner taste
feedback; it does not supersede unrelated comms or executable-icon assets.

## Current state
scripts/title_cover.gd now loads brineui/title/likeness-v2/cover.png for the clipped
character. Previous cover, stationary background and silhouette JSON remain intact.
Two imagegen sources, exact prompts, owner reference, composition script, hashes,
and before-after.png are preserved in the versioned asset folder.

## Verification
6,796 changed facial pixels; zero changes outside the original head crop. Original
1925x817 texture dimensions preserved. New PNG is covered by Git LFS attributes.
Native Godot 4.6.1 capture fixture passed with zero failures at 1600x900 and 960x540:
visible New Loop, original texture registration, both float extremes and exact
Reduced Motion freeze. Both native title sizes visually reviewed. Captures and log:
output/title-likeness-v2/. Scoped diff whitespace check passed.

## Next action
Owner aesthetic review. Source installation complete; no executable rebuild or
Butler upload. The maintained release exporter will discover the new static PNG
reference and regenerate the release manifest during the next release.
