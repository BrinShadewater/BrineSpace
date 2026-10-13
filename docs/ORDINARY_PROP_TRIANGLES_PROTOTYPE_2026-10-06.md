# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: ordinary prop combined submissions prototype

## Objective and acceptance

Reduce regular renderer work with unchanged selected art/order/filter/materials/cache lifetime. Full PC/Mac release/performance scope remains active.

## Accepted decisions and constraints

Private only; normal source unchanged. Extend already verified float-color indexed body/shadow geometry to ordinary unsplit library prop slots, then draw original live content in original order. Exclude portable/custom/drone-dock/aquarium paths. Reuse slot-owned immutable geometry, clear hidden/unused/reclassified caches; no new images, materials, nodes, global caches or art changes.

## Current state

output/ordinary-prop-triangles-2026-10-06/content.gd/private probes/reference and candidate physical fixtures. Candidate Grid and copied large-room Contents explicitly preload private content; reference normal content. Both use same six-source private drone/crew fixture. Positive ordinary-build/draw/holder assertions prevent unused candidate acceptance. Source hashes, native logs, art/cache receipts and station-results/verified.json retained.

## Verification

Saved native quiet1x trace triage (56idle+56pan samples) median~41.4/41.7ms; explicit simulation~4.17ms, after-step-to-render-pre~22.12ms, render signal interval~14.8–14.9ms, renderCPU~14.4–14.6/GPU~13.4–14.0ms. Signal/stage intervals overlap; not an additive complete CPU/GPU decomposition. Source summary output/steady-frame-triage-2026-10-06/summary.json.

Private native26cachechecks/12exacttransitionpairs pass (9geometrybuilds), plus96exactnonblank current-art pairs/12distinctsources across registration mirrors, nearest/linear and dry/flood material. Actual candidate branch executes48basecallbacks (material changes reuse retained commands). Selected capture inspected, original/candidate captures retained. Existing full-room ordering/composition coverage for this added unsplit branch still needed. Later eligibility cleanup also clears stale arrays when a prop becomes portable/custom/drone/aquarium; no claim those fallback subclasses have new visual tests.

Initial private inferred bool failed parsing and a probe ran into invalid construction; explicitly stopped only that failed process, owner unchanged. Corrected explicitbool before successful tests. Initial station reporter mixed spaces/tabs, exited parseerror; corrected before matched measurements. Failed logs retained; no normal/runtime bug claim.

Matched native mixed40room six60sample phases idle/pan1/2/4x. Fullcrew/drone/door/light/power/zoom snapshots and every texture endpoint identical. Candidate157ordinary geometry holders,157→164builds/667→679callbacks, demonstrating stationary reuse and actual execution. RendererCPU lower allsix by0.95–1.77ms; ~460.5–463reported draw calls removed. GPUmeans lower~0.48–1.42ms with normal variability. p95reference→candidate:47.904→45.434,48.790→46.483,45.205→44.935,48.811→46.263,56.502→50.635,55.808→55.004ms. Onepair/not universalFPS or release acceptance, still far above16.7ms. Texture end2776.236MiB identical/private scene/no memoryclaim. All successful native logs clean, all owner2936files unchanged, processes terminal.

## Next action

Validate actual full LIVE composition with neighboring rooms/core and excluded-class cache cleanup, then install narrowly in normal source with paired UID/permanent native regression coverage and actual-normal execution checks. Preserve existing split-library behavior and comparison paths. Continue remaining~22ms preparation/~15ms backend attribution and six-sheet drone Main lifecycle before normal admission. Release target hardware, normal texture/loading budget, packaged original bugs/endurance and Windows/Mac certification remain open.
