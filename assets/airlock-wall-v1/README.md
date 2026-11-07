# Project handoff - Diving Airlock wall bank

Updated: 2026-09-08. Project: BrineSpace.

## Objective and acceptance

Create a reusable Diving Airlock suit-and-tank wall asset, keep proportions modest
and materials matte, and feed concrete corrections into the ongoing art workflow.
This is standalone asset production; placement and directional integration remain
a separate stage. Agent visual review does not imply owner aesthetic acceptance.

## Accepted decisions and constraints

The owner's repeated shine correction governs future art. Preserve Engineering
charcoal/slate, olive fabric, rubber and small ochre handling accents. Continuous
length comes from two suit bays, a fitting bench, three cylinders and a hose rack.
Keep current low hull, north pressure chamber and south station doorway. The
horizontal front view must not be rotated or squeezed into a side-wall substitute.

## Current state

`suit-air-bank.png` is the true-alpha 1994x789 export. V2 is selected; V1 is retained
as a material rejection (cylinder and helmet reflections). Both raw RGB sources
are unchanged. `prompts.json` contains the exact built-in imagegen generation and
targeted edit prompts; `brief.md` gives reference roles and scale intent.
`suit-air-bank.json` registers source UV polygons using neutral threshold 160.
The backed recesses need no enclosed background-hole seeds.

`manifest.json` records hashes, dimensions and selection. The completed
`material-scale-review.json` distinguishes materials, scale, alpha and integration.
The live Airlock, its card and gameplay are unchanged by this asset task.

## Verification

`tools/review_registered_wall_asset.gd` and its UID provide a reusable native
export/scale-board workflow. Run Godot graphically with this script, followed by:

```text
-- --registration=res://assets/airlock-wall-v1/suit-air-bank.json --export=res://assets/airlock-wall-v1/suit-air-bank.png --review=res://output/airlock-wall-v1/material-scale.png --reference-view=res://rooms/underwater/airlock-v1/airlock_view.gd --width=320
```

Final native pass: `output/airlock-wall-material-v2-final.log`. Full export and
1040x900 board visually inspected; proposed sprite width 320, visible height about
100.55 world units. The existing room renders separately at the same world scale.
Light/dark ground checks and exterior/opaque alpha samples pass. The initial board
cropped the enlarged base; final height fixes that. Source-overwrite negative
control exits 1 with unchanged source hash (`output/airlock-wall-source-guard.log`).
PNG LFS attributes pass. No room-route or package acceptance is claimed.

The maintained skill, art-direction reference, new material/scale review and JSON
template now encode explicit rejection gates. The visual bible records the owner
direction. Changed skill files were synced to the installed snapshot; 17 files
compare without differences. The V1 failure and V2 correction are recorded as a
bounded lesson, not a guarantee that future generation will match automatically.

## Next action

For room installation, author inward-facing side views or a split layout around
the pressure chamber, preserving helmet-fitting access and existing interlock
behavior. Then verify all supported orientations, actual routes and refreshed card.
Apply further owner material feedback to versioned sources before installation.
