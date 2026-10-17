# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: Natural tube label

## Objective and acceptance
Clean up BRINE's tube label to sit naturally on its casing. Visual revision ready for owner review.

## Accepted decisions and constraints
Preserve the latest character, smooth motion, tube material and saved room. Preview-only work continues the existing study.

## Current state
preview_room.gd inherits v8 and overrides only the label: removes opaque backing, uses bundled Barlow lettering, curves individual glyphs along the left front pearl panel clear of the central hardware. tools/preview_brine_corners.gd now targets this revision. build_preview.py produces the refreshed GIF from 200 native captures.

## Verification
Native isolated capture passed loop and rigid-face checks; save fingerprint unchanged. Reviewed room and tube crop. Latest successful capture: output/brine-corner-preview/session-46c657fe362d491da3e3a18ad254d7d2 (followed by a successful contrast/size refinement capture). No production integration.

## Next action
Owner visual review; integrate only as part of the pending complete BRINE art integration.
