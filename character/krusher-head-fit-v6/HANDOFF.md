# Krusher bare animation neck connection repair

October 4, 2026. Owner says bare animation heads look less connected than the improved standing reference. Preserve Krusher Dom / System Administrator / James utility suit / matte muted cyan #527C80, current V5 likeness and all helmet frames.

## Changed files and decisions
Latest native canonical candidate: character/krusher-james-canonical-v9, 24 idle/walk/tablet states and 2,122 frame references. build_canonical.py uses unchanged V5 authored heads, shared uniform native scale and original James body sources. Bare head registration compares each original body's collar band to its idle reference, with bounded rigid offsets, instead of moving the collar cutout with legacy portrait-placement offsets. Natural neck is inserted two source pixels deeper and the original collar foreground occludes it. Original torso, limb geometry, props, clocks, pivots and canvases preserved. Restored painted collar accents use the accepted cyan palette. No painted skin bridge, independent axis squeeze or new face generation.

## Checks and evidence
Source/body/shell/endpoint checks: 2,138 pass; all sixteen idle/tablet endpoints exact. Original canvases: 2,122 pass; metadata: 52 comparisons, only frame paths/authoring status differ. attachment-audit.json checks all 1,061 bare references: primary head connected to torso using four-neighbour opaque-alpha components; at least thirteen collar contact pixels in every frame, zero failures. This establishes raster contact, not owner anatomical acceptance.

All 1,061 helmet PNG references byte-identical to canonical-v8, recorded in helmet-preservation.json. Native Godot loader: 14,881 checks, zero errors across all 2,122 slots, original geometry and start/middle/end clocks. Scratch APPDATA; all 2,935 fingerprinted non-log owner files unchanged; engine exit0 and no logged errors.

Visually inspected eight paired before/after walk busts, current standing sheet and selected animated comparison phase. walk-review-mobile.gif and bare-connection-review.gif sample 4.5 seconds at original source clocks, covering at least one walking cycle in each direction. The GIF sampling is a review presentation, not a continuous native station recording. The first temporary audit was placed in the wrong branch and inspected helmet rows using stale variables; fixed before final audit. Final audit enumerates exactly the expected 1,061 bare references. An initial collar restoration brought back painted gold above the prior palette cutoff; corrected before final generation and native verification.

## Remaining work
Owner visual judgment on moving bare joins remains open. Other 562 action/life/water states still retain historical V4 heads and are not revised by this canonical repair. Coherent V5/V6 pitch/quarter/rest source propagation and complete portable bank remain future work; do not claim full-bank acceptance. No normal roster, gameplay, saves or fresh station lifecycle integration changed. No live process for this revision.

## Useful paths
Phone comparison: bare-connection-review.gif. Whole-body motion: walk-review-mobile.gif. Static native views: standing-review-mobile.png. Provenance and scripts live in this folder; native/verify.gd has its paired UID. candidate-bank-index.json names only revised canonical manifests.

## Remote preview delivery
Local-file image references and inline tool images did not display for the owner remotely. A new private Sites page is now published at https://krusher-dom-preview.brinshadewater.chatgpt.site. It serves exact current V6 standing/head PNGs plus an optional walking WebP, losslessly converted with decoded pixel/timeline equality checked. Sites reports deployment succeeded; user-device rendering remains their check. The Site source is isolated under the task visualization workspace, not the game repository. remote-preview.json retains Site identity, deployment/version, source commit and directory for updates. Use its .openai/hosting.json; do not recreate this Site. On Windows use Git Bash on PATH and TAR_OPTIONS=--force-local for the maintained source packager. No sprites or game behavior changed for hosting.

Owner clarified that “character reference sheet” means the original hero portrait plus four full-body turnaround design views, not the native eight-view sprite sheet. concept-04-krusher-dom.png is now copied byte-exactly as character-reference.png on the same private Site and shown above current native sprites. This is explicitly labeled the original concept, with later James-body sprite revisions separate. Site deployment succeeded; no new character art or game change. remote-preview.json updated to the current saved version/source commit.
