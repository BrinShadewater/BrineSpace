# Project handoff

Updated: September 26, 2026 · BrineSpace · Art and theme lock

## Objective and acceptance

Provide one definitive style/theme reference for future work, grounded in the
owner-accepted clean prop exports and established underwater setting.

## Accepted decisions and constraints

Retain muted hand-painted detail, matte materials, maintained interiors, complete
objects, true transparency, department identity and current prop facing. Preserve
owner layouts and source art. Acceptance of the 323 exports is visual; no game
installation or package validation is implied. Final extra3-5 rail was repaired
after the owner's otherwise-positive review.

## Current state

- Replaced BRINESPACE_VISUAL_AESTHETIC_BIBLE.md with the current specification.
- Preserved its complete previous bytes in
  BRINESPACE_VISUAL_AESTHETIC_HISTORY_2026-09-26.md, at the same directory level so
  historical relative links retain their original base.
- Added BRINESPACE_ART_REFERENCE_LOCK_2026-09-26.json: 323 IDs and SHA-256 hashes
  for every accepted master/native export, dimensions and source-sheet names.
- Added an eight-exemplar reference board (PNG covered by Git LFS), visually reviewed.
- Added current-specification pointers to CURRENT_STATUS.md and
  ASSET_PIPELINE_AND_WORKFLOW.md.

## Verification

Archive hash matched the original before replacement. Reference lock built from
all 323 existing master/native pairs; unique IDs asserted. Current links and
named exemplar IDs checked. Documentation-only change; no Godot or asset batch
tests required. No artwork, game code, owner data or runtime bindings modified.

## Next action

Use the bible and fixed reference IDs for future briefs. Preserve the Desktop
export folder with its relative paths when transferring work; the lock identifies
files but does not embed or reconstruct their pixels. Changes in style require a
new owner-selected reference revision. No art production or integration is
requested by this documentation task.
