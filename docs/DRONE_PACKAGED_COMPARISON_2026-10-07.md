# Packaged drone optimization comparison

Updated: October 7, 2026 · Project: BrineSpace · Task: PC/Mac performance and release readiness

## Objective and acceptance

Preserve selected pixels, animation behavior, saves and owner layouts while reducing drone upload stalls and memory. Accept optimizations through matched measurements and relevant regressions. Entire original release plan remains scope; this comparison does not certify release.

## Accepted decisions and constraints

Experimental frozen candidate only; no accepted checkout admission or public upload. Keep original text-script preset, normal crew/flood code, selected quality, PNG runtime loading and threaded Main. Prepare eight small helper scripts between rendered loading-screen frames; no whole-scene synchronous workaround. Owner files and previous packages remain preserved.

## Current state

Evidence: `output/drone-compiled-2026-10-07/`. Patched candidate `brinespace-66929cd10addc5b0`, source SHA256 `66929cd10addc5b0893a72001babde776e402e22244674fdb2c5c93f929f4cca`. Maintained export: EXE109,283,328 / PCK3,646,715,704 bytes. Broad outside-checkout audit: **36,288 checked, zero missing/changed/unexpected, 55 loadable remaps**. Selected original source, notices and runtime PNGs accounted for.

Actual packaged New Game/Studio/save/title/Continue fixture contains **no helper prewarm**: preparation comes from the packaged loading screen. **142 checks, zero failures/leaks/warnings**, full crew/fleet restoration and weak owner/factory/job/cache release. Two small cycles only; not large-station endurance or broad input/menu certification.

Loading render-gap trace remains concerning: automated intro/Continue flows12.781s /5.157s, p95 draw gaps123.544 /227.825ms, maximum1054.162 /1714.553ms;76 /23 gaps over100ms. Fixture skips typing and disk cache is uncontrolled. Scope includes scene setup, required actor/art loading and dismissal, not isolated helper preparation. The new helper loading fix closes its warning in this flow but **does not certify responsive loading or cold/warm gates**. Attribute existing larger stage pauses next.

## Verification

Three matched actual debug=false1920×1080 mixed40-room pairs, idle/pan at1×/2×/4×,60 measured frames per phase:1080 samples per lane. Every one of18 full crew/fleet/door/light/power/zoom state comparisons matches; all complete crew/room resource records and live/expired counts match. No missing art, selected ordinary duplicates, engine errors, exit warnings or leaked-object diagnostics in six gameplay processes. Final candidate capture inspected; prior1516 exact dock/room pairs retain their recorded source/native scope, not an additional packaged motion-pixel certification.

| Workload | Baseline median p95 | Candidate median p95 |
|---|---:|---:|
| Idle1× |34.222ms|35.221ms|
| Pan1× |35.803ms|37.779ms|
| Idle2× |33.930ms|33.797ms|
| Pan2× |35.889ms|36.167ms|
| Idle4× |51.030ms|39.373ms|
| Pan4× |47.946ms|41.734ms|

4× improvement repeats in all three pairs; earlier phases mixed. Median4× p99 idle59.777→45.458ms /pan73.702→47.767ms. Frames>50ms baseline8/7/7 versus candidate0/0/1 (22→1 total). No sampled frame>100ms; sparse360-frame runs per candidate do not prove absence of reproducible stalls in all required actions.

Texture endpoint changes identical across pairs:−61.04,+31.04,+30.97,+30.97,−397.68,−350.38MiB. Final4389.85→4039.47MiB (**about3.94GiB**, still above3GiB budget); no blanket counter calibration adjustment or physical VRAM claim. Ready timing8.9s is direct-gameplay/cache-uncontrolled scope, excluding dialogue; not loading certification.

The first comparison script incorrectly expected top-level inventory aliases. Actual detailed inventories were already collected under `texture_inventory.crew/rooms`. Preserved failed comparator; corrected **postprocessing only**, verified the existing pair's complete matching records and resumed pairs2/3. No repeated first workload or evidence fabrication. Raw reports/images/identities/fingerprints retained.

Remaining candidate54.019ms hitch (third pair, idle1× frame28): latest recorded upload frame207 predates corresponding drawing frame209; no coincident recorded drone upload. Simulation3.969ms, rendering CPU10.807/GPU9.554ms. Boundaries before-render18.805 /render-signals12.582 /after-render18.645ms, callback aggregate28.789ms/178 callbacks (not178 complete grid rebuilds). Intervals overlap; no summed cause claim. `remaining-hitch-attribution.json` preserves trace. Increased post-draw/process interval still unexplained; investigate without blaming stale upload metadata.

All2936 owner files unchanged; every subprocess terminal. Current normal checkout art/logic unchanged by this trial.

## Next action

Complete provider production/source/encoding validation and actual packaged motion/fallback coverage before normal admission. Prioritize steady rendering/preparation (p95 still34–42ms), large loading gaps and the remaining hitch. Keep the matched candidate as the measured reference rather than reopening rejected cache/token experiments without new evidence. Expand required fresh/reported12/large scenes, zoom/placement/demolition/lighting/UI,1440p, endurance, original reports, target hardware and Mac/signing checks. FPS/p99, memory, responsive loading and full platform gates remain open. No release upload.
