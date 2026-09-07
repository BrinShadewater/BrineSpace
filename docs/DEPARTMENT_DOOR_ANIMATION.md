# Department door animation — front-view motion study

## Integrated follow-up

### Accepted low side silhouette — animation integrated

The owner accepted the v6 open silhouette. The normal renderer now uses it with
two recessed panels that retract completely at frame 9. The 72-unit opening,
16-unit wall-end footprints, low 3-unit cutaway and existing crossing timing remain
fixed. Posts reuse the very same `nursery-master.png` cap crop as the current
shared room shell, with department trim and independently dimmed white lamps.
Generic keeps neutral trim rather than recolouring the surrounding wall finish.
Front geometry/source regions remain unchanged. Cards still show sealed sockets.

Current pack: `output/door-redesign/animation-v8/` (80 frames, manifest, atlas,
cycle GIF and sampled native crossing GIF). Side surfaces are deterministic
construction, not new generated directional sprites. The native renderer remains
layered for character sorting. Export now preserves paint order at equal depth;
older flattened exports could shuffle cap components despite correct runtime order.
Native evidence: `output/door-redesign/side-v7-final/`; 88 crossing poses pass,
including opposite travel, four rotations, power and pause. Earlier v7 test failure
was a misplaced test-loop indentation; corrected evidence is preserved separately.
The legacy `--side-open-prototype` flag is still a fixture-only open override.

### Open side-door prototype (v6, awaiting owner review)

The owner rejected v5's side construction: the tall projected posts and narrow
overhead rail still read as machinery across the passage. A review-only alternative
now uses the room shell's actual 3-unit top lift / 4-unit fascia, 16-unit wall-end
caps, a floor-level metal threshold and no overhead rail. Caps, fascia and lamps
are separate depth-sorted pieces; the threshold/track is always behind crew.
Simple code-drawn materials establish the silhouette, not finished generated art.

Run `tests/playtest_animated_door.gd` with a fresh `--capture-dir` and
`--side-open-prototype` to enable it. Normal runs retain the existing animation;
front-facing doors are unchanged even in this fixture. This flag holds side doors
visually open and must not be used to certify closed/moving side-door states.

Evidence: `output/door-redesign/side-open-v6/`, including both horizontal crossing
directions at midpoint. Native capture suite passes (88 poses, four rotations,
power/pause); no script errors. The next stage, only after visual acceptance, is
to refine the cap finish and build recessed leaves using this lower cutaway.

Visual follow-up (animation-v5): equal bounds alone did not fix the join. The
side posts still sampled opposite angled corners of the front arch. Both now
use the same flat top-cap material and separate straight jamb faces; the narrow
rail terminates exactly at those caps. The original generated source is unchanged.
This remains a source-material cutaway, not newly authored directional artwork.
Native crossing evidence is in `output/door-redesign/side-caps-v5/`; visual
acceptance is still required. The current exporter targets `animation-v5`.

Side-registration correction: both posts now derive from identical 16-unit ground
depth and 42-unit elevation, matching the geometry module's wall/socket caps.
The earlier hand-tuned north post was 51 units high versus the south post's 57,
and their nominal 15-unit ground depth did not match the 16-unit caps. Current
post projections are (-8,-94,16,58) and (-8,-6,16,58); rail endpoints derive from
the same aperture/elevation constants. Opening width and motion timing are unchanged.
The earlier animation-v3 sheet/GIF is historical, not the corrected runtime export.

The front-only study below is preserved history. The replacement now runs through
`rooms/doors/department_door.gd` on every connection involving a layered room.
The original atlas remains untouched as fallback; legacy-only connections retain
their old renderer. Unconnected sockets still use wall infill, including cards.

Four finishes are available: Bio, Life Support, Engineering and neutral grey.
Same-department pairs use their department finish. Mixed/unknown pairs use generic,
independent of edge ownership or room placement order. Generic desaturates the
approved Life Support material in a cached shader; it is not a fourth art generation.

Side geometry is explicitly registered: upright end posts, a narrow far-side rail
with a deliberate camera cutaway, translating leaves and a flat metal threshold.
It uses approved source surfaces, not a rotated bitmap or independently generated
side sprite. This is a readability-oriented cutaway, not a complete physical model.
Its visual acceptance remains with the owner.

White lenses are extracted to an emission layer via registered source regions.
The non-emissive paint layer has dark lenses. Both layers share registration and
depth. Shared-door emission uses the lower adjacent room light level; it fades and
pauses with existing room lighting, without introducing power-dependent access.
This conservative shared-fixture rule does not simulate cross-door light spill.

Final pack: `output/door-redesign/animation-v3/`: 80 transparent frames, 32 playback
states, eight unlit open views, three material layers, atlas, contact sheet, manifest
and GIF. Fixed frames are 256 × 320, pivot (128,200), two pixels/world unit. Closing
reverses opening; engine timing remains the existing crossing timing. Native export
script: `tools/bake_department_doors_v2.gd`; preview/QA:
`tools/preview_department_doors_v2.py`. Earlier exports are preserved.

Verification: sprite manifest has no errors/warnings. Pixel checks confirm generic
greyscale, unchanged alpha across power states and clear front opening. Side alpha
is intentionally opaque at its floor tread, so native part checks verify leaf
absence instead. `integration-final.log` covers 88 crossing poses and four finish
geometry registrations; `station-final.log` covers four rotations, 1616 route
samples, mixed legacy rooms, power fades and pause. Four gameplay regression suites
pass. Evidence is under `output/door-redesign/`. No player save migration or gameplay
balance changes were made.

## Preserved initial study

Created from the approved generated concept board, not a regenerated frame row.
Source provenance and exact built-in generation prompt are in
`DOOR_REDESIGN_STUDY.json`. Native source: 1536 × 1024. Original board is preserved.

Run `tools/bake_department_doors.gd` with Godot, then
`tools/preview_department_doors.py` with Pillow. Both refuse to overwrite evidence.
Outputs: `output/door-redesign/animation-v1/`.

Each of Bio, Life Support and Engineering has 10 opening frames. Closing reverses
those frames; closed/open are endpoint holds. Exported frame size is 256 × 192,
ground pivot (128,144), 2 pixels/world unit, clear aperture 72 world units. Playback
metadata uses 18 fps; the GIF adds holds for inspection. Final game access timing
has not changed. Source panels translate rigidly and clip into fixed pockets;
their texture is not squeezed as the opening changes.

The pack contains 30 individual transparent PNGs, a 10-column/3-row atlas,
12 named state entries in a manifest, nine separate frame/threshold/leaf layers,
a contact sheet and a looping three-finish GIF. No mirroring is used.

Geometry checks verify fully open alpha over the passage and fixed header pixels.
The sprite skill validator reports no errors or warnings. Native atlas review
shows consistent silhouettes and paint, with a shallow metal tread instead of the
concept's deep recess. Surface strips were registered non-uniformly to a shallow
front elevation; this is an explicit dimensional adaptation of concept art.

Remaining: authored side-facing projection, independent emissive masks (white
lenses remain in the source artwork), room/character depth review and consumer
integration. The existing game door renderer and player saves are untouched.
This is a complete front opening/closing cycle, not a certified all-direction
station replacement. Keep that distinction in handoff and future tests.
