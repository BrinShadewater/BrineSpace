# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: active mission navigation rebuild census and indexed-link trial

## Objective and acceptance
Continue the full performance, bug closure and PC/Mac release plan. Preserve selected art, timing, owner layouts and saves. Require actual matched gameplay evidence before normal optimization admission. No itch publication.

## Accepted decisions and constraints
The prior warm-cache room ownership fix remains accepted. New indexed-link optimization remains private: exact graph parity and reduced CPU hitch alone do not establish net frame-pacing improvement. No mission delay, frame cuts, global downscale, renderer upgrade or broad refactor.

## Current state
Private evidence under D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/: transition-census/, indexed-links/, indexed-release/, indexed-reference/. Normal navigation source unchanged this trial. Indexed candidate caches local point-index link pairs, retains actual native point IDs, positions, weights and global maps, and avoids testing an already connected reciprocal edge. Original cached links retained. Pack overrides load before NPC compilation; all four actual base-script hashes verified. New physical bootstrap runtime copies and scratch profiles on D; maintained release EXE/PCK read-only.

## Verification
Actual diagnostic census reproduces pan2x frame126 at 251.916 ms: three 19,695-node crew rebuilds total roughly185 ms. Veld98.690/Branforth42.268/Marsh44.029 ms; point/link emission83.009/27.231/28.663 ms, cross-links about12 ms each. Stage instrumentation is attribution evidence, not acceptance timing. First source checksum rejected before gameplay due physical CRLF mismatch; corrected to hash written bytes, failed log retained.

Private exact reference/candidate test: 152,400 checks, zero failures over eight cold/warm mission/locked-door cases. Entire point-ID maps, owner geometry, positions, weights, sorted adjacency and exact selected paths compared. Headless CPU timings are diagnostic only; cold first-case savings include asymmetric cache warm-up.

Actual debug=false native 1080p, 40 rooms/four crew/three natural non-synthetic missions, 9x180 idle/pan/zoom at1/2/4x. Candidate then fresh reference (reverse order to retained baseline): both clean, every mission launches, full mission snapshots/history/resources equal, per-phase crew/drone/doors/lights/power/zoom equal. Uploads2,334 each; exit228.259 MiB each; peaks reference2,346.158/candidate2,346.352 MiB. Compiled hashes guard exact code execution. Same pan2x/frame126 hitch: reference249.749/candidate216.895 ms; crew192.335 to149.509 ms, step194.022 to150.203 ms, engine wait55.697 to66.665 ms. Rendering timers disabled (unavailable, not zero cost). Means worse all9 phases; p95 better3/9, no net acceptance or release certificate. Separate candidate idle4x112.195 ms stall remains. Candidate prop live_draw/advance cumulative counts diverge +66/+12 beginning idle4x; other compared prop fields equal. This is an unresolved visual/clock sampling difference, not silently closed by mission equality. Historical zoom-counter issue remains separately open.

Comparison recorded indexed-release/comparison.json. Owner fingerprints2,936 files unchanged in both runs; adapters restored; engine logs no error/warning/leak/missing art; all measured processes terminal. No owner saves written.

## Next action
Moonbay _route_to_point unconditionally actor.rebuild(game); Main mission branch continues before normal one-crew-per-frame rebuild budget. Investigate safe reuse or a smaller graph for pressure-cycle trips within the same bay, proving exact route/geometry and topology invalidation semantics. Do not merely stagger gameplay or retain an unsafe stale route. Indexed candidate may be composed only after stronger net evidence; first address dominant unnecessary graph scope. Separate drone texture upload stalls remain. Combined physical exports, all original packaged bugs, full workloads/loading/memory/endurance, GTX1650/M1, Mac signing/notarization/Gatekeeper and full release certification remain open.
