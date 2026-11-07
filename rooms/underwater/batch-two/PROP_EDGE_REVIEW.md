# Forty-prop contrast review

All ten `output/batch-two/edge-sheet-<room-id>-v1.png` sheets were inspected.
Each contains all four registered props, offline, on dark and light backgrounds:
80 native diagnostic renders, not 80 new assets. Full captures and SHA-256 values
are retained in each `edge-<room-id>-v1/edge-review.json`. View hashes identify the
captured registration revision; source provenance remains in source-review.json.

`tools/review_registered_prop_edges.py` verifies capture hashes and crop bounds,
requires both backgrounds for each identity and preserves native pixels. No
resizing, alpha removal or source editing is performed. These backgrounds expose
outline contamination but do not prove sprite depth, routes or gameplay lighting.

## Findings and order of work

Anomaly aperture follow-up: platform shapes 18/19 now follow the sloped lower
lamp faces instead of using enclosing rectangles. Inspected native platform
light-background v3 against v1 and card v4: surrounding metal is restored, with
the two dark lamp openings retained. `anomaly-aperture-fit-v5.log` passes the
full source-violet coverage check and two covered/two excluded source-point
regressions. These points are not exhaustive contour approval. Other rectangular
hardware patches remain. Card v4 replaces v3 in both live consumers and export
manifest; original sources and old cards are preserved.

Card v4's bake logged a shared BRINE-core parse failure despite producing an
image. It is not accepted bake evidence. The shared script was already corrected
when rechecked; no unrelated source repair was made here. Card v5 was rebaked
with clean logs, inspected and selected in all three consumers. State-v4 likewise
printed PASS but logged engine/actor errors; retain it as failed evidence.

Anomaly follow-up: card v3 improves the receiver's three offline optical faces
with nested dark glass. A broader texture-modulation trial was rejected after
native `edge-anomaly_lab-v2` review: the platform strip lamps still appeared lit
offline. That trial is retained as rejected evidence, not the current renderer.
Platform/capacitor hardware patches remain in the cleanup queue. Source texture,
registration, collision, sockets and active marks are unchanged.

`anomaly-lens-registration-v3.log` passes source violet-mask coverage and three
interior-lens material samples in each rotation. The fixture-only flat-lens
negative control exits 1 in `anomaly-lens-negative-v3.log`; it does not change
production art. The new 512-square card was inspected and selected in both live
consumers and the export manifest. This is not full material or export approval.

| Room | Findings from both-background review | Follow-up |
|---|---|---|
| Clone Lab | Incubator contains obvious dark source-floor corners above the arch, beside the left support and below the right cabinet. | First repair: refined contour, separate v2 evidence below. |
| Biodome | Earlier spike is gone; grey fringe remains around raised fern/tree leaves. Processor pipe gaps need finer inspection. Aquatic tank's outer shape is comparatively clean. | Preserve leaves and equipment highlights; avoid universal grey-key removal. |
| Holographic Core | Computing cabinet lost detail beneath four flat panels in v1 evidence. Card v5 now retains dim source hardware; calibrator's concave outline still needs source comparison. | Material correction verified in the isolated pilot; continue fine outline/emissive work. |
| Anomaly Lab | Flat offline patches are visible across platform seams and capacitor/receiver details. Outer silhouettes are broadly coherent. | Do not confuse a luminance-mask pass with finished materials. |
| Xeno Lab | Broad silhouettes are coherent. Vessel has conspicuous flat patches on rims/pillars from offline suppression. | Review material versus actual emissive pixels before refining masks. |
| Data Archive | No comparably large source-floor corner spotted. Small offline rectangles remain obvious at this diagnostic scale. | Retain rack/terminal construction when polishing indicators. |
| Cryo Chamber | Outer shapes read well; tiny bevel/handle margins and dark console-foot region remain ambiguous in isolation. | Compare source before deleting possible trim or contact shadows. |
| Bio Lab | Broad outlines read coherently; reactor/console display fills are flat. Fine pipe gaps need source-level inspection. | Keep glass, fluid and painted green trim distinct from emissions. |
| Medical Center | Separate trolley/cabinet construction reads clearly. Desk/chair undercuts retain a grey region whose material needs checking. | Do not erase bases or shadows solely because they contrast with the diagnostic matte. |
| Medical Office | Separate chairs, table and exam console produce clear gaps. No large background island spotted in these views. | Continue native depth review; no blanket pixel-perfect acceptance. |

