# Polish release checkpoint

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance

Package the latest Bill animation and medical-room work using the maintained
release workflow. This checkpoint does not complete the broader visual/polish goal.

## Accepted decisions and constraints

Preserve the ten owner-edited rooms and library marks. No Higgsfield, publication,
commit or source deletion. Native Mac acceptance requires Apple Silicon hardware;
the owner has M1 or newer. The Mac archive is ad-hoc and not notarized.

## Current state

Build **brinespace-1fe9515ad1c5f4c5**, modified working tree based on
`f380c42c046de276b0efe26364e7596ca2410ec7`.
Source fingerprint: `1fe9515ad1c5f4c529b32ee7936fcd1d72e09f7f52a246740b6b17ad0d5dcf56`.
Manifest: 15,478 files, 1,632,083,521 source bytes.

- Windows: `builds/BrineSpace-polish-2026-09-21/`.
- Mac: `builds/BrineSpace-mac-polish-2026-09-21/`.
- Evidence, fixtures and machine-readable checklist:
  `output/polish-release-2026-09-21/`.

Includes canonical south work poses, connected side walks, normal work helmets,
west work-body repairs, post-work facing-flash fix, Med Center/Office layouts and
cards, Med Center rotation retention, and Bill authoring-source collection trim.
Updated generated release manifests/build metadata and CURRENT_STATUS.md. Each
deliverable folder contains README, NOTICE, validation and SHA256SUMS files.
Earlier checkpoints remain intact.

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| Windows EXE | 109283328 | `7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76` |
| Windows PCK | 1672165732 | `73b886997da7d89b1861b6a54aff8dde775328beb07805b8b092c31cb1d58d1d` |
| Mac ZIP | 1678523984 | `1bda8de68e960af413e7ce052ea3ce4d435035ec0b1b3972920bd72f501b74bc` |

Windows PCK is 17,077,176 bytes smaller than the previous animation checkpoint.
That includes all intervening changes, not an isolated collector benchmark.

## Verification

- Maintained Windows and Mac exporters exited 0 with the same source identity.
- Both exact PCK audits: 15,151 assets; missing, changed, remapped and unexpected
  counts all zero. Mac PCK extracted from the completed ZIP for this audit.
- Actual Windows EXE: exit 0, debug=false, zero fixture failures, empty stderr.
  Fresh isolated profile; external QA autoload kept outside deliverable folders.
- Title/New Game/Continue, simulation and navigation restoration; thirteen rooms
  in four rotations with repeated setup; Holo powered/off/held-clock rendering;
  card resources; F8 dialogue-trace preservation.
- 176 decoded Bill frame hashes checked through selected runtime tables and 42
  authoring-source omissions checked through actual release FileAccess.
- Gameplay screenshot inspected. It shows startup framing, not a gait-motion test.
- Release assertion-safety and Mac exporter unit tests: two each, all passed.
- Mac official template, Universal2 arm64/x86_64 bundle, executable permissions
  and package structure passed. Native execution and Gatekeeper remain unverified.

## Next action

Continue Bill foot-contact and ordinary-expedition visual review, and improve
remaining weaker room compositions while preserving owner layouts. The broader
Bill test still has the known protected Research Lab q2 clearance failure; focused
movement fixes do not imply that full test passes. Owner gait/composition approval,
native Apple Silicon gameplay and public-release acceptance remain open.
