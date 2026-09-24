# Animation and display test release

Updated: 2026-09-21. Build brinespace-2601720e53d908cc.

## Objective and accepted constraints

Provide matching local Windows and Apple Silicon-capable test packages containing
the latest verified artwork/display fixes. No upload, publication, commit or owner
room changes. Native Mac execution remains an owner hardware test, not a Windows
packaging result. The broad project goal remains unfinished.

## Deliverables and identity

- Windows: builds/BrineSpace-animation-2026-09-21/BrineSpace.exe and BrineSpace.pck.
- Mac: builds/BrineSpace-mac-animation-2026-09-21/BrineSpace.zip.
- Both folders contain README.txt, NOTICE.md, validation.txt, build_info.json,
  expected-manifest.json and SHA256SUMS.txt. No QA override is in either deliverable.
- Source SHA256:2601720e53d908cc66d5cad00586fe50489b85fbafeca187ccdf2fe9acd5bb2e.
- Source manifest:15,511 files,1,642,038,196 bytes; Git f380c42c046de276b0efe26364e7596ca2410ec7, modified.
- Windows PCK:1,689,242,908 bytes. Mac ZIP:1,695,322,789 bytes.

Includes the previous support-room build, connected Bill side walk, canonical-style
west work body, work helmet continuity, Radio powered displays and powered-display
retention. Earlier packages remain preserved. New authoring-source assets are still
included by the broad character dependency roots; reducing that is separate manifest
work requiring consumer evidence, not a directory-name exclusion during export.

## Verification

Maintained Windows/Mac exporters passed. Exact PCK audits on both packages checked
15,184 assets each: missing/changed/remapped/unexpected all zero. Source identities
match. Official Mac template verification and bundle audit pass: arm64+x86_64,
executable mode100755, one PCK, no QA override. Ad-hoc test archive, not notarized.

Actual Windows EXE, isolated profile, exit0/debug=false/zero failures/empty stderr:
normal title/New Game/architect/Continue flow, advancing simulation and visible
station, eleven room layouts in all rotations with repeated setup, Holo offline/
operating/held-clock effects, card mipmaps/MSDF, F8 report and dialogue-trace bytes.
Added96decoded-frame SHA256 comparisons against the selected runtime Bill tables.
Final gameplay screenshot was visually inspected. This is bounded startup/release
coverage, not a full expedition or owner motion/composition acceptance.

Evidence: output/animation-release-2026-09-21, including release-checklist.json,
exact manifests/audit logs, external smoke fixture and process logs. Final isolated
profile: BrineSpaceAnimationRelease2601720e-20260921235519068.

Two failed fixture attempts are retained: a nonexistent PackedByteArray.sha256_text
call was replaced with HashingContext; terminating that failed run left a test-profile
session lock, causing the next run's genuine previous-session overlay to pause play.
The final driver creates a fresh profile per attempt and checks no recovery overlay
is present. No product code or crash recovery was bypassed to pass the test.

## Next actions

Run the Apple Silicon checklist beside the ZIP. Gatekeeper/signature acceptance,
native gameplay, controls/audio and save/resume are unverified. Continue ordinary
expedition and owner animation/composition review, plus remaining furnishing and
performance work. A four-direction Bill comparison is retained under
output/bill-direction-continuity-2026-09-21; no further body replacement was selected
from that bounded static review.
