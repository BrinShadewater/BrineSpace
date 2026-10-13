# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: zoom scheduling reported/current map verification

## Objective and acceptance
Verify the installed zoom-group scheduling fix on real reported/current station inputs. Continue the entire PC/Mac performance/release plan; passing this scope does not meet release gates.

## Accepted decisions and constraints
Muted secondary display, isolated profiles and owner fingerprints, shared debug=false runtime. Preserve visuals, gameplay, owner layouts/saves and UIDs. No runtime copies or screenshots. Frozen current checkpoint still byte-matches the owner's actual brine_loop.save after tests (read-only SHA check).

## Current state
No production logic changes during this verification. Installed grid_canvas.gd still exactly equals the measured scheduling candidate. Runner/analyzer: output/renderdoc-tools-2026-10-08/run-zoom-group-scheduling-other-maps.py and analyze-zoom-group-scheduling-other-maps.py. Evidence: D:/bs-release-crew-cache-20261009/benchmark-input-isolation/zoom-group-scheduling-other-maps/{comparison.json,zoom-comparison.json,input-saves.json,identity.json,completed.json,owner.json}.

## Verification
Twelve native debug=false runs, three alternating before/after pairs per station, 12,960 frames. Twelve phases each: idle/pan/selection/zoom-selection at 1x/2x/4x, 90 frames each. Reference is hash-verified pre-change grid; both lanes otherwise identical. All 72 full phase states/cameras and 324 UI snapshots exact. No engine/script errors or missing art. Input disabled; muted secondary confirmed in every report.

| Metric | Reported before → after | Current before → after |
|---|---:|---:|
| Whole mean ms | 12.196 → 12.108 | 12.300 → 12.152 |
| Whole p95 ms | 17.566 → 17.888 | 20.282 → 19.979 |
| Whole p99 ms | 26.495 → 25.918 | 30.701 → 28.323 |
| Whole maximum ms | 40.421 → 32.371 | 49.863 → 49.826 |
| Zoom mean ms | 13.648 → 13.765 | 13.421 → 13.306 |
| Zoom p95 ms | 25.659 → 24.677 | 24.407 → 24.213 |
| Zoom p99 ms | 35.397 → 29.137 | 31.208 → 28.323 |
| Zoom maximum ms | 40.421 → 32.371 | 42.183 → 34.141 |
| Texture peak MiB | 1559.506 → 1559.506 | 1945.262 → 1945.262 |

No frames >50 or >100 in either map/lane. Reported whole mean -.716%, all three pairs better; current -1.207%, mixed (one pair worse). Small average gains; keep claim scoped. Reported zoom mean slightly worse, despite lower tails. Zoom p99 -17.7% reported /-9.2% current. The prior large station zoom p99 reduction remains separate measured evidence. Both maps still fail whole p95≤16.7 and p99≤25; averages alone do not certify 60 FPS. Texture budget fits these sampled settled workloads; no long-term/driver VRAM certification.

Owner fingerprint 2938→2938 unchanged. Native jobs terminal/shared override restored. Evidence 33.64 MiB plus scratch 33.83 MiB retained, no runtime/art copies or captures. Free C122.30/D69.05 GiB. No broad retesting beyond the new scheduling change.

## Next action
Exercise lighting, connected placement and demolition through actual gameplay methods with explicit action-success labels, so blocked demolition cannot masquerade as coverage. Compare current/large matched states and structural visual behavior for the changed urgent scheduling. Existing maintained live-surface regression/visual test already passes, but these other release workloads are not covered by these twelve-phase runs. Then continue repeated-image upload remedy and true native endurance/loading/bug/UI/hardware/Mac/signing/package work. Do not repeat unchanged larger-cache/indexed/cropping trials or substitute this scoped acceptance for the original release plan.
