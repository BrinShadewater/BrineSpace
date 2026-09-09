# Higher-resolution architect selection portraits

September 8, 2026. The character selector now uses head-and-shoulder regions from
the existing approved concept sheets instead of magnifying a 32x34 gameplay-sprite
crop into the 160x170 portrait slot.

| Character | Source under character/ | Native region (x, y, width, height) |
|---|---|---|
| Major Bill | major-bill-v2/references/approved-concept.png | 252, 136, 256, 272 |
| Dr. Veld | dr-veld-v1/concept-01.png | 246, 134, 256, 272 |
| Chief Engineer Branforth | chief-engineer-branforth-v1/concept-01.png | 248, 144, 256, 272 |

All three source sheets are 1672x941. No artwork was regenerated or upscaled.
scripts/architects.gd owns the regions and caches selection textures;
scripts/architect_selection.gd uses linear filtering for these portrait controls.
Other UI controls retain their existing filtering. Gameplay sprites and the compact
checkpoint portraits retain their existing sources. Locked identities remain hidden.

## Verification

A focused native Godot 4.6.1 check exited 0 with PORTRAIT REVIEW PASS and no reported
engine/script errors. It verified all three selection textures, crop bounds, source
resolution, existing checkpoint portrait loading, browsing without changing the saved
selection, locked selection rejection, and visible confirmation controls.

Agent visual inspection covered captures at 1600x900 and 960x540: all three faces
are identifiable, hair/goggles fit their crops, and the selector layout remains
usable. This is technical and agent visual review, not recorded owner approval.
The current raw-PNG export plugin includes the character directory recursively;
these source sheets are already tracked. An updated exported package was not built
in this pass. Previously frozen package evidence does not cover this change.
