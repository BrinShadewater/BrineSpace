# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: actual West lossless indexed drone storage

## Objective and acceptance

Reduce the measured mining West full-sheet upload while preserving exact selected frames/effective filtering. Full PC/Mac memory, frame pacing, loading and release gates remain open.

## Accepted decisions and constraints

Private feasibility only; normal runtime/art/quality unchanged. Full original dimensions and hardware nearest texture sampling preserved via RG8 color indices plus immutable RGBA palette. No lossy colors or discarded frames. Linear still requires original RGBA fallback; no indexed linear claim. Preserve runtime PNG compatibility before admission; current raw private binaries are not release assets.

## Current state

output/drone-west-indexed-2026-10-06/{prepare.py,probe.gd,run.py,encoding.json,results.json,remap.gdshader}; upload-repeat/ holds three allocation pairs. Exact source reconstruction of all 144506880 RGBA bytes:13987 colors, 256x55 palette, 72309760 indexed+palette bytes (about half original). Source SHA256 recorded, original source untouched. Offline Python preparation2.9s is not runtime loader performance.

## Verification

Authoritative corrected native test: all180 original cells x3scales x2mirror views =1080 exact nonblank image comparisons, zero failures. Every original/candidate capture explicitly has visible pixels. 600x600 view fits full frame; uses original region coordinates and nearest hardware sampler. Selected West frame90 original/indexed captures retained and indexed capture visually inspected. Engine logs clean/exit0; owner2936 non-log files unchanged.

Initial1080 equality probe lacked nonblank enforcement: mirrored negative rectangle was wrongly translated right, leaving some clipped or entirely outside viewport. First narrow visual check asserted blank and two probe processes were explicitly stopped; failed logs retained, both fingerprint receipts unchanged. Observable per-case rectangles/captures isolated fixture error, not renderer/art bug. Final test fixes mirror positioning, viewport bounds and checks visible output; initial equality alone is superseded. Two-frame observation also used; no claim fixed wait alone proves rendering (nonblank checks do).

Final isolated upload: whole25362us vs indices12161us+palette45us. Earlier initial pair27810 vs13347+54us. Three alternating-order allocation pairs: whole24217/13509/12505us, indices6036/8173/5134us. All three lower, but these are main-thread API call timings within one process, not three release/gameplay runs. Source texture still allocated for reference comparison, so this probe does not demonstrate actual scene residency saving. Full indexed upload remains potentially expensive and does not meet frame targets by itself. No 4x/FPS/total memory/loading claim. All tested processes terminal.

## Next action

Extend the existing weak/session-owned private provider to West and integrate in the current mixed40-room physical fixture. Avoid retaining original RGBA when effective filter is nearest; preserve original identity/API for genuine linear consumers and account for fallback retention. Require original coordinates, PNG sidecars/hash validation, bounded preparation and cache ownership, ordered layers, worker shutdown and no duplicate ordinary cache. Measure actual West 4x transitions and upload aggregates, decoded/texture memory and scene-exit behavior. Cover remaining headings before normal admission; block release if whole-frame/memory gates still fail.
