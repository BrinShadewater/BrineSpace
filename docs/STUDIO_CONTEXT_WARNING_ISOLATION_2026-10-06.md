# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: prototype exit-warning isolation

## Objective and acceptance
Identify the anonymous reference-count-zero exit warning before admitting the
compressed animation backend. Keep actual Studio and selected visuals intact.
Do not suppress the warning, delete preview behavior or infer an engine cause.

## Current state
All new controls live under `output/compressed-crew-2026-10-06/bounds-cache/`;
their generators live one directory above. Normal runtime/art remain unchanged.
Full logs, isolated profiles and owner fingerprints are retained. All completed
controls exit code zero with no behavioral failures; warnings are classified
separately and remain a blocker. Every completed control preserves 2,936 owner
non-log files. No processes remain running from these controls.

## Verification
| Controlled change | Anonymous exit warning |
|---|---|
| Skip Studio canvas registration only (305 canvases skipped, zero missing routes) | Present |
| Construct/open Studio, close before its rendered frame | Present |
| Construct Studio without adding it to the scene tree | Present |
| Constructor only, remove effects-preview initializer | Absent |
| Constructor only, remove cast-preview initializer | Present |
| Construct effects preview only, in full prototype scene | Present |
| Construct its StubGame only, in full prototype scene | Present |
| Construct its StubGrid only, in full prototype scene | Absent |
| Full Studio, move grid allocation into StubGame._init | Present |
| Full Studio, pass grid to StubGame from effects._init | Present |
| Minimal native process: grid, game or effects constructor (three controls) | Absent in all |
| Minimal native process: reload original/adapted flood helper, then StubGame (two controls) | Absent in both |

Identity audit: 23 early Main references and Studio cast/players, normalized from
signed IDs to unsigned, match none of the warned object IDs. Earlier effects/
stub-game/stub-grid weak references also released. Thus ordinary retention of
these named objects, Studio drawing, UI registration and the two initialization
rewrites are not established remedies. The rewrites remain rejected experiments;
do not copy them into production merely because they seem tidier.

The constructor path narrows the trigger, but minimal clean controls show that
construction alone is insufficient outside the full scene. Reloading the flood
helper alone is also insufficient. This is not yet proof of a GDScript engine bug,
a texture-storage defect or a permanent Studio leak. The prior ten-transition
memory/ownership results retain their recorded scope; this warning remains open.

## Next action
Reduce the full-scene context while retaining StubGame construction: compare
immediately after startup versus after first render, actor recovery and simulation.
Use matched normal/private controls and preserve the guard/profile evidence.
Locate the first necessary stage before another implementation change. Continue
loading/frame work independently when this investigation ceases to produce useful
discriminating evidence. Full release scope, Mac checks and default-backend
admission remain unfinished.

Follow-up stage reduction exposed actual deferred camera callbacks using a null
scene tree during fast return-to-title. Three lifetime guards are now retained in
normal Main; permanent regression changes two failures/ten errors to none.
Recovered-only and full Studio/two-Continue controls exit cleanly with only these
guards updated, including absence of the anonymous warning. Ten-cycle confirmation
remains next; see `CAMERA_SCENE_LIFETIME_FIX_2026-10-06.md`. The original reduced
recovery control had engine errors and cannot establish an independent constructor
failure. The earlier initializer/factory experiments remain unaccepted.
