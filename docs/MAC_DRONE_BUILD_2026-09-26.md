# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Mac counterpart to the drone Windows build

## Objective and acceptance
Update the Mac build to the same frozen runtime snapshot as Windows. Delivered
`builds/BrineSpace-mac-drone-runtime-2026-09-26/BrineSpace.zip`, with README, NOTICE,
build_info, expected manifest and SHA256SUMS. Previous candidates are preserved.

## Accepted decisions and constraints
Reuse the Windows frozen source at `output/drone-release-2026-09-26/frozen-source`.
Exclude later workspace edits and unfinished crew studies. No gameplay changes,
commit, upload or publication. Native Mac acceptance cannot be inferred from Windows.

## Current state
Both platforms are `brinespace-073f851880d1bda9`; source SHA256 `073f851880d1bda980dfbedcf0b2e7bd59f285fd168f11df24ee72f961e25624`.
All 15,676 source entries match exactly. The Mac PCK is byte-identical to the tested
Windows PCK: `ab695ee6aaab3f9585c680a13560e0e35bfff11957932eb9fccb0385964e6970`.
The Mac ZIP SHA256 is `6adaa076a2b9a077d10d1335bbd94465dcf9b393f4dcd67b1f5a0ba9dfec2236`.
The maintained `tools/export_macos.py` ran from the frozen tree. Verified template
inputs were linked read-only into that tree; runtime source files were unchanged.

## Verification
Two export-wrapper tests and selected-template preflight passed. Official archive
SHA512, actual selected Mac template hash and Godot 4.7.2 editor version verified.
Export completed successfully. Bundle audit: x86_64 + arm64, executable mode 100755,
one PCK, no QA override. Exact PCK audit: 15,304 checked; zero missing, changed,
remapped or unexpected assets. Source-manifest and PCK parity with Windows passed.
Evidence: `output/mac-drone-release-2026-09-26`, including parity.json,
bundle-audit.json, pack-audit.log and validation.json. Export log is in the delivery.

## Next action
Native Mac test: launch/Gatekeeper, New Game/Resume, room and drone animation,
save/relaunch/Continue, audio, fullscreen, trackpad and F8. Record Mac/chip/macOS and
this build ID. This is an ad-hoc local test build, not notarized; native runtime and
signature acceptance remain unverified. No further rebuild needed for docs changes.
