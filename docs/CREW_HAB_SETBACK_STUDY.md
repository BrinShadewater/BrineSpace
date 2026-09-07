# Crew Hab rear-chair setback study

The q3 rear-chair pose exposes Bill above the low north hull. This study keeps
the approved wall height, actor scale, 72-unit sockets and south-facing art.
V2 was subsequently integrated into the production room; packaged follow-up
remains pending. The initial isolated-study evidence is retained below.

`tools/crew_hab_setback_study.gd` subclasses the current room. In q3 only it
moves the chair and reading lamp 32 world units south; the chair-linked mat follows.
The bookshelf remains wall storage. V1's full-room capture exposed an overlap
with the nearby berth, so that arrangement was rejected despite passing depth
ordering. V2 also shifts `hab_berth_east` 24 world units west.

## Evidence

- `output/hab-chair-setback-study-v1`: twelve static depth checks pass, but the
  inspected q3 rear pose overlaps the berth. Not visually accepted.
- `output/hab-chair-setback-study-v2`: twelve static depth checks pass. The q3
  rear full-room image was inspected: no visible chair/berth intersection, and
  Bill's head no longer projects into the exterior above the cap. It still
  approaches/overlaps the cap's screen area, so this is not blanket silhouette
  acceptance for other actor poses or animation frames.
- `tools/playtest_hab_setback_study.gd` binds the candidate only in the test
  grid and runs the existing production-controller Crew Hab itinerary.
  `output/hab-setback-routes-v1` exits 0 without engine/script errors: four
  rotations, five scheduled arrivals each including return to start, six
  reciprocal transitions each, and 1938 collision/speed samples total.
  No teleported movement legs or changed collision rules.

Next: check the whole candidate composition, prop bounds and service access,
then integrate and refresh card/package evidence if those checks support it.
The gallery now links the integrated captures and retains a narrower warning
about cap proximity and unreviewed actor animations.

## Bounds, access and integration

The composition audit now reports interior visual bounds and standable side
midpoints in addition to footprint/visual intersections. These are sample points,
not a complete walking or work-animation service test.
`hab-access-baseline-v1` and `hab-access-candidate-v1` show all props contained,
no ground-footprint intersections and the same chair/lamp visual intersection.
At q3 the chair gains a clear left midpoint; the east berth loses its wall-facing
left midpoint but keeps front, rear and right clear. Current rest selection does
not require that left side. No collision or NPC behavior was changed.

Integrated the offsets before dressing placement in `crew_hab_view.gd`:
renderer SHA-256 `1EDF0C3DF98E384A80136813C7FEDCC3DEE6BE9253419FB3900EC7540E2FA099`.
The historical study subclass now delegates without applying offsets again.
Production q0/q1/q2 placement branches are unchanged; q0 card geometry therefore
does not require a new bake for this setback alone.

`hab-chair-setback-integrated-v1` exits 0, twelve static depth poses pass.
All 24 isolated normal/reversed PNGs match the V2 study exactly. The twelve
context PNGs differ: the shared checkout now renders a patterned green rug.
The integrated q3 rear context was visually inspected and retains the intended
chair/berth separation. Do not claim full-room pixel parity or overwrite that
concurrent decorative change.

`hab-setback-integrated-routes-v1` exits 0 without engine/script errors, passing
20 scheduled arrivals across four rotated layouts, 24 reciprocal transitions and
1938 production movement samples. Packaging and broader actor-animation review
remain separate follow-up work.

## Package attempts during shared UI changes

`output/batch-two/hab-setback-package-v1` stops at import on an undeclared
`reboot_button` reference in main. The shared checkout subsequently replaces
that reference with the picker opener. A fresh v2 attempt then stops on missing
`title_settings.apply_text_scale` in `architect_selection.gd`. Both failures are
retained; neither produced successful package verification. No unrelated UI
code was changed by this room pass. Retry only after the dependent UI scripts
compile; earlier packages do not verify the integrated setback.

The bible now clarifies usable standing space as part of furniture composition,
without changing the low-wall decision. Both room-pipeline repair-loop copies
record whole-group bounds/access checks and explicit service-side tradeoffs;
both validate and match SHA-256
`536893113EBF96310319E463F2B695796730308BCD6F1EFFFD87B919850C9215`.

V3's import confirms the earlier UI errors are gone, but catches type inference
failures in BRINE Core's display drawing: an untyped rectangle array made derived
Vector2 variables ambiguous. The room renderer now declares `Array[Rect2]`;
coordinates, colors and animation expressions are unchanged. V4 passes native
import and host preflight and creates the executable/PCK. Runtime outcome follows
separately; binary creation alone is not package acceptance.

V4's standalone mixed tour now passes from an external working directory:
31 arrivals, 88 reciprocal transitions, 6729 Bill collision/speed samples,
three active/present architects and 21 focused room captures. The loading gates
pass 20 sources, 40 raw source/card PNGs, 30 component images and 19 profiles.
PCK SHA-256 `39977736D3AD6D24FC9BB95327B12E1ED390B62164A3F7C71010DEF0E094FAD9`.
Evidence: `output/batch-two/hab-setback-package-v4/verification.json`.
The q3-specific exported route test is separate from this mixed layout, which
places the added Crew Hab at q0.

`output/hab-setback-exported-routes-v1` uses that same PCK from an isolated
temporary working directory. It completes q0/q1/q2 (480/488/483 samples), then
retains only q3's start capture without further output for nearly three minutes.
The uniquely identified test process was stopped after the 180-second review
window. This is timeout evidence, not a successful q3 traversal. The q3 start
frame was inspected at 1600x900; it shows the updated room but not the full route.
No engine/script error identified the stall. Diagnose this separately before
claiming packaged four-rotation traversal; native four-rotation evidence and the
passing mixed package retain their narrower scopes.

## Timeout investigation and successful replays

The fixture now supports opt-in `--trace-tour-progress`. It writes and closes
`last-tour-progress.json` around start/arrival captures, endpoint lookup, graph
route generation, smoothing and every hundred movement samples. The record
includes phase, elapsed ticks, target cell, foot and remaining path size. It
does not change movement, collision or recovery rules.

`hab-progress-package-v1` passes the three-crew mixed tour (31 arrivals, 88
transitions, 6784 samples). PCK SHA-256:
`122E9B3F2ACA4690FBF84205C10F19784C65A2EAFADDBEB8BA5A31699FBE2CC2`.
Its isolated focused run `output/hab-progress-export-v1` exits 0 without
engine/script errors: all four rotations complete, 20 arrivals, 24 transitions
and 1938 movement samples. Q3's final record reaches `after arrival capture`
at 16086 ms with an empty path at the starting cell.

A bounded replay of the exact earlier v4 PCK also passes all four rotations:
`output/hab-setback-exported-routes-v2`, child 0, no engine/script errors,
the same 480/488/483/487 per-quarter movement counts. This does not reproduce
the earlier stall, and does not establish its root cause. Keep v1 timeout evidence;
do not label the progress instrumentation a movement fix. Both package revisions
now have explicit successful four-rotation route evidence, while the historical
timeout remains unexplained.
