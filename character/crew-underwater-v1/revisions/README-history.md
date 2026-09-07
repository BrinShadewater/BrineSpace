# East swim stroke revision 2

## Current integration evidence

Native south doorway run 93436 passes and preserves 78 captures with hashes in
`south-cross-room-route-evidence.json`. Three middle-crossing samples were
inspected in `south-doorway-middle.png`: subjects and the passage are visible,
helmets remain attached, and no obvious wall clipping appears in those samples.
The prior run 102340 was obscured by draft UI and is not visual acceptance evidence.
The south fixture now zooms out to expose both rooms. Full-sequence playback
inspection remains pending. The revision checker now covers all nine integrated
east/west/south packs, including south source hashes, visor alpha and exact helmet
compositions; nine packs pass with zero failures.

Branforth's south candidate 03 replaces the wide second-pose arm sweep with a
bent-elbow catch at unchanged body scale. After rebuilding helmet fits and
clearance envelopes, all three actors complete the 19-node southbound route.
`south-route-tight-stroke.log` records PASS; the earlier failure log remains as
diagnostic history. No doorway geometry or collision margin changed. Native
moving southbound capture and continuous loop review remain outstanding.

Southbound route probe (`tests/test_crew_water_station.gd -- --cross-room --south`)
currently FAILS for Branforth: Bill and Veld complete 19-node routes, while
Branforth has clear endpoints but no safe full-cycle doorway lane in the sampled
-48..48 range. His revised outward arm sweep needs a narrower passage motion
or an authored stroke correction. Do not relax collision margins to make this
fixture pass. Evidence is in `south-cross-room-route-evidence.json` and
`south-route-test.log`; successful native phase selection does not establish
usable southbound navigation. The directional fixture also uses the correct
vertical capture region and keeps south evidence separate from east/west runs.

South camera corrections now include 18 body frames and 18 fitted helmet frames
across all three crew. Compare them at `review.html?direction=south`; these are now
provisionally integrated. Native south phase checks pass all six bare and helmet
phases for all three crew; movement and turning coverage remain outstanding. The review computes its canvas from pivot-relative extents so taller
south frames remain fully visible at a shared shoulder anchor. Four controller
tests pass, including all six south phases bare and equipped. These tests verify
frame selection and bounds, not continuous visual quality or native integration.

East and west stroke revisions and matching helmets are now provisionally loaded
for Bill, Veld and Branforth: 36 body frames and 36 fittings. Older candidate
notes below record earlier stages. Both runtime directions use the wider canvas
with directional shoulder pivots; the clearance exporter and main review consume
the same revisions.

West native phase playback passes all six bare and helmet phases per actor.
The furnished westbound 29-node doorway route passes for all three, including
horizontal holds in the narrow passage and treading after arrival. Native run
95436 captured 81 frames; 27 ordered samples were visually inspected in
`west-doorway-samples.png`. Helmets remain attached and no obvious wall clipping
appears in those samples. This is sampled inspection of one doorway, not full
continuous motion or all-direction acceptance. Exact captures and hashes are in
`west-cross-room-route-evidence.json`. North/south refinements remain outstanding.



Bill, Veld and Branforth each have six newly generated reach/pull/recovery frames.
Sources and exact prompts are preserved in `../generated/*-swim-east-candidate-02.*`.
Rebuild with `python character/crew-underwater-v1/build_swim_revision.py --actor ACTOR`.

These 18 frames now replace the east-swim rows through the normal runtime loader.
The earlier pilot files remain available for before/after comparison.
Each uses a 104 × 92 canvas, shoulder pivot (61, 44), and 14-pixel anatomical
head-height calibration. Contracts record source hashes, measured anchors, crops,
scale and placement. Canvas width accommodates forward-reaching hands.

[Synchronized comparison](review.html) shows the current and revised six-frame
loops with a shared clock and shoulder position. Contact-sheet inspection finds
more distinct arm phases for all three crew. Veld's torso pitch changes noticeably
between reach and pull; Branforth's shoulder orientation also changes during the
pull. Their temporal smoothness and registration still need review. The poses
are not approved merely because their alpha and margins pass.

First helmet fittings add 18 overlay frames with per-pose offsets and source hashes.
Rebuild with `python character/crew-underwater-v1/fit_swim_revision.py`. The comparison
has a helmet toggle. Near-side forearm pixels now restore over the collar in
reach phases 1 and 6; registration records the exact source rectangles. Run
`python character/crew-underwater-v1/check_swim_revisions.py` to detect stale
sources, mismatched timing/pivots, clipped content and incorrect compositions.

