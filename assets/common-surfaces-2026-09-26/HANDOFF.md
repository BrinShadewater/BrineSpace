# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Counters, desks and surfaces

## Objective and acceptance
Six reusable surfaces matching established art, perspective and size-relative pixel density, including designs that abut walls. Owner visual review pending.

## Accepted decisions and constraints
Matte neutral materials, clear empty worktops, overhead/cutaway camera. Wall counter, wall desk and workbench have straight rear edges without projecting rear fittings. No furniture placement or runtime changes requested.

## Current state
masters/ and game-size/ contain wall counter, wall desk, workbench, wood desk, prep island and side table. Built-in image_gen; production.json and sources.json preserve prompts and provenance. manifest.json records crop, sizes, hashes, suggested display widths and wall-flush design flags.

## Verification
Six RGBA exports checked and reviewed against accepted native reference artwork on light/dark backgrounds. Broad visible worktops, complete supports, open knee spaces, straight rear edges on wall designs. Proportional premultiplied-alpha LANCZOS exports, alpha>=16 visible bounds with four source pixels padding, four export pixels margin. Budgets 85x85 for side table through 260x155 for workbench; suggested display width follows 0.34 world units per library pixel. Actual wall contact must align visible back edge rather than transparent canvas edge. No wall snapping, collision, seated-character fit or runtime placement verified.

## Next action
Owner reviews. For installation, register floor footprints and rear contact lines, then check wall contact and crew access in room.
