# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: learned room-source prefetch

## Objective and acceptance

Replace fixture-specific image prediction with runtime discovery and improve loading without worsening warm behavior, pixels, state, memory bounds or cleanup. The complete original PC/Mac performance/release plan remains active.

## Accepted decisions and constraints

Reject schedulers without measured gains. Keep normal source and retained release packages unchanged. Metadata may hold bounded source paths, never images or room objects. Tests use verified scratch profiles and fingerprint the real owner data. No release upload authorized.

## Current state

Private six-file prototype captures lazy-view source requests, binds room IDs to source groups, persists bounded metadata at final session-owner exit and clears lookup tables. It learns from runtime construction/placement/Studio instead of reading the observed fixture list. Sources, backups, runners and logs live under `output/drone-compiled-2026-10-07/learned-room-*`. Candidate six existing scripts and Bill are restored byte-exactly afterward; RunSave instrumentation restores independently. Normal runtime source unchanged.

## Verification

- Initial corrected learned-list native pair: 262 checks each, no failures/engine errors/leaks/warnings; all 12 complete crew snapshots and texture endpoints match. Learns 15 room IDs / 12 source groups and predicts 75 paths. First large Continue 7946.795→8106.023 ms and Veld restore1837.225→1997.386 ms regress. Later5765.201→5670.031 ms mixed. Whole decoded peak equal at95,415,252 first /110,421,636 later bytes. Flat learned-batch scheduler rejected.
- Out-of-order recovery variant: 262 checks each, clean; all12 crew/texture endpoints match. First large Continue7876.793→8305.389 ms, Veld1814.881→2108.554 ms regress. Hits12673→12677, first unused76→46, peaks equal; joining/discarding speculative jobs consumes the benefit. Later5619.823→5636.598 ms mixed. Recovery scheduler rejected; no export/admission.
- Metadata-only unit suite: 11 checks pass with no errors/warnings after fixing corrupt-JSON handling. Covers nested capture, deduplication, path validation, selected-room lookup, persistence/reload, empty observations, stale replacement, per-group overflow, damaged and oversized data, atomic schema rejection and exit cleanup. Uses `JSON.new().parse` so a malformed optional cache falls back without an engine error. Initial unit logged one parse error; failure evidence retained. An initial candidate-file encoding failure was corrected to explicit UTF-8; failed evidence retained.
- Every owner fingerprint comparison retains2,936 files unchanged. All processes terminal. These are private native trials, not package, FPS, GPU-memory, Mac or target-hardware acceptance.

## Next action

Learn actual late PNG requests after startup and carry their order into the ordinary next-load prefetch, rather than replacing it with all declared room sources. The learned75-path list overpredicts the actual52-call geometry stream; generic scene dependencies do not establish request order. Preserve complete trained orders, bound metadata/worker memory and test new rooms, repeats, cache expiry/corruption, first and warm loads, actual pixels and packaged behavior. Continue independent navigation-edge admission, title-retained memory, gameplay frame pacing and all original release requirements. Accepted navigation package5760e46d67c3376b and prior measured gains remain unchanged; neither rejected scheduler is a release candidate.
