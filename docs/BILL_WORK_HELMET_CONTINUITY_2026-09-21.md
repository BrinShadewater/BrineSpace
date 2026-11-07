# Bill work helmet continuity: north and south

Updated: 2026-09-21. Continuation of the west helmet repair; broad goal remains open.

## Objective and accepted decisions

Keep Bill's physical helmet at the same size across standing, walking and work.
North/south work used 34x40 while the corresponding standing overlays are 48x56.
Review independent source views; do not mirror them or change bodies to hide fit errors.
No generation, Higgsfield or owner-room changes.

## Installed change

Both action builders now consume explicit overlay_size 48x56 and anchor offset 23,25
from their helmet registrations. Per-pose head anchors and body pixels remain intact.
Normal-size north/front candidate sheets were inspected against standing references
before installation, including all six lowering poses and shoulder/tool overlaps.

The canonical rebuild changes 36 equipped kneel/repair/stand PNGs and two fit
registrations. All other captured art/metadata files remain byte-identical. All 36
installed PNGs match the staged candidates. Bare artwork, playback and room layouts
are unchanged. Evidence: output/bill-north-south-helmet-size-2026-09-21.

## Verification

Full 2,214-frame validation passes with 780 original frames and 113 original manifests
preserved, zero errors/border touches. The helmet regression now checks west,
north and south against standing overlay dimensions and opaque shell pixels.
It passes. Work endpoints and stand reversal remain pixel-identical. Source-stage
checks preserve every pixel below the fitted helmet region.

Native action captures completed for both directions: 198 frames per equipment
state, zero failures and no logged errors in north-native.log and south-native.log.
Equipped working frames were inspected at room scale in both directions. The
fixture forces facing and helmet selection; it proves rendering/action coverage,
not autonomous facing, equipment donning or complete expedition acceptance.

## Remaining work

Body style/proportions and full gait/action transitions still require review;
equipment continuity is one defect, not complete character acceptance. Preserve
the owner's room layouts. Release archives predate these corrections.
