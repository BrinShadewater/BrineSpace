# Construction Drone Bay material repair — agent review complete

Latest checkpoint: static equipment and the recognizable live drone are integrated
and agent-reviewed. The shared fleet source remains byte-identical; only the
Construction source rectangle receives a decode-time matte ochre/graphite material
transform. Mining and Salvage regions are untouched. Docked, travelling and
articulated working states retain the exact silhouette and animation UVs. Evidence:
`assets/construction-material-v2/drone-material-review.json` and
`output/construction-owner-repair-2026-09-12/drone-material`.
The selected q0 card now includes the matte drone. Drone fleet, paid jobs,
lifecycle, Production Ten connections/walker paths, 176 room layouts, 20 side
variants and all 47 card identities pass; the latest art run is
`output/test-runs/20260912-223410-headless`.

The earlier static equipment repair is integrated and agent-reviewed.
The square cradle replaces the rejected slotted study and supports the unchanged
drone in all four directions. Native empty/docked evidence: `cradle-square`; final
room evidence: `cradle-native` under `output/construction-owner-repair-2026-09-12`.
Final functional run `20260912-200457-headless` passes drone fleet, 176 layouts,
production-ten walker paths and 47 cards. An unused former atlas loader was removed
after capture; it had no remaining callers. q0 card refreshed; sources/hashes in
`assets/construction-material-v2/static-review.json`.

The owner asked whether the drone itself needed redesign. Native review supported a
material repair while retaining its recognizable silhouette. The selected runtime
transform reduces orange gloss and white sparkle; an image-generation study with a
better yellow/graphite palette was rejected because it changed the canvas, arms,
grippers and outline. No gameplay timing or animation geometry changed. The
chronological notes below preserve earlier candidates and intermediate checks.

Updated: September 12, 2026 · BrineSpace room-asset queue.

## Objective and acceptance

Resolve the owner's overly metallic room assets and match the matte room style.
The drone redesign question remains open; no silhouette replacement is implied.
Gameplay and character animation belong to the other sessions.

## Current state

Generated a matte repaint from `assets/construction-directional-v1/construction-south.png`.
Raw output and exact prompt are preserved in `assets/construction-material-v2`.
The CNC casing and fabrication worktop have fewer bright scratches and broad readable
midtone planes. Four clamps, two tool heads, six drills, five holders, four drawers
and two spools remain. A second targeted repaint removes the roller and spool reflection
bands; `construction-south-refined-raw.png` and `refinement.prompt.txt` preserve it.
Four refined native views were inspected; wall material repair passes agent review.
The room remains incomplete until its independent machinery is repaired.

`tools/build_construction_matte_directions.py` cleans only border-connected pale
background, crops the result and creates exact quarter turns. All four construction
registrations select those images. Original registrations are backed up alongside them.
This also replaces the older angled side geometry with the overhead bank. Existing
floor-prop layout is unchanged. Static draw helpers now accept an optional texture;
Construction alone selects the repainted atlas for cradle, bench and hatch. Drone
draws and other bays continue using the original atlas and animation path.

## Verification

Native four-orientation capture: `output/construction-owner-repair-2026-09-12/candidate-native`.
Baseline: sibling `before` directory. Final q0–q3 images inspected after restoring
`wall_contact` metadata. Without it, south bank placement was wrong despite the
layout/card/side suites passing. The metadata is an active renderer contract.
Final native capture has no stderr. q0 is copied to the existing selected card.
Relevant regression results are recorded in the pack review JSON.
Final run `20260912-193414-headless`: 176 layouts, 20 side variants and 47 cards pass.
The lesson was appended to both room-skill copies. Full sync inspection reports four
existing file differences (gameplay-preview contract, layered assets, material review,
sync checker); unrelated content was preserved instead of overwriting either copy.

## Next action

Latest native evidence: `output/construction-owner-repair-2026-09-12/refined-native`.
Regression run `20260912-193727-headless` passes 176 layouts, 20 side variants and
47 cards. The current q0 card uses this refined capture.

The bottom-row cradle, bench and hatch from
`assets/construction-material-v2/floor-equipment-candidate.png` are integrated.
All visible component bounds stay strictly inside their original source rectangles;
two cradle gap probes key out and the hatch lid probe remains opaque. Fresh q0–q3
captures in `output/construction-owner-repair-2026-09-12/floor-native` pass material
and placement review, with no stderr. `floor-review.json` records hashes, probes
and the 176-layout/20-side/47-card passing run `20260912-194110-headless`.
The existing q0 card now matches this capture. The generated top-row drones are
unused. Existing fleet animation and original drone pixels remain selected.
Drone fleet, production-ten connections and walker paths also pass in
`output/test-runs/20260912-194229-headless` after the optional texture change.

