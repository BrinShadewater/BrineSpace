# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: first large-station restore attribution

## Objective and acceptance

Reduce first large-station Continue latency while preserving navigation graphs, collisions, actor state, responsive loading and save integrity. Full original PC/Mac release gates remain applicable.

## Accepted decisions and constraints

Profile the demonstrated bottleneck before changes. No permanent cross-session image cache, art reductions or gameplay changes. All work is private in the physical frozen source with byte-restoration in `finally`; scratch profiles and owner fingerprints required.

## Current state

Diagnostic runners and candidate are retained under `output/drone-compiled-2026-10-07/`: `run-restore-attribution.py`, `run-restore-navigation-attribution.py`, `prepare-navigation-edge-trial.py` and `run-navigation-edge-trial.py`. Normal runtime source is unchanged.

## Verification

Two native three-cycle traces pass 262 checks each with zero failures/errors/leaks/warnings; owner's 2,936 non-log files unchanged. RunSave and Bill source backups restore byte-exactly after each run. Native attribution supplements, rather than substitutes for, prior debug=false packaged timing.

The first restore's Veld phase takes 2.962/2.987 seconds versus 0.180/0.200 on the next. Bill is inactive (~0.3 ms); Branforth/Marsh ~0.18–0.20 seconds; application ~59–76 ms, finish ~13–20 ms.

Deep trace: first active navigation build has 48 uncached keys (cache 4→52) and 20,480 nodes. Geometry wall 784.769 ms includes 28.654 ms yielded wait; local graph wall 2131.691 includes 1580.254 ms wait; cross graph 64.352 includes 49.937 ms wait. Later actors reuse the cache, with ~1.3 ms geometry preparation. This identifies geometry preparation and cold graph generation plus slice scheduling; it does not identify every internal geometry cost or prove a fix.

Private trial prepares the original world-space grown/clipped blocker rectangles once per authored cell, then uses the original sweep for local edges between proven standable points. Corridors/legacy and explicit all-segment sampling preserve reference logic. Reference switch allows a matched comparison. First reference fixture exposed a typed conditional empty-array error; run stopped, sources restored, failed evidence retained. Explicit typed initialization corrects that trial-only error.

Corrected original/fast native three-cycle pair: 263 checks each, zero failures/errors/leaks/warnings. In each lane all 67,121 tested authored-cell edges match the original collision method across 76 geometry cells. All 12 recorded navigation graph hashes (points, weights, connections for all three active crew) and complete saved crew snapshots match between lanes. First Veld restore 2924.916→1857.028 ms (~36.5% lower); first large Continue total 9122.899→7993.154 ms (~1.13 seconds lower). Later Continue 5652.988→5669.831 ms, essentially unchanged. Native debug timings, one ordered pair, not packaged or hardware acceptance. Detailed summary: `navigation-edge-trial-summary.json`.

Both frozen scripts restored byte-exactly; no normal runtime patch. Large QA adapter archived as `qa-cold-hints/large-loading-lifecycle.gd`, identity checked; small comparison adapter restored byte-exactly. All processes terminal and owner's 2,936 files unchanged.

## Next action

Repeat the measured packaged improvement before admission; cover explicit sample-all fallback and further layout invalidation. Attribute remaining cold geometry preparation (~0.76 seconds in earlier native trace), then address its actual hotspot. Independently investigate title retained memory and continue original gameplay/memory/bug/endurance/target PC/Mac scope.

## Packaged follow-up

Synthetic boundary suite passes 171,094 eligible exact collision comparisons (zero differences), including tangent/half-open edges, thin and zero-area rectangles, closed/open sockets and multiple station coordinates. Headless existing segment-clearance, navigation-rebuild-stagger and reactor-route tests pass with zero errors/warnings; the reactor's old tangent example is explicitly inapplicable to current art, while general tangent coverage passes. Rebuild test verifies one actor per update after room placement. These do not certify every Studio layout edit or sample-all fallback.

Maintained export produces `navigation-edges-release/BrineSpace.exe`, build `5760e46d67c3376b`, source SHA256 `5760e46d67c3376be1e3778fdf6c2dbd98d82d09e0aae590658521ded0a2459b`. PCK 3,646,719,192 bytes, SHA256 `8e836994a82219b878ca5d80b1840204a80a7f415e84ae65dca4ad61aa8f42c8`; EXE SHA256 `7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76`. Outside-checkout expected-hash audit: 36,288 checked, 55 remaps, zero missing/changed/unexpected. Patched Bill source is physically retained as `navigation-edge-candidate.gd`; frozen root's Bill is restored byte-exactly after export, so reconstruct that one input explicitly for another candidate build.

Actual debug=false original/fast three-cycle pair: 263 checks each, zero failures/errors/leaks/warnings. In each lane, 67,121 tested links agree with original collision checks across 76 geometry cells. All 12 recorded three-crew navigation graphs and complete crew snapshots match; texture counters exactly equal at all 12 endpoints. First large Continue 7706.106→6830.839 ms (~875 ms / 11.4% faster); later Continue 4920.447→5154.037 ms (mixed/slower). New Game 7221.239→7082.185 ms. First large restore still misses six-second gate. Largest loading draw gaps 343.878→303.790 ms on that restore; progress responsiveness acceptance remains open. One ordered local pair, OS cache uncontrolled; no FPS/memory/Mac/target-hardware certification. Both Continue captures inspected; not animation-motion acceptance.

QA now uses the new physical package in `qa-cold-hints/` with updated identity and `navigation-large-lifecycle.gd`; its name does not identify the build. Small and earlier large adapters retained separately. SHA256/recorded-identity verified old QA PCK duplicate removed before replacement; retained cold-hints deliverable unchanged (3.647 GB duplicate reclaimed). All owner checks retain 2,936 files unchanged, frozen Bill restored, and all processes terminal. No normal runtime source admission, upload or original release-gate closure.
