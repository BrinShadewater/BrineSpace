# BRINE chamber renewal

## Current tank lettering (v6)

At the owner's request, BRINE is now printed on a flush enamel area of the upper
tank collar (source rectangle 555,535,142,34). The overhead sign and supports are
removed. Character, floating, furniture and circulation are unchanged. Current
card: `core-card-v6.png`; native evidence: `output/brine-collar-v6/` and
`output/brine-collar-v6-final.log`. The v5 overhead-sign description below is historical.

## Current room polish (v5)

A supported, dark-metal BRINE nameplate now sits above the tank cap, with pearl
trim and restrained aquamarine lettering. It follows the tank's registration in
every room rotation and participates in visual-bound checks without adding a
floor obstacle. Existing renderer-native drawing supplies the sign, floor mats,
contact shadow and monitor graphics; no generated character art was changed.
Dual monitors now show different traces/bar readouts, and the server has small
powered indicators. Flush workstation mats and a soft tank contact shadow ground
the furniture. The accepted slim face, cap clearance and float remain intact.

Current card: `core-card-v5.png`. Current evidence: `output/brine-polish-v5/` and
`output/brine-polish-v5-final.log`. Native checks include all four rotations,
furniture/nameplate containment, 16 doorway entries and returns with 3,569
movement samples, complete float containment with the old-placement negative
control, pause/offline behavior and three actual viewport widths. Earlier
revision evidence below is retained as history. No new package export is claimed.

## Current face and cap correction (v4)

The owner identified hair reaching into the top cap and requested facial features
closer to the original BRINE portrait. `brine-source-v4-face.png` refines the face
and hair toward that portrait: softer oval features, rose lips, blue eyes and a
center-parted chestnut bob, retaining the slimmer floating figure. The built-in
image-generation edit prompt is `brine-prompt-v4-face.txt`; previous sources remain.
Runtime now uses `brine-float-v4.png` and the native `core-card-v4.png`.

The source-space body rectangle is (521,575,210,210). Its actual alpha silhouette
stays inside glass bounds (555,585,142,190) for the whole float, and the original
top cap is drawn over the occupant as a foreground occluder. The cap no longer
depends on the body being drawn last or on one sampled animation frame.

`output/brine-face-v4-native.log` passes the prior native checks plus 880 silhouette
samples across 88 seconds and a negative control rejecting the old placement.
Highest and lowest native float captures were visually inspected. Updated motion
preview: `output/brine-face-v4/brine-floating.gif`. Current dependency audit passes.
The following describes the previous renewal pass and retained furniture contract.

Owner direction: a slimmer BRINE in the existing crew's pixel-art style, slight
floating inside glass, occasional bubbles, and additional computers without
blocking potential entrances or crew movement. This supersedes the original
empty-perimeter and title-illustration treatment for this room.

## Integrated result

- Slim, short-haired adult BRINE in a matte blue suit, eyes closed, relaxed arms
  and one bent knee. `brine-source-v3-slim.png` is the accepted source for this pass.
  The 92-square runtime sprite preserves a 74-pixel figure height and aspect ratio.
- The existing pearl chamber remains the focal machine. Its rear is drawn first,
  then the cooled body, translucent aquamarine water and glass reflections, and
  finally the source ceramic front lip. BRINE is visually enclosed by the tube.
- Float offsets are bounded to 1.82 world units vertically and 0.44 horizontally,
  with eight- and eleven-second periods. One small bubble rises for 1.8 seconds
  per nine-second interval. Power loss stops these effects; pause holds the clock.
  The glass reflections remain still. No locomotion or role-action pack is implied.
- A dual-monitor workstation, diagnostic desk and server cabinet occupy three
  perimeter activity areas. The existing observation pedestal is repositioned.
  Startup cryopod and all four possible doorways remain supported. Screen traces
  draw inside the monitor glass while powered; equipment remains visible offline.

## Sources and reproducibility

All sources used the built-in image-generation tool; exact prompts are beside
the files. The original title body supplied identity for the first trial, but
that trial retained the illustration proportions and halo and was rejected.
The second trial used Dr. Veld's approved concept as the style/camera reference.
The owner then requested a slimmer figure, producing the third source. Both
earlier trials remain preserved and are not runtime assets.

The computer atlas references the original BRINE room for camera/materials.
Its native canvas is 1536 × 1024 RGB with an opaque checkerboard exterior.
The accepted body source is 1254 × 1254 RGB on white. `build_assets.py` uses the
project's edge-connected light-neutral cleanup, preserving raw sources, and
nearest-neighbor aspect-preserving reduction for the body. It writes RGBA assets
and the authored composition profile. This is deterministic cleanup/registration,
not a generated room bitmap or a new navigation implementation.

`../manifest.json` records current dependencies and hashes while preserving
historical evidence separately. All new runtime files reside under the existing
raw-export `rooms` root. Both station/card mappings use `core-card.png`, baked
through Godot with sealed unused sockets and an empty installed startup pod.
The earlier architect comparison/card remains historical evidence.

## Verification and limits

`tests/test_brine_room_v2.gd` passes in native Godot 4.6.1:
four rotations, all 16 doorway entries and returns using Bill's production mover,
3,569 collision-checked movement samples, bounded bubble frequency, furniture
containment, visible float changes, pause equality and offline tank equality.
The fixture awakens Bill through the normal core recovery entry point and adds
four free test corridors; it is not a paid-economy or multi-crew traffic test.
Tank-only offline comparisons exclude the independently animated walking crew.
Native captures are checked at actual 1280, 1600 and 2560 widths.

Final log: `output/brine-renewal-native-v4.log`, with no ERROR or SCRIPT ERROR.
Room captures and `brine-floating.gif` live in `output/brine-renewal-v2/`.
Agent inspection covered the slim source, native room rotations, glass placement,
screen alignment and card. This does not imply owner aesthetic approval.
The dependency audit passes. Architect recovery, save and crew regression logs
are under `output/brine-v2-test_*.log`.

Earlier native attempts remain diagnostic records: the first encountered an
in-progress shared main-script edit; the second used whole-room offline equality
which included moving crew pixels; the third caught untyped screen coordinates.
The final pass corrects those checks/types. No new exported build was produced;
previous package claims belong to their recorded earlier revisions.