Panel rack now uses a matte low flat-storage companion, built by
`tools/build_construction_panel_pallet.py`. The rejected first edit retained tall
plate faces; both raw candidates and prompts are preserved. The final companion
uses five flat stacks and a crosswise spare stack. Runtime picks inward release
direction from the prop center and fits its aspect inside the previous 90 by
80.12 maximum rectangle; draw and reported bounds share that calculation.
Native q2 reviewed in `output/construction-owner-repair-2026-09-12/panel-native`:
the pallet is readable, matte and faces right toward room center. Other normal
layouts omit it, so alternate pallet placements still need explicit review.
Follow-up: `tools/capture_construction_panel_facings.gd` now exercises the live
texture-selection and bounds helpers at north/east/south/west placement centers.
`output/construction-owner-repair-2026-09-12/panel-facings/facings.png` was inspected:
all four release edges face center. Recorded sizes are 81.82×80.12 for north/south
and 78.46×80.12 for east/west, within the former maximum. Native stderr is empty.
This closes alternate pallet-facing review; it is a component fixture, not a claim
of four occupied room layouts or crew clearance beyond the existing route checks.
Layout, side-variant, card and production-ten walker-path checks pass in
`output/test-runs/20260912-194614-headless`. Native capture stderr is empty.

Remaining floor machinery needs explicit
overhead/inward-facing review; these material captures do not prove that contract.
The assembly bench now has a generated overhead companion: joint caps and parked
arm read from above, tool tray and controls face the operator edge. Raw RGBA alpha
is preserved by `tools/build_construction_overhead_bench.py`; four exact turns
use the same inward selection as the pallet. Draw and bounds use one fitted
rectangle inside the previous 100×77.78 maximum. q0/q1/q3 native views inspected
in `output/construction-owner-repair-2026-09-12/bench-native`; q2 omits the bench.
The narrower side view remains legible. Current q0 card refreshed.
176 layouts, production-ten walker paths and 47 card identities pass in
`output/test-runs/20260912-195142-headless`; native stderr is empty.
Cradle/hatch camera review and the drone design decision remain open.
Hatch source review found the existing oval lid/front lip incompatible with strict
overhead. A new circular-lid candidate is preserved as
`assets/construction-material-v2/hatch-overhead-raw.png`, with prompt and alpha/hash
review. It is not installed. `scripts/drone_art.gd::draw_hatch` draws an aperture
offset by -0.065 width with ellipse radii 0.32/0.24 width; that visual overlay must
be aligned to the new lid in Construction only. Preserve `hatch_open` state/timing
and verify closed, partial and open native states before replacing the live source.
The candidate has four clamps and bottom release controls; turn those inward.
Hatch integration follow-up: `tools/build_construction_overhead_hatch.py` removes
alpha below 16, crops to 959×993 and writes four exact turns. Construction's view
uses source-coordinate aperture center/radius and the existing `hatch_open` value.
No deployment timing or state changed. Native 12-state component sheet in
`output/construction-owner-repair-2026-09-12/hatch-states/states.png` passes visual
alignment review; four complete room captures in sibling `hatch-native` pass
placement and material review. Both captures have empty stderr. Drone fleet,
176 layouts, walker paths and 47 card identities pass in `20260912-195709-headless`.
The selected q0 card is refreshed. Hatch camera work is now complete at agent-review
level. Cradle camera review and the drone design decision remain open.
Cradle follow-up: generated overhead source and four cleaned turns are preserved
under `cradle-overhead-*`, with exact prompt and alpha-gap probes. Native comparison
`output/construction-owner-repair-2026-09-12/cradle-candidate/empty-docked.png`
shows the unchanged drone on all four candidate orientations. The side-facing
support shrinks below the drone width when fit inside the old envelope; rejected
for docked fit, not installed. Next: nearly square support deck, then repeat the
empty/docked comparison before selecting it. Source-only work; no new gameplay tests
needed for this rejected candidate. Fixture stderr is empty.
Shared fleet atlas consumers include Mining and Salvage;
resolve source selection explicitly before changing shared pixels. The selected
region-local decode transform now supplies that isolation and has been reviewed at
gameplay scale with corrected furnishings. A silhouette redesign is not supported
by the current evidence. Construction's reported material mismatch is complete at
agent-review level. No export or owner visual acceptance is claimed.
