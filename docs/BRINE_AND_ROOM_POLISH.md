# BRINE and production-room polish

Completed the requested follow-up: smaller-window BRINE readability, horizontal doorway occlusion, cable-background cleanup and a fresh combined Windows debug export.

## BRINE

The title-derived body/card-v3 passes at actual 1280x720 and1600x900 (45 full frames each), supplementing the previous actual2560 pass. Native unscaled room crops were reviewed: face/skin and blue suit remain distinguishable, with the head below the cap and feet above the base. Fine facial detail naturally disappears at station-overview zoom. Evidence: output/brine-core/polish-1280 and polish-1600; zero assertions and no script errors.

## Doors

Ordinary horizontal room connections now use the existing low cutaway trim, matching corridors and preserving the 72-unit aperture and sliding leaves. No tall header crosses the open central passage. The animation fixture passes four finishes, both orientations, 88 crossing poses, mixed power and pause. A new assertion guards the open horizontal actor area. Evidence: output/brine-core/low-door-regression.

The current Bill controller completed16 crossings/112 frames across all BRINE port/rotation combinations. All three unscaled review pages were inspected: the open horizontal passage no longer hides his upper body. Evidence: output/brine-core/low-door-crossings and low-door-review. Normal wall occlusion outside the doorway is retained.

## Source-floor openings

Reviewed all ten donor images. Explicit source-space openings remove trapped background in14 assemblies across Battery Array, Research Lab, Command Center, Quarantine Cell, Maintenance Bay, Mining Drone Bay and Salvage Drone Bay. Simple polygon pieces expose the live floor; raster sources, machine platforms, equipment footprints and animation anchors remain intact. Ore Refinery, Storage Bay and Crew Lounge have retained platforms/furniture surfaces rather than speculative dark-pixel removal.

Exact openings and area records: rooms/production-ten/floor-cutout-review.json. Each revised room passes four-rotation operating/offline/pause/containment checks at1600x900, and native room crops were inspected. Seven512-square card-polish-v1 images are selected in station/card consumers. Evidence: output/production-ten/polish-*.log and corresponding room folders. This is a targeted cleanup of reviewed openings, not a claim that every donor pixel is flawless.

## Export

output/room-rollout/windows-polish-34-v1 contains the fresh Windows debug executable and pack. It ran from an external working directory. All34 selected source hashes,68 source/card PNG decodes and the new BRINE body component hash/decode passed. The controlled production-controller tour reached51/51 placed rooms (34 identities plus17 support Batteries),135 reciprocal transitions and10377 checked movement steps. Zero assertions; export and runtime checks pass. Overview inspected; it is navigation/asset evidence, not detail-scale art review.

Pack SHA256: C71624E2CAFA22A3A2F7666F9BC20DE1180C97CD2AE966477C1D6F14D07DBA5D.

The build is a local debug validation artifact, not a published release or autonomous destination-choice test.
