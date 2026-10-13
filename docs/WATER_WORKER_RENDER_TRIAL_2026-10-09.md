# Project handoff

Updated: October 9, 2026 - Project: BrineSpace - Task: private water-worker rendering

## Objective and acceptance

Continue the full PC/Mac performance/release-readiness plan. Overlap numerical
water preparation with parent drawing while preserving exact current inputs,
selected pixels/timing,normal simulation and owner data. Keep prototype private
until repeat timing and complete lifecycle/settings coverage establish admission.

## Accepted decisions and constraints

Max2in-flight jobs per grid/session. Mutable topology is exclusively transferred
from canvas metadata to work context until joined. Callbacks build numeric commands
only;no SceneTree/GPU/image/simulation calls. Main thread draws only exact input-key
matches and falls back synchronously. Stationary water retains normal cache.
No half-width trial combined;no renderer upgrade or thread-safety checks disabled.

## Current state

Private base starts eligible work in submit while parent drawing continues,joins
before its draw,restores topology and exposes current commands transiently. Input
invalidation joins/discards previous work;_exit_tree joins before freeing. Private
Moon dynamic draw replays matching [floor,level,clock,pump] commands;missing match
uses the normal synchronous path. Shared coordinator bounds2jobs;third room can
fall back. Normal game source remains unchanged this turn.

Native QA prototype:586checks/0fail.288sequential raster pairs cover3overlapping
Moon bases,4rotations,18pressure/clock steps,material on/off,nearest/linear filtering,
modulation. Additional latest-input image proves pending input replacement renders
current state;join/bound/consumption checks and immediate detachment with pending
job prove exit joins before deferred free.544jobs start/join and1632prepared water
calls consumed during sampled matrix. This is room-base coverage,not Studio props
or full owner visual/settings/culling acceptance.

Actual debug=false1080p40room/fourcrew/full-mission reference-first pair:
3,000idle frames per lane at1/2/4x. Shared private nav/storage/drone controls as
previous diagnostic;same measured Moon/helper/base/canvas sources/PCKs,only worker
flag differs. Candidate means35.639/36.673/37.554ms versus41.530/42.338/43.251ms;
p9538.003/42.649/49.696 versus47.365/50.201/57.819ms; p99better3/3 too. Initial gain
5.66-5.89ms. Candidate max122.316ms;all release FPS/stutter gates still fail.

All compared phase crew/drone/doors/lights/power/zoom/props/mission/resource endpoints
and final mission histories match. Candidate6238starts==joins,14933prepared hits,
sharedpeak2/active0 at finish; cumulative wait37.126ms (includes warmup). All3missions
return/unload/fullgraphs recover. Bothuploads4074 and settled end1916.471/exit228.259MiB
match; candidatepeak2408.880 vsreference2346.502MiB remains unexplained,no memory
improvement or no-growth claim. Renderer timing differences cannot prove worker
GPU gain;this targets main-thread preparation.

Evidence:D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/
water-worker-render/(native source/results),water-worker-runtime/(actual pair,
comparison.json,reference-source-audit.json,source/pack identities/full logs).
Only this handoff and CURRENT_STATUS.md change in checkout.

## Verification

Completed reference initially failed harness source guard because expected canvas
hash used pre-write LF string rather than actual Windows CRLF file bytes. Compiled
rows all match saved file sha de11dee4583449a712872b77b2870895d3833fff5b2cd12c2e0b565b89fcaf69.
Raw reference JSON retained unchanged;remaining source/branch/runtime checks independently
audited. Candidate-only runner corrected diagnostic expected-hash literal;measured
scripts and PCK inputs unchanged,adapter hashes differ solely for that validation
metadata. Do not imply identical adapter artifacts. No repeat of completed reference.

Native/actual logs clean after audited harness failure;compiled source/branches
verified,focused/debug=false,router releases,owners2936same,all processes terminal,
adapters restored. Intentional input-replacement/detachment tests remain private.

## Next action

Add pending-job cleanup for hidden/culled rooms (current _exit_tree coverage does
not establish hiding). Check pause/reduced-motion/layout changes/current-input
fallback and whole-room prop layering. Reverse actual pair order and compare CPU
wait/stutters/memory peaks before admission. Do not integrate based on one pair.
Continue full original loading/endurance/original-nine/Windows-target/Mac gates;
no public package or upload change occurred.
