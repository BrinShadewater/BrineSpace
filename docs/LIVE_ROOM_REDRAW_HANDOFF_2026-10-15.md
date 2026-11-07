# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: live-room redraw costs

## Objective and acceptance

Reduce live-room redraw CPU without appearance changes; compare average FPS and
placement hitches against the latest accepted OpenGL reference. Completed within
the frozen QA cohort and normal-source rendering scope; no 60 FPS claim.

## Accepted decisions and constraints

Keep OpenGL, current art/quality and all live crew/water/doors/warnings. Preserve
layout mutation serials, owner data, unrelated dirty changes and paired UIDs.
Private room-image LOD remains private. Serial guarded Godot jobs, isolated
APPDATA and owner fingerprints are required. No export, commit or publication.

## Current state

Installed `rooms/large-rooms/moonbay.gd` and
`scripts/moonbay_base_canvas.gd`: retain the contiguous floor/perimeter/shelf
prefix, then live water child before existing walls/gates and props. All inputs
except mission/unused generic clock invalidate that prefix; external ports/flood,
layout, helmet, materials and tint fallback preserved. Expanded existing
`tests/test_moonbay_retained_walls.gd`; UIDs unchanged. Status and
[results report](LIVE_ROOM_REDRAW_2026-10-15.md) updated.

Normal idle 49.83 → 50.17 FPS; Moonbay callback saving 0.179–0.198 ms, total
live-room callback saving 0.120–0.171 ms. Placement action normal 57.835/58.391 →
54.323/57.587 ms; 4× 71.350/73.733 → 78.858/74.994 ms. Hitches mixed; no consistent
remedy. Still about 3.27 ms/frame from a 60 FPS idle mean, and 0/16 phase gates.

## Verification

3,840 release frames, both orders, all 16 phase state/camera/path pairs exact;
338 process samples, no foreign/duplicate game. Twelve station cross-process
images and twelve repeat pairs exact. Installed native room oracle: 597 exact
image pairs; large-room retention 163 checks; water replay 493 checks; mission
and save tests pass. Original fails the three new static-retention assertions.
Owner guards preserve all 2,948 files; hashes, UIDs and whitespace checked.
Independent source review and visual review complete. No pending required check.

Artifacts: `C:/bs-live-redraw-20261015/`; helpers/plot:
`output/live-redraw-20261015/`. `ab1-analysis.json`, source/admission identities,
visual parity and native logs are the acceptance evidence. All native jobs are
finished; preserve the owner's editor and unrelated sessions.

## Next action

Profile animated water or first-time room canvas/private capture setup internally
before another candidate. New room creation explains costly placement submissions;
five solar visits were not five submissions. Do not bypass layout serials or
repeat rejected identity/index trials. Atlas bursts and the private LOD journal
bound remain separate. Mac and an actual current-roster Windows export need their
own release acceptance when requested.
