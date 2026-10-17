# Project handoff — Veld paired south water family

Updated:2026-09-30. Full Veld animation goal active.

## Objective and acceptance
Master-consistent full animation set, then cross-animation polish. This milestone
composes the complete south tread/start/swim/stop family in both equipment modes.
Owner and installed-world acceptance remain separate.

## Accepted decisions and constraints
Original/selected front master governs identity, proportions and palette. South
prone crown/face camera and rear collar placement follow canonical prone head.
Scanner screen-right, cylinders screen-left. No runtime binding/export changes.

## Current state
build_bare_loop_trials.py now registers body face through largest connected facial
skin region, not all warm pixels. Frozen .21 shoulder-scale hypothesis for six-pose
loops; named upright crown107 and prone face-bottom156. One source-family cloth/
patch/face curve against south selected idle. Skin grade restricted to connected
face components; stronger blue/green ratio excludes cyan scanner/chest lamps from
patch grade. Hair geometry/color and non-matching accents preserved from sources.

build_family.py writes8staged states/48frames,256x256,pivot128,128,standingHeight148.
Shared native upright/prone head components plus first3source-v2 pitch fits; last
near-prone interior reuses exact prone master to preserve correct collar camera.
Largest connected face supplies head fit; foreground glove pixels retained.
Four launch body interiors from saved south-transition-source-v1, fixed .18 scale
and face-bottom134/143/150/154, share family material curves. Exact new loop frame0
endpoints; stop exact reverse. Original timing,water/stride metadata retained.

Manifests,validate.py,contacts,review/template/make_review.py and fit records saved.
Aggregate material-v2/candidate-selection.json now32effective states/192refs;
new south overrides old south loops and adds starts/stops. Prior v4 selection saved.
No grid_canvas/ACTIVE_ASSETS selection edits. Cross-direction identity still open,
especially inherited east/west loop bodies and north's broader patch/cyan selector.

## Verification
12 bare loop border checks,48 paired protected-body/border checks,134 packaging/
reverse/exact-join checks PASS. tools/review_veld_water_material_candidate_v5.gd and
output/check_veld_water_material_candidate_v5.py:1104checks PASS, all32staged states,
192loaded texture refs, clocks/geometry/water metadata and actual four-direction
start/stop API handoffs in both variants. Native93/47 board1800x4200 viewed through
all south rows. Latest successful scratch profile changed[],exit0.

Initial source warmth anchor classified boot metal as skin, placing helmets off
body despite border/body-mask assertions. Caught visually before native candidate
gate, corrected to connected face. First native gate then passed. Material masks
were subsequently narrowed for actual face and blue-vs-cyan ownership; rebuilt/
revalidated/repeated native gate for changed pixels. Prior passing pixels/logs/
profile/capture kept in revisions/v5-before-material-ownership; latest1104checks
apply to current files. No broad/unrelated reruns.

Viewed paired loop/launch contacts and browser near-prone launch slot4 with93/47
station previews. Full screenshot browser-launch-slot4-v1.png. Source art/identity
and native functional checks do not prove owner acceptance or whole-world routes.

## Next action
Crosscompare all four staged directions with dry/original masters. Audit north
patch/scanner color ownership and inherited east/west loop armor/scale/hair; repair
those source families where needed before coherent water promotion. Measure native
installed clearances/joins then continue water turns/cargo/actions/distress/death,
everyday-life and final full-set polish. Goal incomplete.
