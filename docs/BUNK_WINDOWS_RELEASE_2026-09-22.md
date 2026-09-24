# Bought-bunk Windows and Mac test builds

Updated: September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Refresh the Windows test package with the installed four-crew bunk profiles,
sharing fixes and Bill's reduced overall helmet. Owner visual acceptance remains open.

## Accepted decisions and constraints
No Higgsfield, publication or commit. Preserve owner layouts and library marks.
Mac testing targets Apple Silicon; native Mac acceptance remains pending.

## Current state
Maintained exporter produced `builds/BrineSpace-bunk-polish-2026-09-22/BrineSpace.exe`
and its PCK. Build ID: `brinespace-c0508d641e858e5e`.
Matching Mac: `builds/BrineSpace-mac-bunk-polish-2026-09-22/BrineSpace.zip`.
QA fixture, logs, exact artifact hashes and screenshots:
`output/bunk-polish-release-2026-09-22/`; see `release-checklist.json`.
Both deliverable folders have README, NOTICE, build metadata and SHA256SUMS.
The isolated QA runtime contains an override and is not the deliverable.

## Verification
- Both exact PCK audits: 15216 assets each; missing, changed, remapped and unexpected all zero.
- Actual Windows release executable: New Game, simulation and F8 report flow;
  zero failures, debug=false, empty stderr, exit 0.
- 49 packaged bunk frame samples match reviewed source RGBA hashes; Bill's
  specific controller binding verified. Native gameplay screenshot inspected.
- Headless soak: 40 cycles / 800 frames, mean 0.77 ms, worst 13.8 ms.
  This is fixture simulation CPU timing, not gameplay FPS or balance acceptance.
- Maintained Mac exporter completed with matching verified 4.7.2 template.
  Windows/Mac source metadata match exactly. Universal 2 (arm64/x86_64),
  executable mode 100755, single PCK and no QA override pass.
  Ad-hoc test build, not notarized; native Mac runtime and signature acceptance unverified.

## Next action
Obtain native Apple Silicon testing using the checklist beside the ZIP.
Continue broader room/gameplay review and owner visual feedback; this smoke test
does not establish full expedition stability or public-release readiness.
