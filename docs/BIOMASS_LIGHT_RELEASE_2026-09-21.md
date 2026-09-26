# Biomass and light-validation release checkpoint

Updated September21,2026. Broad objective remains active.

## Objective and constraints
Package installed Biomass furnishing/feedback and measured call-local lighting reuse
alongside prior Bill, drone, layout and rendering repairs. Preserve owner layouts
and older packages. No Higgsfield, commit, upload or publication.

## Artifacts and identity
Windows: builds/BrineSpace-biomass-light-2026-09-21.
Mac: builds/BrineSpace-mac-biomass-light-2026-09-21.
Both brinespace-c09c0a614a5c9299, source SHA256
c09c0a614a5c9299bb3eb1e2c5859eaa825231a3a168d71eb17cd24acf405287.
Git f380c42c046de276b0efe26364e7596ca2410ec7, modified worktree.
Manifest15497 files,1637250690 source bytes. New vessel texture and both registrations
are in dependency closure; raw generation is excluded. README, NOTICE, build_info,
expected manifest and SHA256SUMS accompany both deliverables. No QA override ships.

## Verification
Manifest Python suite6tests passes. Maintained Windows and Mac exporters complete.
Both exact PCK audits:15170 assets, missing/changed/remapped/unexpected all0.
Actual Windows executable:debug=false,0failures,exit0,clean final logs. Exercises
navigation replacement and inactive/dead restore; five rooms/four rotations/repeated
setup including Biomass; vessel PNG decode/dimensions and telemetry registration;
normal title/New Game/architect/transmission Continue; simulation, station visibility,
card rendering setup and F8 trace ZIP. Gameplay capture inspected.
The first smoke failed only its new nested-array comparison: JSON yields floats,
while the fixture expected integers. Exact packed inspection printed correct values
[[491.0,124.0,14.0,11.0]] and demonstrated integer-array inequality. Corrected the
external fixture's expected types and reran with fresh QA profile; no product change
or re-export was needed. Initial logs retained, not counted as passing evidence.
Final profile:BrineSpaceBiomassLightReleaseC09c0a61B.

Mac official template verification and bundle checks pass:Universal2 arm64+x86_64,
mode100755,onePCK,nooverride,pack1681025920bytes. Matching source identity confirmed.
Ad-hoc test archive; not notarized. Native Mac/Gatekeeper/gameplay unverified.
Evidence:output/biomass-light-release-2026-09-21, including final check record,
source manifests, exact audits, actual-release logs and native captures.

## Next action and limits
Test Mac on owner's M1-or-newer hardware using the checklist beside the ZIP. Continue
ordinary expedition and Bill/room visual acceptance. Broader49-room/31-pair station
parity evidence belongs to the earlier layout checkpoint, not a rerun for this build.
Current changes instead have focused Biomass native/parity/feedback checks and paired
light-validation key comparisons in their integration handoffs. No public-release
or full-game acceptance claim.
