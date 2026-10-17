# Reusable crew body reference

The owner's proposed families are Bill, Veld, James (Branforth) and Marsh. `base-family-comparison.png` shows their existing four-direction idle sources at one common 2x nearest enlargement. Original heads, colours and equipment are retained so each source model can be identified. This is a reference catalog, not four new character derivatives.

| Family | Source appearance and suggested starting point | Reuse status |
|---|---|---|
| Bill | Broad combat-suit silhouette | Body, recolour, head and equipment reuse demonstrated by Krusher |
| Veld | Slimmer suit silhouette; owner's suggested default for female characters | Proposed family; establish the new character's head and gear fit |
| James / Branforth | Utility suit with more visible tools and work equipment | Proposed family; establish tint masks and whether tools suit the new role |
| Marsh | Android body with pale segmented panels | Proposed family; preserve the chosen mechanical identity and equipment rules |

All source standing profiles declare 184x184, pivot (92,172), standing ruler 148 px. Shared metadata does not prove identical body proportions or head/helmet fitting. Choose by likeness, build and role rather than stretching one family into another. Preserve the existing source pixel density and pose registration.

## Source selection

Human rows use the declared `ACTIVE_ASSETS.json` matte locomotion overrides. Later role/action overrides are separate from these base locomotion references. Marsh resolves idle entries in the actual ordered `marsh-v2/catalog.json` body list, with later matching entries taking precedence; his south idle currently comes from the selected material candidate rather than the older pack. `catalog.json` records the exact manifest/frame paths and hashes, per-direction idle/walk coverage, clocks and opaque body bounds. It should be regenerated when source selections change.

Animation coverage differs among the families. A new derivative inherits its chosen source clocks and gait; a common canvas is not a reason to force every family to one frame count. Additional requested actions must use sources consistent with that family's master.

## Derivative checklist

1. Select a family and preserve its four source facings, registration, gait and holds.
2. Author independent heads at matching density, using neck registration; do not mirror asymmetric hair or features.
3. Build a family-specific suit marking mask and shade the department target by source luminance. Bill's red marking thresholds are not a universal recolouring rule.
4. Fit helmet and equipment using that family's actual face/neck geometry and glove layering.
5. Prove idle, walk and the needed role action at source and display scale before expanding coverage. Retain source hashes and independent technical/visual evidence.

Rebuild from the checkout root with `python character/crew-base-reference-v1/build_catalog.py`, then `validate_catalog.py` in the same folder. This catalog changes no art, runtime selectors or gameplay.
