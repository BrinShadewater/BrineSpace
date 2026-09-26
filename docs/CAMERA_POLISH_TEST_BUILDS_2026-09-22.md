# Camera and Fit polish test builds

Updated September22,2026. Broad project goal remains unfinished.

## Deliverables
Matching Windows/Mac build: brinespace-fb99bc56643b745a.
Source SHA256: fb99bc56643b745a8c2d58b6b2aaeb6fa764ab3336629707a6f50e1615246549.
Windows: builds/BrineSpace-camera-polish-2026-09-22/BrineSpace.exe plus PCK.
Mac: builds/BrineSpace-mac-camera-polish-2026-09-22/BrineSpace.zip.
Both folders include README.txt, NOTICE.md, build_info.json and SHA256SUMS.txt.
Previous b0d1640cfe18c6fc packages remain preserved. No publication/commit requested.

## Changes and verification
Includes Continue camera focus after hidden layout and split-floor Fit preparation,
along with preceding locker/shelf/console/Biodome/bunk animation work.
Maintained exporters exit0. Windows and Mac metadata match. Both exact PCK audits
check15216assets with zero missing/changed/remapped/unexpected entries.

Actual Windows release: New Game/architect selection/transmission handoff,
simulation, disk replacement-scene Continue, Fit button and F8 pass with zero
failures, debug=false, empty stderr. Continue preserves crew/resources and centers
BRINE within1.41399viewport pixels at nondefault zoom. Fit starts and settles with
the core visible. Both restored/Fit screenshots inspected. These core-scene checks
are not a100-room performance remeasurement or all-action packaged playthrough.
49bunk frame samples and49locker/card PNGs match reviewed RGBA source pixels.

First actual executable attempt failed external QA indentation before testing;
its process was stopped and logs retained. Corrected harness ran in a fresh profile.
No production correction was needed during packaging. All QA overrides remain
outside playable folders.

Mac verified template, Universal2 structure and matching source/PCK audits pass.
Ad-hoc test archive, not notarized. Native Apple Silicon launch, Gatekeeper and
full gameplay acceptance remain open. Do not treat Windows execution as Mac proof.

Evidence: output/camera-release-2026-09-22/release-checklist.json (artifact hashes
and sizes), package.log, actual-release.log/stderr, pck-audit.log/mac-pck-audit.log,
release-restored.png/release-fit.png and exporter logs. This supersedes the
in-progress status in CAMERA_RELEASE_IN_PROGRESS_2026-09-22.md.

## Next action
Run the included Apple Silicon checklist on the owner's M1-or-newer hardware.
Continue owner motion/composition and broader expedition/audio review. Preserve
all named owner rooms and library marks. Test-build delivery does not close the
broad polish goal or establish public-release stability.
