# Reactor registered-prop edge review

## Decision

Retain the current six prop cutouts. The reviewed offline captures do not show
a definite new background-contamination defect requiring repair. This is a
focused edge review, not full-room, animation, rotation or release acceptance.
No source art, registration, wall height, card or gameplay code changed.

`output/reactor-current-edge-review-v1/edge-review.json` records twelve native
800x800 PNGs: six props against dark purple and light beige, at four pixels per
world unit. All twelve were visually inspected across the review. The retained
log reaches `PROP EDGE CAPTURES: 12`; stderr has raw-image loading warnings, but
no engine/script errors. These editor-side renders do not prove packaged loading.

## Observations

- Chamber: retain the steel rim, amber glass and physical base. No decisive
  stray floor patch was identified along its outer silhouette.
- Console: retain the screen housing, feet and orange material accents. Their
  colour alone does not establish baked emission; offline/on testing is separate.
- Service table: the space between its legs exposes both diagnostic backgrounds;
  the tabletop, supported tools and hanging cloth remain intact.
- Service cylinder: the handle and looping hose expose the backgrounds through
  their openings without an obvious opaque source-floor fill.
- Task lamp: the arm, stem and base loop remain separated from the background.
  Its pale diffuser alone does not prove a missing power-state response.
- Cooler: the narrow return-pipe gap exposes both backgrounds. The darker lower
  backing is deliberately retained, for the source-based reason below.

## Cooler backing resolved from source

`output/reactor-cooler-backing-detail-v1.png` is a read-only nearest-neighbour
detail from source rectangle `[315,140,85,220]`, enlarged exactly 3x to 255x660.
It visibly shows a raised mounting platform with a beveled outer edge and front
face beneath the pipe, distinct from the surrounding tiled floor. Removing the
whole dark region would remove hardware, not merely clean a cutout.

The renderer's existing excluded gap remains `[335,182,7,98]`; this review does
not enlarge it. Source detail metadata is in the adjacent `.png.json` file.

## Revisions and limits

The capture's recorded renderer hash matches the current renderer at review:
`397846F36646F8C66AFFACF3C7B3295101D2AB2F7EF0A4069C565CC68D8D7178`.

The source detail records Reactor source SHA-256:
`487794FA86F762E5DCDB6AE93B1D1FE3CB29EE5CFAD7144E7F44F128111CE7DE`.

Additional hashes inspected at review time, **not captured transitively by the
edge helper**, are:

- `reactor-composition-v2.json`:
  `E84A1899469679B8FDB90269FB7A34E6A6A918A794CE08D866CE16401819AF95`.
- `maintenance-support-v1.png`:
  `4FAAA6D321768BBE61218E3881F9AF1083464C4EC06BE9EDF14895AD36E6F89F`.

The helper records its direct view and output hashes, not every inherited script,
profile or reused atlas. Do not treat it as a complete dependency snapshot.

Independent Reactor-host pause/motion, actual gameplay-scale effects and broader
crew overlap remain follow-up work. Historical package results in
[Reactor steel export v17](REACTOR_STEEL_EXPORT_V17.md) retain their original scope.
The existing repair-loop rule to distinguish hardware/platforms from unwanted
background already covers this finding; no new bible aesthetic is inferred.
