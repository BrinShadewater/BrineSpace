# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: actual late room request scheduling

## Objective and acceptance

Improve full PC/Mac release performance while preserving pixels, state, bounded resources and warm loading. Admit only measured useful changes; full original release gates remain active.

## Accepted decisions and constraints

Normal source and retained packages unchanged. Private actual-request metadata captures only PNG requests from late lazy room construction, deduplicated/capped at256 paths, with bounded optional JSON parsing and scene-exit table release. No fixture source list, permanent image cache, art reductions or upload.

## Current state

Three-file prototype/backups in `output/drone-compiled-2026-10-07/late-room-order-{candidate,before}/`; runners and two native original/fast comparisons retained as `late-order-*` and `late-independent-*`. Frozen Grid/Prefetch/SessionArtCache/Bill and temporary RunSave edits restore byte-exactly. Retained navigation package5760e46d67c3376b unchanged.

## Verification

- Appended late-path tail with four-path lookahead:262 checks per lane, zero errors/leaks/warnings; all12 crew snapshots/texture endpoints match. First large Continue8116.775→8284.868ms, Veld1840.351→1901.214ms; later5653.498→5802.222ms. First hits12673→12654 despite25 learned additions. Jumping to appended indices disrupts earlier still-needed request scheduling; rejected.
- Independent four-job hint queue preserves the ordinary path index/cursor. Negative result slots separate hint results from ordinary jobs; required images still use the identical PNG decoder.262 checks each clean, all12 crew/texture endpoints match. First large Continue7999.464→8015.138ms, Veld1841.207→1820.952ms; later5602.734→5736.750ms. Hits12673→12695, but unused76→83. First decoded peak95,415,252→113,333,121bytes; later110,421,636→134,010,816bytes. No useful loading gain, resource/waste regressions; rejected.
- Native local ordered pairs only; no packaged/FPS/memory/hardware/Mac acceptance. Owner2,936 files unchanged in every comparison. All processes terminal and sources restored.

## Next action

Deprioritize further room-prefetch scheduling microtrials: actual room requests are known but prediction/queue changes have not improved total loading. Preserve demonstrated cold-hint and local-edge packaged gains. Investigate retained navigation/room resources at settled title states, particularly the prior large-lifecycle texture increase, without forcing lazy texture materialization or GPU readbacks. Complete edge fallback/layout admission, combined compressed-provider memory/rendering acceptance and remaining original gameplay/bugs/endurance/PC/Mac release gates.
