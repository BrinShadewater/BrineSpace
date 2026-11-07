# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: normal indexed prop body/shadow submissions

## Objective and acceptance

Reduce measured renderer submissions with exact selected appearance, ordering, filtering/materials and scoped resource lifetime. Full PC/Mac frame/memory/loading/bug/endurance gates remain open.

## Accepted decisions and constraints

Existing library_base slots submit ordered shadow/body triangles together using float colors and original geometry/UVs. Live effects remain separate. Per-slot cache replaces on artwork changes, releases on hidden/unused/reclassified slots and dies with scene owner. No global image/cache table, art/atlas/engine/animation/quality changes. Internal `--separate-library-bases` preserves original comparison path; no user quality option.

## Current state

Normal `scripts/room_content_canvas.gd` integration and new `scripts/library_base_triangles.gd` with paired UID. Permanent native `tests/test_library_base_triangles.gd` and `tests/test_library_triangle_cache.gd`, paired unique UIDs/native render-perf index. Existing large-room test retained.

## Verification

Actual normal-source native160 exact synthetic/current-art image pairs, zero failures; eight current source sheets, filtering/scales, alpha, concave overlap, mirrors, floor classification, inherited modulation and flooding material. Native26cachechecks/12exact transition pairs cover stable reuse, move/resize/mirror/pieces/texture/floor changes, hide/unhide/empty/restore, reclassification and observed owner release. Synthetic fixture initially omitted cached layout_flip and produced Store type errors despite pixel comparisons; corrected fixture matches actual props and clean result is authoritative. Native135large-roomchecks/80exactpairs also pass. UID uniqueness and whitespace checks pass.

Private new-helper actual mixed-station LIVE comparison12exactpairs passes with40room bounds/248ordinaryslots/activeBRINE signals. This excludes omitted floor/wall/foreground passes and actual Main demolition/save. Normal helpers retain the same tested drawing path plus cache-release cleanup.

Installed normal modules in matched physical mixed40-room pair, idle/pan1/2/4x,60samples each:40executingcanvases,146retained geometry holders,151→162builds/251→266base callbacks. Report guard initially required prototype's147minimumholders, rejecting completed clean candidate because cleanup removed unused holders. Corrected guard checks40canvases,positiveholders/draws andbuilds>=holders; recovered existing successful native output without rerunning. Failed runner log retained; no game or source fix was needed for that threshold.

Renderer CPU lower in all six phases by0.77–1.08ms/frame; reported draw calls lower~427–430; GPUmeans lower0.38–0.84ms with normal measurement variability. Full crew/drone/door/light/power/zoom state andtexturecounters equal everyphase, final3036.131MiB/no memorysavingclaim. Whole-frame p95 lower at1x/2x, but4xidle59.698→62.617ms and4xpan59.914→62.401ms regress. Candidate range45.19–62.62ms stillfailsreleasegates. Two scoped comparisons establish renderer-cost benefit, not universalFPS or three-run packaged acceptance; investigate4xframe pacing/system work separately.

All successful native processes clean/terminal; everyrun2,936ownerfiles unchanged. Private compressed crew/drone/debug=true fixture limitations remain. Evidence `output/prop-triangle-submission-2026-10-06/{integration,cache-check/hidden,normal,normal/station}`. No export/Windows/Mac certification in this admission.

## Next action

Measure remaining regular static library prop submissions, which currently retain original body rendering, and investigate4x simulation/frame stalls before widening combined geometry. Preserve original custom/portable/drone paths and exact body/effect order. Continue actual renderer/system/memory work and full release certification; do not count local renderer savings as frame-gate closure.
