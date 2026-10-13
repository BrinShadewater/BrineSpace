# Marsh master repair handoff

Updated: 2026-09-30 · Project: Brine Space · Task: repair the master-comparison findings

## Objective and acceptance

Owner authorized fixing the cargo, swimming, diagnostics and run/rest mismatches identified in `MARSH_MASTER_COMPARISON_2026-09-30.md`. Installed repair is ready for owner visual review at `character/marsh-master-repair-v1/index.html`: four identity masters, idle anchors, synchronized before/after playback, source/station scale and frame stepping.

## Accepted decisions and constraints

- Original directional identity masters remain authority. Idle, walk, crew conversation, welding and torch artwork remain byte-identical.
- Marsh is an android: existing white injury fluid retained exactly; ordinary shutdown remains dry.
- Preserve frame silhouettes, canvases, pivots, standing height, authored timing and all other state metadata. Shared cropped poses use the same revised artwork across transitions and reversals.
- This repairs detail and materials within accepted silhouettes; it does not replace motion geometry or claim perfect high-resolution master equivalence.

## Current state

Built 399 distinct edited poses from 21 master-referenced source sheets; installed 788 frame slots across 174 of 204 reviewed states. Added chest/collar/harness/pouch construction, restrained fabric detail and more adult facial detail in cargo, water, run, rest, galley and shutdown artwork; diagnostics retain canonical head and boots while improving torso detail. Repaired a distorted generated injury-start body with the matching reviewed dry pose and original white fluid. Corrected extraction of reflowed partial sheets before installation.

Static ivory grades follow directional idle anchors, blending directional targets through turns. Each unique pose has one reusable grade. Maximum within-clip ivory mean range fell from 30.26 to 15.92; remaining directional range is a diagnostic measurement, not a visual pass criterion.

Files: new `character/marsh-master-repair-v1/` sources, candidate sheets, frame exports, three manifests, selection, provenance, prompts, audit and review page; `character/marsh-v2/catalog.json`; refreshed `character/marsh-consistency-review-v1/`; master-comparison page navigation; five new prepare/package/install/publish/audit tools; rebuild override and colour-lock audit additions. Earlier exports remain recoverable and unchanged. Prompt recording caveat for sheet 00 is explicit in `source-prompts-final.json`.

## Verification

- All 21 candidate contact sheets inspected; selected final graded cargo/water/run/diagnostics/injury boards rechecked. Seven refreshed native station-scale summary boards inspected.
- `audit_marsh_master_repair.py`: 1,058 slots / 204 states, unchanged alpha geometry, registration, timing, accepted anchors, diagnostic head/boots, white fluid, shared-pose equality and source hashes. Current runtime contract matches selection.
- Godot 4.7.2 `test_marsh_quality_v2.gd`: 22,504 checks, zero failures.
- Native `playtest_marsh_consistency.gd`: 204 states, 1,058 source/elapsed checks, 432 captures, zero failures. Published 27 native phase previews.
- Colour lock: 10,779 PNG paths, zero errors. Python compile and viewer JavaScript syntax passed. New PNG source/export paths use LFS.
- Both Godot invocations used separate scratch APPDATA folders; scratch logs confirmed. Real-profile fingerprint checked 2,775 readable files. Five live-session/parity/log files changed concurrently; locked current log excluded. These unrelated changes were left untouched. Main progress/checkpoint/layout files did not change. Evidence in `output/marsh-animation-audit/master-repair-*`.

## Next action

Native advancing motion review subsequently completed across 204 states / 1,058 slots and 30 sequences; chronological boards inspected without new major clipping or proportion defects observed. Timed before/after and station-size review: `character/marsh-master-repair-v1/motion-review/index.html`. See `MARSH_MOTION_REVIEW_2026-09-30.md` for findings, capture fixes and limits. Owner motion acceptance remains pending. Browser automation rejected local `file:` URLs; continuous browser/gameplay acceptance is not claimed. No further demonstrated artwork repair is pending. No commit made in the shared dirty checkout.