Native fixture: `tests/playtest_crew_water.gd -- --swim-revision` passes all six
bare and helmet phases for each actor, including exact texture selection and
104 × 92 dimensions/pivot retention. Captures are in `native/`. Agent inspection
of helmet phases 1, 4 and 6 shows readable reach/pull silhouettes and retained
faces. Pixel-level comparison against authored prop rectangles found zero overlap
in all 36 fixed-position samples, including Veld's close console approach. These samples do not prove clearance along swimming routes or continuous
loop smoothness. The native log includes room-image loading/export warnings.

Remaining: review the loop seam and torso motion continuously, then verify
swimming routes and walls using the full body footprint. The widened rows and
helmet fits pass native phase selection through the normal loader; this does not
establish collision clearance throughout the station.

The shared NPC movement guard now uses generated swim/tread bounds, including
helmets and both facings during a turn. Tests for every actor reject a clear-foot
stroke that would hit a prop, allow unobstructed movement, and reject extension
beyond known floor. Water goal selection now searches the existing navigation
graph with node and facing as its state, validating swim envelopes on each edge.
Smoothing rechecks the full footprint and turns. All three crew complete the
synthetic obstacle detour; removing its connecting edge correctly yields no route.
Dry crew/save regression passes. Full-station water-route performance, crew traffic
detours, and integration with actual flooding/exterior traversal remain unverified.

After changing water frames or pivots, run `build_swim_clearance.py` from the
expansion directory (or its repository-relative path), then `check_swim_revisions.py`.
Clearance source hashes prevent silently using bounds from older artwork.

`tests/test_crew_water_station.gd` exercises one equipped in-room route for each
actor on an authored five-room graph (1,627 nodes). All arrive. Search time fell
from 53–68 ms to 2.1–2.6 ms after avoiding redundant floor sampling in rooms with
complete rectangular blockers. Corridor/legacy sampling remains. Logs preserve
the before/after runs; `station-route-evidence.json` records the latest result.
Synthetic obstacle, traffic detour, turn and missing-floor checks also pass.
This does not establish cross-room, exterior or worst-case search performance.

The cross-room probe (`--cross-room`) now passes for all three crew after separating
horizontal swim and upright tread bounds. Each follows a 29-node route from the
maintenance room into the adjacent storage room. Tests exercise a horizontal hold
while paused in the doorway and treading after arrival. The existing 16-unit graph
is sufficient with the correct travel envelope; no doorway art or grid change
was required. Search now takes about 12-13 ms on this fixture after pruning rooms whose
registered blocker bounds cannot intersect the sweep (previously 22-24 ms).
Worst-case and simultaneous multi-crew search costs remain unmeasured. Native visual review of the moving doorway sequence remains
separate from these controller/geometry tests.

Native `--cross-room --native` run 105612 passes and records 26 moving doorway
frames per actor (78 total), listed and hashed in `cross-room-route-evidence.json`.
Middle-crossing samples for all three show visible helmets and horizontal bodies
inside the doorway without visible wall clipping. Doorway-only GIFs accompany
that run. This is sampled visual inspection, not approval of every captured frame.
Earlier failed fixture captures remain outside the run directory; they are not
evidence of the corrected scene. Later full-room samples retain a stationary Bill
render outside the doorway crop, so do not present these as concurrent traffic tests.

Follow-up review inspected all 78 captures as ordered contact sheets. Helmets stay
attached and visible, strokes remain legible, and no wall clipping is visible in
this eastbound sequence. Veld's body pitch varies more than the other crew. This
is frame-by-frame inspection, not real-time motion review or coverage of other
doorways/directions. Contact sheets and GIFs now use a wider crop so Veld's trailing
foot is not cut by the review artifact; original station captures are unchanged.

West-facing revision candidates now cover all three crew: 18 frames, each
104 x 92 with shoulder pivot (43,44). They use independently generated west
references and retain Veld's blue scanner and Branforth's amber meter on the
visible left hip. Contact sheets show distinct arm phases. Head/torso registration,
loop continuity and native westbound testing remain pending; runtime
west rows are unchanged. The revision checker covers candidate alpha, margins,
frame count and source hashes separately from integrated east coverage.

West helmet fittings now add 18 frames across the three actors. Per-phase
registration keeps faces visible; recorded foreground arm regions restore the
reaching hands over the collar. The checker verifies each fitted image against
its exact body, overlay, placement and foreground regions (six revision packs,
zero failures). Contact-sheet inspection covers all 18 fittings; this does not
establish continuous motion quality or native westbound clearance.

Use `review.html?direction=west` for synchronized previous/candidate playback,
including helmet toggling. The page's three controller tests cover initialization,
timing and west asset loading. East remains integrated provisionally; west body
and helmet revisions remain review candidates.
