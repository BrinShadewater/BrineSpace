# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: attribute slow drawing frames and test zoom settling budget

## Objective and acceptance

Continue the full PC/Mac performance and release-readiness work. Preserve selected art, simulation, owner layouts and saves. Admit optimizations only after matched performance and relevant visual/behaviour checks; no publication.

## Accepted decisions and constraints

The previous response was an owner-requested status update, not a performance milestone. This pass analyses the completed diagnostic and creates a tested private scheduling candidate. No normal runtime or art changes. Actual changes must still repaint immediately; size-only cached layers may wait while their existing commands scale. Existing preparing-camera behaviour remains intact.

## Current state

Detailed actual-release diagnostic has 1,620 current-frame traces. Idle/pan median grid callback sums are about 12.5–12.9 ms; zoom4x median 17.825 ms. Callback sums can overlap; renderer signal intervals (~11 ms) are wall time, not GPU timing. Slow zoom2x72 is 91.437 ms with 43.914 ms grid callbacks; zoom4x103 is83.736 ms with55.683 ms callbacks. Floors, wall slots and room preparation rise during these slow frames. Nested category labels must not be summed.

Private key-cause probe records below145/foundations121/terrain3/derelict4/floor2/wall2/doors240/lights2 stale-key events. All floor/wall stale-key events occur at startup process_frame1: the measured gameplay floor/wall rebuild bursts arise from size-only settling, rather than a demonstrated new structural room mutation in this workload. Environment cover changes and door state changes remain real dependencies.

`_flush_retained_layers` groups walls, rear/front doors and lights. During settling, a changed door makes the entire due group urgent, including siblings that changed only size; these can execute after the floor group has already spent the frame's size-rebuild budget. Private candidate partitions these later groups: pending real changes execute immediately; size-only siblings retain the backlog and wait their turn. Preparation and non-settling behaviour are preserved.

## Verification

Native scheduling test: original12checks/3failures (size-only wall/front-door/light piggyback); candidate12checks/0failures. Checks include immediate changed door, actual floor/wall changes, backlog, pending-marker consumption, preparation hold and normal work. This is scheduler verification, not rendered-art parity.

Single matched uncaptured actual `debug=false`40room/fourcrew9phase pair: candidate285 deferred sibling submissions, control0, so the changed branch executes. All compared crew/drone/door/light/power-count/zoom states and prop counters equal in every phase. Peak2348.739303MiB/exit228.259212MiB/uploads4297 equal. Clean logs, focused samples, released router. Native/readiness owner fingerprints2936files unchanged, physical adapter restored byte-identically; all runners/engines terminal.

Matched zoom slow points: 2x/frame72 82.658→73.872 ms; 2x/frame132 77.187→66.534; 4x/frame43 78.151→55.756; 4x/frame103 86.410→61.324; 4x/frame134 78.909→58.973. These are single-pair observations, not robust gains. Whole zoom p95:1x52.265→52.199;2x50.723→53.575;4x56.725→58.738 ms. Zoom means1x37.444→37.459;2x39.872→40.557;4x41.137→42.080. Work moves into other frames, and aggregate performance is mixed/still fails. Do not admit or call this an FPS improvement yet. The1x76 control85.242→candidate30.576 observation has essentially unchanged before-render interval; do not attribute that separate renderer-interval outlier to the scheduler patch.

Final candidate screenshot inspected: station floors/walls/props and UI present. This single still does not certify settled pixel parity, intermediate motion, original bug closure or release visuals. Full packaged regressions/three measured pairs/endurance/target PC/M1/signing/notarization gates remain open.

Evidence: `output/renderdoc-tools-2026-10-08/{draw-work-probe-categories,key-cause-probe,settle-budget-native,settle-budget-release-trial}` and corresponding source generators, analysis/comparison helpers, immutable pack identities and owner records. Initial draw-work probe deliberately stopped after discovering total timing lacked category snapshots; corrected category probe completed. Failed partial log preserved, adapter/owner restored.

## Next action

Keep the scheduling candidate private. Check actual settled visual convergence and repeated performance before considering admission; reduce total drawing/preparation cost rather than relying on work redistribution alone. Full objective remains active. Drive now reports only78MiB free: avoid full exports and large repeated reports until a verified disposable duplicate/cache can be reclaimed. Do not delete selected art, archives, retained packs, captures or physical frozen sources to make space.
