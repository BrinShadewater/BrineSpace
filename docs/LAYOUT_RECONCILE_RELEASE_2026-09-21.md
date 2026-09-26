# Layout reconciliation release checkpoint

September 21, 2026. Broad objective remains active.

## Objective and constraints
Package the four renderer repairs and four saved/default furnishing updates for
owner testing, alongside prior Bill/room/render polish. Preserve owner data and
older packages. No Higgsfield, commit, upload or publication.

## Current artifacts
Windows: builds/BrineSpace-layout-reconcile-2026-09-21.
Mac: builds/BrineSpace-mac-layout-reconcile-2026-09-21.
Both build brinespace-e3d4c7647fe9e73f; source SHA256
 e3d4c7647fe9e73f1e6e4368516261fbeadfce1f9ecb35d36eecb1577a273d27.
Git f380c42c046de276b0efe26364e7596ca2410ec7, modified worktree.
Manifest: 15,494 files, 1,637,183,339 source bytes.
Includes Salvage/Quarantine/Construction/Biodome restoration fixes, complete saved/
default layout reconciliation and refreshed cards. README, NOTICE, metadata,
expected manifest and SHA256SUMS accompany both packages. No deliverable override.

## Verification
Native editor station test: 49 rooms, 44 views, four rotations, 31 cached/direct
pairs. All 31 independently compared RGB arrays match exactly. Static/live reuse
and active crew/drone/construction checks pass. Close screenshot inspected.
Both exact PCK audits: 15,167 assets; zero missing, changed, remapped or unexpected.
Windows actual EXE: debug=false, zero failures, exit 0, no engine/script errors.
Checks navigation replacement/dormant/dead restore, four repaired rooms in all
rotations with repeated setup, title/New Game/architect/transmission Continue,
simulation, visible station, card rendering setup and F8 trace ZIP. Gameplay
screenshot inspected. Trace uses a labelled isolated fixture marker, not a
reproduction of the original dialogue report.

Two rejected harness runs are preserved: the first had mixed indentation in the
external added test; the second checked simulation after five process frames,
before Continue restored processing. The final run waits for transition removal
and process-mode restoration; diagnostics show mode 4 -> 0. The same observable
wait replaces the fixed wait in maintained tests/release_new_game_smoke.gd. That
test is outside the runtime manifest, so this fixture change does not invalidate
the exported source identity. No gameplay fix was made for these harness failures.
QA profile: BrineSpaceLayoutReleaseFixtureE3d4c764B; only isolated copied EXE/PCK
has the autoload override. Final evidence: output/layout-reconcile-release-2026-09-21.

Mac maintained exporter verifies the official template; bundle inspection confirms
arm64+x86_64, executable mode 100755, one PCK and no QA override. Source metadata
matches Windows. Ad-hoc test archive, not notarized; native Mac/Gatekeeper acceptance
remains unverified. Apple Silicon checklist is beside ZIP.

## Next action and limits
Test the Mac archive on owner's M1-or-newer hardware; gather Bill motion and room
composition feedback from the current checkpoint. Continue ordinary expedition
acceptance and targeted remaining saved/default review. These bounded checks do
not establish full game, visual or public-release acceptance.