This prioritizes visual defects, not game balance. No palette, department, room
footprint, port mask or unlock change is implied. Existing operating tests stay
necessary but cannot approve the offline appearance.

## Clone contour correction

`edge-clone_lab-v2/clone_incubator-light.png` reviewed against v1 and the original
source: the three broad floor-contamination areas are removed while emitter,
supports, rim and front cabinet remain. The registration's footprint, pivot,
width and effect coordinates are unchanged. Three known-background points and
three retained-hardware points are now fixture assertions, not a full mask proof.
Card v2 is the station/card/export selection; original source and card retained.
The small supporting props were not edited. See CLONE_INTEGRATION.md for runtime
evidence and EXPORT_VERIFICATION.md for packaged scope.

## Xeno source-surface review (current capture v3)

Follow-up: material pass v4 restores locally modulated housing texture and nested
dark optical glass; card v3 is selected. See XENO_INTEGRATION.md. The repair brief
below records the preceding diagnosis; exact aperture-shape refinements remain
distinct from this material-detail improvement.

Compared `xeno_lab-source-v1.png` with the newly captured
`output/batch-two/edge-xeno_lab-v3/xeno_vessel-light.png`, not only the historical
v1 sheet. The current vessel still has the same flat offline patches. Capture log
`output/batch-two/xeno-edge-review-current-v3.log` reports eight renders and has
no ERROR/SCRIPT ERROR entries. Only the vessel's light-background frame was
visually inspected in this follow-up; the other seven are captured, not newly
approved. The recorded view hash is
`3b0fb1b3a4610165d381be37bf8aa7aae29ce95455399bebbfcd105aae57ebc8`.

Repair classification, using source-pixel coordinates from `display_regions()`:

| Region | Visible source construction | Required repair approach |
|---|---|---|
| `(294,205,40,41)` | Circular dark optical glass with two bright violet points, surrounded by a metal bezel. | Preserve lens depth without restoring the two painted active points. A uniformly flat disk is not the finished glass material. |
| `(224,201,14,24)` and `(386,200,15,24)` | Small lamps inset into curved vertical side hardware. | Keep curved housing and rim shading; suppress the lamp interior only. Rectangular silhouettes currently interrupt the fittings. |
| `(288,431,49,12)` | Narrow violet strip following the vessel's curved lower lip. | Match the strip aperture, retaining the light metal rim above it and its lower edge. The current broad rectangle visibly covers construction. |
| `(211,447,16,16)` and `(400,446,16,17)` | Small inset indicators on sloping base faces. | Use face-aligned aperture polygons, not axis-aligned patches extending over the face bevels. |
| Remaining small regions | Tiny residual highlights/indicator pixels. | Inspect individually after the broad repair; do not automatically restore them through a global texture tint. |

The tall central chamber's dark glass and the source's green sample contents are
not the defect being corrected. Keep them, the outer contour, registered scale,
collision, sockets and operating marks unchanged. Holographic Core's texture
modulation fix must not be copied wholesale: it could reintroduce Xeno's painted
violet activity. This requires separate glass, lamp-aperture and housing treatment.

Next gate: native before/after vessel inspection, explicit retained-housing and
suppressed-indicator samples, existing four-rotation state tests, and a new card
with both live consumers/export manifest updated. This section is a repair brief,
not a claim that the masks have been repaired or the room accepted.
