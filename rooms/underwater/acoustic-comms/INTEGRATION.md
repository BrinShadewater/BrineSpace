# Acoustic Communications initial integration

Canonical `radio_lab` retains its east/west straight layout, gameplay category,
name, cost, consumption and production. Four source assemblies now render through
the shared hull and south-facing prop system. Plain wall samples omit generated
red socket inserts; an engine-owned dark screen covers the baked waveform.
Local console trace and receiver meters animate when operating. Transducer
canisters and the hydrophone service bench are static.

Station, draft/inspector catalogue and aspect-fit consumers select card v1.
`tools/bake_whole_room_card.gd -- --acoustic --output=<new path>` reproduces it.
The native 512 card and 1600 active station/draft/inspector frame were reviewed.
Stylized headset scale and source floor within enclosed cable loops remain art
tradeoffs. Other generated frames are not implicitly visually approved.

`tests/playtest_acoustic_comms.gd` passes at 1280x720, 1600x900 and 2560x1440:
four rotations, full visible bounds, host-specific motion/offline/pause frames,
non-overlapping footprints, canonical ports, 728 aisle samples and screen-local
effects. Four existing gameplay regression suites also exit zero. Logs under
`output/acoustic-comms/` contain no SCRIPT ERROR/ERROR lines; inherited Image.load
warnings remain. Paired script UIDs and immutable source are retained.

Remaining: real-economy behavior, neighboring boundaries, production walker/depth
review, export coverage, fine silhouette cleanup and owner aesthetic acceptance.

## Economy and connected traversal follow-up

The focused walker sweep includes both ordered directions against the first ten
rooms, Thermal Power Control and itself: 1,472 pairs, 480 compatible and 168,872
production foot-position samples, zero failures. It also checks production
neighbor selection and incompatible boundaries. `output/acoustic-comms/walker.*`
records this collision/path evidence, not sprite occlusion acceptance.

At base rotation and 1600x900, four supplied/depleted/suspended/restored states
and paired frames pass through the actual room economy. Power depletion stops
signal effects; restoration restarts them. No working-cell overrides are used.
The inherited final banner mentions four rotations, but this economy body covers
only base rotation; the separate room fixture covers rotated visual states.
Evidence: `economy.*` and `economy-1600/` under the same output directory.

Both east/west ports at all four rotations pass eight production-walker arrivals
against Battery Array. All 56 sampled frames were visually reviewed in unscaled
100x100 doorway crops at fixed 30% zoom, with clear passage and appropriate door
retraction/closure. `crossings-review.json` records crop bounds and sheet hash;
full frames/index remain in `crossings-1600/`. All runs exit zero without
SCRIPT ERROR/ERROR lines. This does not cover every neighbor material, blocked
neighbor pixels, all prop-depth poses or continuous unsampled animation.

Remaining: export coverage, fine silhouette cleanup, additional depth/blocked
boundary visual review and owner aesthetic acceptance.
