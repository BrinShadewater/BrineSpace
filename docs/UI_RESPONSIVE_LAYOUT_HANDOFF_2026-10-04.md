# Project handoff

Updated: October 4, 2026 · Project: BrineSpace · Task: compact-window readability

## Objective and acceptance
Check smaller windows, larger text and cards/inspector/crew spacing; correct readability or clipping problems in the live game. Preserve native visual review as well as geometry checks.

## Accepted decisions and constraints
Accepted hull/panel/card/portrait art retained. The existing Menu text size preference continues to scale menus/journals/summaries only. Compact gameplay windows now use a1600×900 design canvas below1440 physical pixels wide; larger windows retain1920×1080. This makes small-window text/buttons20% larger than the former uniform desktop downscale. Minimum physical window960×540 and Expand aspect behaviour retained. No gameplay, resource, save or asset selections changed.

## Current state
- `scripts/main.gd`: adaptive interface scale follows window size changes and restores desktop scale on enlargement. Compact top-navigation minimum width472 and gaps8 (desktop540/gaps12), keeping long resource captions from pushing Menu beyond the window. Deferred startup application occurs after UI construction.
- `tests/test_ui_responsive_layout.gd` and paired `.uid`, registered in `tests/index.json` hull-ui group. Covers four resolutions, expanded four-portrait crew strip, resource text, side dock/pinned controls, all navigation,130% pause menu text/action widths and journal reader/close control. Longest refill-caption stress fixture checks all header text and navigation together.
- Backups, incremental review and ten native captures: `output/ui-layout-audit-2026-10-04/`. No crew script changes.

## Verification
Final native Godot4.7.2 fixture148 checks/0 failures at960×540,1280×720,1280×1024 and1600×900. Native UI workspace suite PASS (camera fit/pan/zoom, selection, menu/workspace restoration and saved-state access). Final rendering/layout errors0; all2931 owner non-log files unchanged under scratch APPDATA. Logs/guards: `output/ui-integration-2026-09-30/responsive-reviewed` and `responsive-workspace`. Incremental added-line whitespace check passes.

Native minimum-window gameplay/pause menu,4:3 gameplay, large-text journal and final compact header stress views reviewed. Earlier113/117/143-check fixtures passed; visual stress review still exposed off-screen navigation because those checks only bounded the resource bar. Compact navigation fix and dedicated navigation bounds checks address it. Initial visual review also established that fitting controls were too small at the minimum size. Raster source/filters retained; larger compact rendering reviewed for card/icon readability rather than generating replacements.

## Next action
This layout pass is complete in source. Owner visual acceptance and a normal-play UX session remain separate from these isolated fixtures. No export or commit requested; concurrent character work preserved.
