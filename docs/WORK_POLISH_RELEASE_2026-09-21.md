# Work-animation and furnishing release checkpoint

Updated September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Refresh local Windows and Mac test packages with Bill's selected work repairs,
power-room grouping and the door-edge reuse optimization. No publication requested.
Owner visual acceptance, ordinary-expedition review and native Mac testing remain open.

## Current state
Build `brinespace-867eac6b1b17b4fc`, source SHA256
`867eac6b1b17b4fc7577c7c12bcec23df0d240eff8597e36223266f0c3095b17`.
Modified checkout based on `f380c42c046de276b0efe26364e7596ca2410ec7`;
15478 source files, 1631889158 bytes. Windows and Mac source identities match.

- Windows: `builds/BrineSpace-work-polish-2026-09-21/`.
- Mac: `builds/BrineSpace-mac-work-polish-2026-09-21/`.
- Evidence: `output/work-polish-release-2026-09-21/`.

Includes smaller helmet, four walk repairs, exact work endpoints, north/west work
identity repairs, grouped Turbine/Heat Recovery layouts and refreshed cards, and
per-call door connection reuse. Previous packages preserved. Both folders contain
README, NOTICE, build metadata, expected manifest, validation and SHA256SUMS;
Mac additionally has the Apple Silicon test checklist. No QA overrides in deliverables.

## Verification
Maintained Windows and Mac exporters exit zero. Both exact PCK audits from an
empty directory check 15151 assets: missing/changed/remapped/unexpected all zero.
Actual isolated Windows EXE exits zero, debug=false, zero failures, empty stderr:
240 decoded Bill frames, 225 authoring omissions, 15 room identities x4 rotations
with repeated setup, navigation restore, Holo effects, New Game/Continue/simulation,
card resources and F8 trace. Gameplay and report captures visually reviewed.

The first actual-release fixture inspected power rooms before render_into applied
their layouts. Sixteen support-presence failures were fixture sequencing, not
missing PCK files. Added a native preview invoking the production render path before
inspection; corrected full fixture passes. Failed logs preserved with pre-render-fixture
prefix. This changes the fixture only, not shipped code or the selected source.

Mac official template verification and Universal2 arm64/x86_64 bundle checks pass;
executable mode 100755 and one PCK. Ad-hoc testing export, not notarized. No native
Mac/Gatekeeper/gameplay acceptance established here.

SHA256:
- EXE: `7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76`
- PCK: `60375b5d68f44583ada3e73f68502cc8364ca79bfe7df865666820803608be50`
- Mac ZIP: `fc09620459ba49afc54ce6ca6d639f29659195effb1a3302a9831202efac1fba`

## Next action
Review ordinary expedition behavior and remaining art/animation issues; collect
owner feedback on Bill and furnishing, and native Apple Silicon results. Preserve
the ten protected room layouts and library marks. Broad polish goal is unfinished.
