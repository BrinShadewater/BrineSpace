# Crew animation polish

Updated September 27, 2026. **Candidate work; not installed in the game or exports.**
Review: http://127.0.0.1:8791/character/crew-polish-v1/

## Consistency audit — September 27

The new [style review](style-review.html) and [findings](review/style/REPORT.md) cover
5,301 body-frame references. Export density matches; crew palette/detail/anatomy
consistency remains unresolved. The colour V3 pilot is rejected, not selected.

## Current candidate

Veld now has a matching painted core in all four directions: idle, walk, kneel,
sample inspection (`repair`), and stand. Twenty body states contain 100 frame
references; the fitted diving-helmet pack matches all twenty states and 100 slots.
The source art follows the current visual bible: matte industrial materials,
muted cobalt/charcoal/ivory, mature brown-skinned female face and silver-streaked bun.
Larger authored sources are downsampled once; no source is enlarged. New source
prompts and raw outputs are retained in `sources/`, with selections/rejections in
`selection-v2.json`. Final exports use normalized transparent RGB and binary alpha.

`veld-painted-v2/manifest.json` and `veld-painted-v2-helmet/manifest.json` are the
current candidate pair. Walks remain six poses; idle uses three, lowering/rising
five, and sample inspection six. Stand reverses the authored lowering sequence.
Sixteen body and sixteen equipped endpoint joins are exact. This does not make
intermediate movement smooth: sample retrieval is abrupt and the walk needs more
coherent intermediate poses. Other production actions still use the earlier style.
Do not install this subset over the production library until those joins are resolved.

The browser provides individual states, a complete sample-action sequence,
candidate equipment, four facings, gameplay/2x/4x scale, speed, pause and stepping.
The current-game column is bare-headed even when the candidate helmet is selected.

## Earlier motion studies retained

`motion/` contains twelve Veld/Branforth/Marsh directional cycles: 289 recovered
video frames. All 72 original sampled poses and cumulative timing boundaries are
preserved exactly. These add motion samples, not painted detail. `veld-study/`
is the superseded first 24-pose surface study. Bill south V1 remains unselected
because its gait repeats contacts. The frozen baseline covers 724 body states and
4,413 frame references, not every runtime-composed join or equipped state.

## Build and verification

From the repository root:

- `python character/crew-polish-v1/build_veld_painted.py`
- `python character/crew-polish-v1/build_veld_equipment.py`
- `python tools/run_margot_check.py crew-polish-candidate -s tools/review_crew_polish.gd`

The existing isolation wrapper is reused despite its historical Margot name. It
sets scratch APPDATA and fingerprints the real profile before and after execution.
The native run passed **236 checks**, with 24 rendered capture frames; all real
profile files were unchanged. Checks cover actual sprite-player phase selection,
paired equipment, exact joins, pause and snapshot restore. All 200 candidate frame
references pass dimensions, binary alpha, transparent RGB and clipping checks.
Body pixels below the collar are preserved in every equipped export. PNG paths
resolve to Git LFS. JS syntax and selected browser action/equipment/facing controls
pass, with no browser console errors. Production catalog/pixel baseline is unchanged.

Evidence: `review/painted-checks.json`, `review/native/checks.json`, the contact sheets,
and `review/painted-browser.png`. Native logs/profile fingerprints are under
`output/margot-polish-native/crew-polish-candidate*`. Selected source-scale and native
poses were visually inspected; this is not complete temporal or room-contact acceptance.

## Remaining work and blocker

A Seedance 2.5 continuous-motion attempt was rejected by Higgsfield with
`not_enough_credits`; no job ID or video was returned. Its exact reference/prompt
and failure record are preserved. Do not silently retry or mark it generated.
Continuous video generation through that provider is blocked until credits are
available; this is not a blanket blocker on static source edits or local review.

Finish gait in-betweens and explicit sample retrieval, reconcile the remaining Veld
action endpoints, then extend the accepted direction to Bill, Branforth and Marsh.
Verify actual room contact/occlusion and full temporal quality before production
selection. Existing denser motion studies alone do not satisfy the requested clarity
and consistency cleanup. Full cast cleanup and in-game integration remain unfinished.
