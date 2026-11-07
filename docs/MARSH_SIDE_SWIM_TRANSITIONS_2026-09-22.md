# Marsh side swim transitions handoff

Updated September 22, 2026. Project: Brine Space.

## Objective and acceptance

Connect Marsh's existing tread/swim poses with visible starts and stops. Prove a
representative pair before extending coverage. This pass completes east and west;
north/south and all carry/swim turns remain open. Owner visual acceptance remains
separate from source, playback and route checks.

## Accepted decisions and constraints

No Higgsfield, room edits, gameplay-speed changes, publication or new export.
Two independent directional sources were generated with the built-in OpenAI
image tool. West is not mirrored from east. Raw PNGs and exact prompts are saved
under `character/marsh-swim-transitions-v1/sources/` with frozen current endpoints.

## Current state

Four clips installed: swim-start/stop-east and swim-start/stop-west, five frames
each. Each start uses three new intermediate poses between exact current tread
and swim frame-zero endpoints; each stop reverses that authored sequence.
Durations are 60/90/100/90/60ms, totaling 0.4 seconds. Registration uses measured
shoulder landmarks and fixed 0.24 source scale, not a floor/foot anchor.

`tools/build_marsh_swim_transitions.py` reproduces and optionally installs them.
`tools/rebuild_marsh_art.py` reinstalls both supplements during canonical rebuild.
East canvas is 184x184; west uses 184x208 transparent padding so diagonal feet are
not clipped. Both retain pivot 92,172 and standingHeight 148. Existing endpoint
pixels remain unmodified, including west's padding-only adaptation.

Runtime additions: 20 PNGs plus two manifests and two provenance files in
`character/marsh-v2/supplemental/swim-{east,west}`. Only existing catalog.json and
clearance.json changed; no existing runtime PNG changed. The derived lower
clearance grows by 4.41 world units east and 9.26 west; width/top stay unchanged.
The historical helmet envelope also updates, but no helmet art or ability is added.

Supplemental contracts record new pixel hashes and water metadata. The pack test
now checks each supplement's declared medium, retaining dry defaults for older
ground supplements. Preview: `character/marsh-swim-transitions-v1/review/sides.gif`.
Its endpoints are held longer for inspection; runtime duration remains 0.4 seconds.

## Verification

- Two Python tests pass for all 20 reconstructed frames, binary alpha, profiles,
  timing, exact existing endpoints and reversed stop sequences.
- Human crew validator: 156 body states / 754 frame references, no errors or border
  touches, 211 original source frames and original source manifest unchanged.
- Crew complete packs: 19,591 checks, zero failures.
- Native production player: 150 samples per facing, 75 captures per facing,
  distance-driven swimming at 46 world units/second. Both start and stop are
  selected and hand off to the destination loop's frame zero. Clearance denial
  returns a valid base pose; an interrupted start selects a valid stop.
- Native Marsh battery/route test passes with 93 route samples after clearance
  expansion. No gameplay speed or controller changes were needed.
- All final engine runs exit zero without errors. Initial stop-handoff fixture
  assumed an exact decimal time boundary; it now asserts the observable transition
  completion. Production code was unchanged. Evidence is retained separately.

Evidence: `output/marsh-swim-transition-2026-09-22/`, including before/changed
hash inventory, independently reconstructed clearance delta, native results,
captures, rebuild/validation/pack logs and battery-route log. This does not prove
every flood-room route, arbitrary interruption's visual smoothness or owner approval.

## Next action

Author north/south starts and stops, preserving their actual foreshortened poses
and torso anchors. Then address 12 swim turns, 12 dry carry turns and 12 swim-carry
turns, preserving cargo contact. Four of the previously identified 44 clips are
now supplied; 40 remain. Existing test exports predate this work.
