# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: Full Veld sample journeys

## Objective and acceptance
Complete the master-matched animation set and cross-family polish. This milestone
adds actual sample journeys and loaded-return disk restoration to staged cargo proof.

## Accepted decisions and constraints
Use real dispatch, oxygen needs, airlock cycle, exterior routes and unloading.
Dedicated prebuilt station; candidates loaded explicitly, no production art/profile
promotion. Scratch APPDATA; 2,914 real non-log files unchanged. Preserve shared work.

## Current state
tools/review_veld_full_expedition_v1.gd/.uid and Python runner cover six journeys.
Four normal airlock orientations and two recalls; staged scientific actions/cargo
loops/turns and conservative profile. Native phase captures/report retained here
in expedition-review-v1; expedition-evidence-v1.json binds fixtures/runtime/source
hashes and 336 candidate references. Renderer fix in sub_biome_view.gd keeps ground
meshes owned by the drawing canvas until its next redraw; other shared edits preserved.

## Verification
18,307 checks pass in 51.62s, no engine errors. All normal expedition phases,
six pickup poses, actual cargo turns, dry unload, extraction/delivery credit and
four loaded-return disk restores with exact pixels/paused position. Exterior
pickup/return and dry unload reviewed at actual native station scale.
Initial fixture treated void body loader as Boolean; fixed. Passing phase assertions
initially concealed 35 mesh errors after restore. Same single journey without restore
passed; uncached-prop diagnostic still failed. Seabed cache rebuild freed meshes used
by retained canvases; ownership fix makes full six-journey native run clean. All failed
intervals retained under output/veld-full-expedition-v1/interval-before-*.

## Next action
Test safety/power/gear interruptions and additional disk phases/traffic, then install
staged cargo/action/turn art plus conservative clearance and prove normal loader
selection against source pixels. Continue remaining life/distress/recovery/death
coverage and whole-set consistency/polish. Full goal active; no owner/full-set acceptance.
