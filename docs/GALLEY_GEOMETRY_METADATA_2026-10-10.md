# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: geometry-only legacy prop templates

## Objective and acceptance

Continue the full PC/Mac performance/release plan. Remove unnecessary first-room
image work without changing selected pixels, geometry, navigation, gameplay or
historical fallback art. Full release gates remain open.

## Accepted decisions and constraints

Keep the geometry-only serving template in normal galley setup. Existing
`RoomAssetLibrary.template()` remains the complete, textured API. Metadata requests
derive exactly the same registration/prop fields, retain their original template
ID and obtain the original shared image if later drawn as a library prop. No art
deletion, downscaling, new renderer or gameplay change. Muted secondary-display
tests, isolated profiles, unchanged owner saves and shared physical QA runtime.

## Current state

Changed `scripts/room_asset_library.gd`: one shared template assembler with complete
and metadata-only entry points and separate cache keys; on-demand image resolution
in `draw_base` for metadata props. Existing complete template calls retain their
original lookup/decode/worker behavior. Changed galley rebuild to request metadata
for its inherited serving prop, which live current layouts filter out.
`scripts/session_art_cache.gd` clears the metadata cache at final owner release.
Extended existing `tests/test_galley_lazy_art.gd`; its paired UID remains unchanged.
No new packaged delivery, commit or upload. Frozen PC/Mac packages still omit these
later source optimizations.

## Verification

Current-galley resource census job78235: cold geometry48.282ms; old serving template
18.107ms, four selected station templates1.5–1.8ms each, visible floor23.275ms and
wall18.471ms in the action frame. Navigation points/links remain ~3.3ms. Floor is
already RGB; wall requires alpha. Neither offers a useful exact smaller-format
conversion. No asset conversion performed.

Reported12 actual debug=false comparison4412: four runs/4,320 measured frames,
placement/demolition at1x/2x/4x, owner layouts copied. Twelve phase-end states equal.

| Metric | Forward textured / metadata | Reverse textured / metadata |
| --- | --- | --- |
| First1x placement |149.946 /131.994ms|151.965 /137.308ms|
| Step in that frame |69.325 /52.031ms|69.691 /53.243ms|
| Overall mean |14.686 /14.673ms|14.670 /14.669ms|
| First phase texture counter |1580.843 /1574.845MiB|1580.843 /1574.845MiB|
| Frames >100ms |1 /1|1 /1|

Normal galley/library files are byte-identical to the measured candidate. Subsequent
cleanup change only adds final-owner metadata release and has native coverage.
Native original/current prop checks56/56 byte-exact: four rotations, power states,
overhead art, original PNG fallback and direct library drawing after a metadata
request. Cold candidate setup uploads no serving source; metadata matches complete
prop fields apart from the image and resolution ID. Pixel harness initially bound
a cached old library; owned failed native process164956 stopped, corrected explicit
same-library bindings pass. Failure evidence retained, owner guard unchanged.

Maintained normal test: intended missing-API red demonstrated after correcting a
preparation parse error; normal green24checks/0failures. Covers original14checks,
metadata geometry, absent-source behavior, cold upload avoidance, overlapping-owner
retention, final-owner cache release and exact next-session image reload.
Existing session-art test26checks/0failures. Existing galley native gameplay passes
paid construction, deck/entrance, save/Continue, hungry crew/meal behavior, frozen
time/suspension,104 continuous route samples and three viewport sizes. Guarded
copies add only profile/mute/window controls to those existing fixtures.

Current final-source40-room comparison17662: four actual debug=false runs/
4,320frames, same actions/speeds, twelve phase-end states equal. Mean27.732->27.499ms
forward,27.580->27.524ms reverse. P95 improves38.380->36.652 /37.336->37.047ms;
p99 mixed54.559->56.791 /58.334->53.037ms. Six >100ms frames remain every run.
Phase texture peak2788.218->2782.220MiB in both orders. These endpoint counters do
not replace earlier per-frame peak evidence. Small average differences are not a
robust general FPS claim; the accepted benefit is unnecessary loading/storage removal.
End capture inspected, but its stabilized-pattern popup obscures part of the station;
not complete moving-station visual acceptance. Fixture deliberately advances active
simulation and resets pause each step; this does not certify interactive pause/input.

All engine/art/input/profile guards clean in successful comparisons. All full owner
fingerprints2,938 unchanged. Configurations/fixtures restored, jobs terminal. Latest
free C124.35GiB/D81.23GiB. Small overlays/reports and bounded end captures only; no
full PCK/source copies or unbounded screenshot output.

Evidence in `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`placement-resource-census/resource-analysis.json`, `channel-feasibility.json` in
that folder; `galley-metadata-performance/paired-analysis.json`,
`galley-metadata-pixels-v2/results.json`, `galley-metadata-normal-red-v2/`,
`galley-metadata-normal-green/`, `galley-metadata-test_session_art_cache/`,
`galley-metadata-test_galley/`, `galley-metadata-large-performance/paired-analysis.json`,
and `galley-metadata-large-inputs/identity.json`. Exact drivers/private sources retained.

## Next action

Investigate bounded preparation of required floor/wall images before the first
interactive placement, including actual selection/hover/preview behavior, without
incomplete rooms or changed gameplay timing. Preserve the current cold direct-action
stress workload. Large-map visible drone upload bursts remain a separate priority.
Continue full original bug/UI/input, endurance, target-PC/Mac native, frame/stall/
memory, packaging/signing/notarization gates. No itch publication.
