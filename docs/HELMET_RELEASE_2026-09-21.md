# Walk and helmet release handoff

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Refresh local Windows/Mac test candidates with the four selected Bill walks and
smaller normal helmet. Preserve prior room, animation and performance work.
This checkpoint is not owner art acceptance, full-expedition acceptance or a
public release. Broad project goal remains unfinished.

## Accepted decisions and constraints
No Higgsfield, uploads, commits or publication. Preserve owner room layouts and
library marks. Normal building costs/failures remain enabled. Apple Silicon is
the owner's available Mac hardware; native Mac acceptance remains pending.

## Current state
Build: brinespace-f2ec1eb651c14137.
Source SHA256: f2ec1eb651c141373664e08e7d440354fd57190a125bbda21c555a15282cd4ca.
Git base: f380c42c046de276b0efe26364e7596ca2410ec7, modified working tree.
Windows: builds/BrineSpace-helmet-2026-09-21/.
Mac: builds/BrineSpace-mac-helmet-2026-09-21/.
Both have matching build metadata, expected manifest, rights notice, README,
validation notes and SHA256SUMS. Mac ZIP is Universal 2 with ad-hoc signing, not
notarized. Earlier packages remain intact; the unfinished Windows-only 5fc build
is superseded. Release workflow updated to prevent stale fixture paths.

## Verification
Evidence: output/helmet-release-2026-09-21/release-checklist.json and adjacent logs.
Maintained exporters completed successfully with verified Godot 4.7.2 templates.
Both PCK audits ran from an empty directory: 15151 checked; missing, changed,
remapped and unexpected all zero. Mac bundle architecture/permissions checks pass.
Actual Windows EXE, isolated copy/profile: exit 0, debug=false, zero failures and
empty stderr. Checked New Game/Continue and simulation, navigation restoration,
13 room layouts x 4 rotations, Holo effects, card resources and F8 trace bytes.
240 decoded idle/walk/kneel/repair/stand frames cover four directions and bare/helmet
variants. 158 authoring-file omissions checked. Gameplay capture visually inspected.
The initial harness pointed to the older walk fixture and failed 120 obsolete
helmet hashes plus its error gate. Preserved stale-fixture logs document this setup
error; corrected run passes. Driver now derives paths from its own folder and its
PowerShell syntax passes. No export rebuild was required for this QA-path fix.

## Next action
Owner can test the Mac ZIP on Apple Silicon using MAC_TEST_CHECKLIST.txt beside it.
Native Mac gameplay, Gatekeeper/signature acceptance and Intel execution are not
verified. Continue ordinary paid expedition/owner visual review, Bill north/west
work suit and backpack continuity, room polish and measured performance work.
Do not change or scatter props in the ten owner reference rooms.
