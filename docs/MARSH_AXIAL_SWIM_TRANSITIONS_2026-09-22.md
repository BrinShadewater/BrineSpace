# Marsh north/south swim transitions handoff

Updated September 22, 2026. Project: Brine Space.

## Objective and acceptance

Complete north/south starts and stops after the side-facing pairs. Preserve
foreshortening, scale and exact existing endpoints; verify selected playback and
clearance. Owner visual acceptance remains open.

## Accepted decisions and constraints

No Higgsfield, owner-room edits, gameplay speed changes, publication or new export.
The built-in OpenAI image tool produced one six-pose source with independent rear
and front rows. Source and exact prompt are preserved as `axial-start-01.*` in
`character/marsh-swim-transitions-v1/sources/`, alongside four frozen endpoints.

## Current state

Four clips added: swim-start/stop-north and swim-start/stop-south. Each has five
frames: exact existing endpoints and three new intermediates. Stops reverse the
authored starts. Timing remains 60/90/100/90/60ms, total 0.4 seconds. All four
directions now have start/stop coverage: eight clips, 40 frames.

`tools/build_marsh_swim_transitions.py` uses a fixed 0.30 scale for both axial rows
and measured shoulder anchors. The initial 0.27 audition shrank the intermediate
poses and was not installed. North/south canvases are 184x184 with pivot 92,172
and standingHeight 148. Existing east/west pixels and registration are unchanged.
`tools/rebuild_marsh_art.py` now reinstalls all four directional supplements.

Runtime adds 20 PNGs and four manifest/provenance files under
`character/marsh-v2/supplemental/swim-{north,south}`. Only the existing catalog and
clearance JSON changed; no existing runtime PNG changed. North lower clearance
grows 1.323 world units to contain the intermediate pose; other bounds stay fixed.
Supplemental pixel contracts and the Python rebuild regression cover all directions.

Preview: `character/marsh-swim-transitions-v1/review/north-south.gif`. Endpoints
are held longer for inspection in the preview, not in runtime playback.

## Verification

- Two Python tests pass across all 40 frames: exact rebuilding, binary alpha,
  profile/timing, exact current endpoints and reversed stops.
- Human crew validator: 160 body states / 774 frame references, zero errors or
  border touches; original source frames and manifest unchanged.
- Crew complete packs: 19,707 checks, zero failures.
- Native production player: 150 samples per direction; starts and stops selected,
  destination frame-zero handoffs, clearance-denied fallback and valid interruption
  checked. Both runs exit zero; intermediate native captures visually inspected.
- Native Marsh battery/route regression passes with 93 route samples after the
  clearance update. Final engine logs contain no errors.

Evidence: `output/marsh-axial-swim-2026-09-22/` holds baseline/changed hashes,
clearance delta, native captures/results, rebuild/validation/pack and route logs.
These are bounded player and route checks, not every flooded room or arbitrary
interruption's visual acceptance. Existing test packages predate this work.

## Next action

Author a representative adjacent swimming turn and test actual turn handoff,
pause/restore and distance continuity before expanding. Thirty-six original gaps
remain: 12 swimming turns, 12 dry carry turns and 12 swim-carry turns. Cargo turns
must preserve the held object's position and anatomical hand contact.
