# Audio Windows playtest

Updated: September 8, 2026 · Project: BrineSpace · Task: audio polish continuation

## Objective and acceptance

Deliver a local Windows build containing the Suno audio polish and positional
station sound, with native checks against the exported package.

## Accepted decisions and constraints

Keep Moonlit Canyon/Test Run as background music; reuse the supplied effects.
No additional Suno credits, gameplay balance changes or online publication.
Keep saves before normal gameplay quit and retain the existing save-failure path.

## Current state

`scripts/audio_shutdown.gd` stops active audio and drains the mixer for 0.2 seconds
before normal title/gameplay quits. Callers in `title_screen.gd` and `main.gd`
retain save decisions. `tests/test_audio_quit.gd` checks both paths and gameplay
save creation. Both new scripts retain editor-generated UID companions.

`tools/build_audio_playtest.py` freezes materialized working files, imports,
compiles gameplay, exports and hashes a local Windows package. Test adapters
exist only in the frozen copy; the default entry remains the title screen.
`tools/check_audio_playtest.py` exercises six native package checks with isolated
APPDATA/LOCALAPPDATA and verifies unchanged EXE/PCK hashes.

Deliverable directory: `output/audio-playtest-20260908/build/`.
Snapshot manifest and full logs are alongside it. Concurrent work created a
medical-center view during the initial snapshot; the first export rejected the
missing dependency. `snapshot-repair.json` and `snapshot-repair-2.json` record its
addition, dynamic registration/image dependencies and the current music playlist
ownership fix. The first package test exposed the latter gaps; retry logs retain
the evidence without hiding either initial failure. The playlist now duplicates
its entries so shutting down one instance cannot empty the next instance.

## Verification

Final import/export pass with zero engine errors. All six native package checks
pass: Suno assets/playback, stereo positioning, title/settings, station systems,
title quit and gameplay save/quit. Each exits zero without engine errors. Test
saves use isolated APPDATA/LOCALAPPDATA. The packaged settings screenshot was
visually reviewed; Music, Effects and Ambience controls fit and remain readable.
Existing raw-PNG loader warnings remain; raw assets are explicitly included.

The final PCK SHA-256 is
`f47e74b90c57092e00c890f374337c256db93cee67b21d9f68646f88acedf7c6`;
the EXE and PCK hashes are recorded in `package.json` and checked after testing.
This is an audio-focused acceptance scope, not full acceptance of concurrent room
art or editor changes. Subjective headphone/speaker listening remains separate
from mixer measurements. Forced process termination bypasses normal quit cleanup.

## Next action

Owner listening during an ordinary expedition: judge music/ambience balance,
room character and distance falloff on the intended headphones or speakers.
