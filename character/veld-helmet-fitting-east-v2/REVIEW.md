# Veld canonical fitting rebuild — 2026-09-29

## Accepted and installed — 2026-09-29

Owner accepted muted-shell-v3 and asked to continue. Sixteen fitting/removal
frames now load through a Veld-only body override; 72 equipped east idle frames
use a separate matching-tone override. Original shared idle assets retained.
Actual loader/native fixture: 138 checks, zero failures. Both grounded idle joins,
all selected pixels, durations, pivots and reverse sequence verified; native.png
reviewed at source/gameplay sizes. Scratch APPDATA asserted; 2,730 real profile
files fingerprinted, zero changes. No release export. Other east equipped states
retain their prior shell grade; their action interiors remain audit backlog.

## Helmet-tone follow-up — muted-shell-v3

Owner approved the arm revision otherwise and requested a darker helmet. Shell
and trim receive the same 0.82 RGB multiplier in carried and fitted poses; face,
visor aperture and white lamp are protected with a one-pixel mask margin. Alpha,
body, arms and timing are preserved. Builder and 16-frame palette/edge checks
pass; updated head strip visually inspected. Prior arm-joints builder/contact and
versioned GIFs retained. Current endpoint is the locally toned selected equipped
idle. Its installed source remains untouched: installation must carry this tone
into the equipped idle join. Candidate remains staged for visual review.

## Arm-joint follow-up — arm-joints-v2

Owner liked the overall canonical appearance but reported arms bugging out during
fitting. Diagnosis: broad extrapolated badge rectangles overwrote bent forearm
pixels; pose5 extraction clipped the elbow; pose6 combined a lowering near arm
and adjusting far hand into one invented connection. Idle far-hand pixels also
remained under the raised pose. Repair confines badge replacement to its actual
blue footprint/filled emblem holes with one-pixel edge dilation; widens pose5's
hand-to-elbow mask; retains pose4's raised far arm and clears the idle far glove.
Pose6 now keeps the entire selected lowered near arm and overlays only the far
adjusting hand/forearm. Sleeve palette frozen from the prior revision. No new
generation, face/helmet redesign or timing changes. Prior builder/contact and
versioned GIFs preserved. Builder passes prior16-frame checks plus exact pose6
near-arm pixels. Contact/head and82px dark/light frames inspected; visual/native
acceptance and installation remain pending.

## Objective and acceptance

Resolve fitting/removal drift identified in the whole-library comparison. Current
candidate: muted-shell-v3. Staged visual review; not installed or owner accepted.

## Accepted decisions and constraints

Use the selected east bare/equipped idle identity and shared helmet. Preserve
timing, eight poses, stationary stance and linear sampling. Prior fitting versions
remain in veld-helmet-fitting-east-v1 for rollback. Retained special-action backlog
identified by the audit is separate from this fitting rebuild.

## Current state

build.py reconstructs the sequence from the actual accepted idle pixels. Bare face,
hair and collar remain fixed until shell occlusion. Fitted face/head come directly
from the selected equipped idle. Torso fittings, canisters, legs and boots remain
canonical; rows139–207 are exact in every PNG. Moving arms are isolated from the
preserved v13 staging under explicit polygons; one accepted-sleeve palette curve
applies across all arm layers. The actual science badge is perspective-mapped over
the generated emblem. Two imagegen edits are preserved with prompts: an empty
helmet aperture and a body underlay. Only the aperture RGB from the helmet edit
is used; original shell RGB and alpha are retained outside it. Only a small formerly
occluded torso-side fill from the body edit is used. Generated head/body pixels are
never substituted wholesale. Full raw sources and old pose-staging PNGs retained.

GIF previews use one shared 256-color palette for fitting and removal, no dithering
or per-frame adaptive palettes. This prevents encoding from changing identical
stationary pixels. Manifest remains184x208, pivot92,196, standing148.

## Verification

Builder passes: eight fitting/eight reversed removal PNGs, original timing
cardinality, exact idle endpoints, exact lower body, exact bare heads in first
three interior poses, exact equipped crown, no boundary clipping, all16 decoded
GIF exterior checks and exact stationary decoded GIF RGB rows. Head/contact
comparisons and all eight poses at82px on dark/light backgrounds inspected.
All2,932 selected frame references match the audit hashes (selected-assets-check.json).
No runtime bindings, other actors or player saves changed. Native integration and
owner motion/visual acceptance remain pending; this is an image-pack revision.

## Next action

Review the new fitting/removal playback for shoulder attachment, arm/collar
occlusion and carried-to-fitted helmet movement. Install only after visual
acceptance and the relevant isolated runtime checks. Broader retained animation
inconsistencies remain tracked in ../veld-consistency-audit-v1/FINDINGS.md.
