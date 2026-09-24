# Animation and Biodome polish test builds

Updated September 22, 2026. Broad project goal remains active.

## Objective and constraints
Refresh local Windows/Mac test builds with the installed locker identity repairs,
shelf helmet fit, console contact/power/restore fixes and Biodome composition.
Preserve existing packages and owner data. No publication or commit requested.

## Deliverables
Matching build ID: brinespace-b0d1640cfe18c6fc.
Windows: builds/BrineSpace-polish-2026-09-22/BrineSpace.exe and BrineSpace.pck.
Mac: builds/BrineSpace-mac-polish-2026-09-22/BrineSpace.zip.
Each folder includes README.txt, NOTICE.md, build_info.json and SHA256SUMS.txt.
The Mac folder also retains its expected manifest and export log. The Windows
expected manifest is frozen with QA evidence. Earlier bunk-polish builds remain.

## Verification
- Maintained Windows and Mac exporters completed with Godot 4.7.2 and matching
  verified templates. Source identity matches across both packages.
- Release dependency tests: 8 pass; assert-safety: 2 pass; Mac exporter: 2 pass.
- Each exact PCK audit checks 15216 assets: missing, changed, remapped and unexpected
  counts all zero. No runtime source corrections were needed during packaging.
- Actual Windows release executable passes New Game, processing/visibility,
  transmission Continue and F8 diagnostics: zero failures, debug=false, exit 0,
  empty stderr. Native gameplay screenshot inspected. It verifies 49 bunk frame
  samples plus 48 installed locker PNGs and the Biodome card against source RGBA.
  These image checks are not a packaged playthrough of all repaired actions.
- Mac Universal 2 bundle structure passes (arm64/x86_64, executable mode 100755,
  one PCK, no QA override). Ad-hoc testing build, not notarized. Native Mac
  execution and signature/Gatekeeper acceptance are unverified.

Evidence and exact hashes: output/polish-release-2026-09-22/release-checklist.json.
QA autoload/isolated runtime stays under output and is not a deliverable. Source
build metadata identifies the selected modified worktree; no commit was created.

## Next action
Run the included Apple Silicon checklist on the owner's M1-or-newer hardware.
Continue broader expedition, motion, room-composition and performance review.
These bounded checks do not prove public-release readiness or full stability.
