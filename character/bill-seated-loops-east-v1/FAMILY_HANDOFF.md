# Project handoff

Updated: September 30, 2026 · BrineSpace · Bill east seated breathing and reading

## Objective and acceptance
Continue the full master-consistent Bill animation set, then cross-animation
consistency and polish. This milestone stages east seated breathing and reading
in both gear states. Owner acceptance and normal runtime selection are separate.

## Accepted decisions and constraints
Preserve the new east seated anatomy and current master matte materials, brown
hair, readable face, native helmet and planted boots. Breathing keeps both gloves
on thighs; reading holds one tablet in both hands, with one brief screen tap.
Keep shoulder/forearm/head joins anatomical. Shared256px plane, pivot128,224,
standingHeight148 and east selected sole223. No per-pose height normalization.

## Current state and changed files
Four gear states/24 references, six poses per960ms cosmetic loop. Breathing has
four independent interiors and exact selected east sitting frame005 at both
ends. Reading uses six independent poses with the prop present throughout.
Sources and prompts are retained in sources/: breathing generation
exec-1aad0029-d77d-4bc6-a04c-0ff1f5e534d9; reading generation
exec-1f284a70-f3c1-42ef-bf44-51659fc13fec. The initial breathing prompt was authored
under bill-seated-idle-east-v1; this combined loop pack is its source authority.

`build.py` freezes each source ruler: breathing .25/.276, reading .255/.28.
Anatomical material regions use measured source density1.11/1.07 and the selected
east grade from bill-seated-east-coherent-v1/grade.py. Boot contact is measured
after the single resize and translated to the exact seated sole. The native east
helmet follows authored head positions/reading tilts; original body pixels below
the collar region are protected. No actor logic, normal loader or registry changed.

## Verification
74 package checks pass: raw/frame bindings, frozen rulers, distinct authored
poses, seated joins, body protection, shared plane and boot contact. Isolated
candidate fixture passes157 native checks in12.55sec: loaded pixels/density,
scripted pose selection, cosmetic playback in cycles0/1/7, loop joins and a fresh
native82px board. Full-size and native paired loop boards visually reviewed.
All2,914 real non-log profile files unchanged under scratch APPDATA.

Current runtime observation snapshots support only north/south reading. The
candidate fixture explicitly expects east reading snapshots to be rejected;
it does not claim live east reading service, checkpoint or chooser acceptance.
Seated snapshots remain valid. This is source/player evidence, not furniture
contact or selected-runtime evidence.

## Remaining work and next action
East tablet take-out/put-away, exact neutral/reading stage joins, real furniture
review, normal family selection and saved/interrupted stages remain. West seated/
reading, other life/rest families, broader world journeys and full-set final
material/proportion/motion polish remain. Full Bill goal stays active.

Lesson: keep source/player evidence separate from actor snapshot and furniture
support. Generating a directional reading loop does not establish a service that
currently selects that direction. Keep material transforms bounded by source
density and retain exact seated entry/closure pixels across gear states.
