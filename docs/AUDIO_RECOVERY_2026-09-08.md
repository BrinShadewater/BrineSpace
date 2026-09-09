# Recovery and crew feedback audio

Updated: September 8, 2026 · Project: BrineSpace · Task: sound pass and remaining cues

## Objective and acceptance

Fill three silent feedback transitions and tighten overlapping crew sound handling,
using restrained original audio and verified gameplay triggers.

## Accepted decisions and constraints

No Suno credits, external generation or changes to dispatch/recovery requirements.
Prior Windows packages remain frozen. Keep repeated and paused state changes quiet.

## Current state

Three original procedural cues are implemented in `station_audio_cues.gd` and
exported under `output/audio-recovery/`:

- `all_clear.wav`: a soft resolving tone after previously reported warning
  conditions remain empty for three active seconds. Returning risks cancel it;
  pause stops the timer. Only one notification per confirmed recovery, with a
  20-second cooldown. It refers to monitored warnings, not every possible hazard.
- `crew_dispatch.wav`: a brief receiver/mechanical confirmation after successful
  `crew_expedition.gd` dispatch, localized at the departure room. Failed attempts
  never reach the cue; two-second cooldown.
- `crew_awake.wav`: a subdued rising tone when `cryo_recovery.gd` adds an actual
  survivor to the roster, localized at the ward. Blocked or unfinished emergence
  stays quiet; five-second cooldown coalesces simultaneous wakes.

`station_audio.gd` now refuses new crew Foley while another crew Foley voice remains,
in addition to its existing shared cooldown. This avoids overlap with the slightly
longer tails introduced by pitch variation. Event settings share one lookup.
The ambience cap remains nine and existing volume controls apply.

## Verification

Focused audio tests pass, including stable recovery, returning risk cancellation,
pause, nonrepetition and cue playback. Station systems and cryo recovery fixtures
pass new assertions on actual dispatch and survivor emergence. The initial station
run passed assertions but logged two resources still in use at exit; a verbose
diagnostic rerun exited cleanly without that warning. Both logs are retained.

Native stereo audition passes with 1,409,024 frames, -26.51 dBFS peak, zero dropped
frames, successful WAV save and no engine errors. Evidence and the three WAVs are
under `output/audio-recovery/`. Existing raw-image loader warnings remain separate.
These bounded signal checks do not establish subjective listening acceptance.

Changed fixtures: `test_suno_audio.gd`, `test_station_systems.gd`,
`test_cryo_recovery.gd` and `review_audio_mix.gd` (optional `--recovery` audition).

## Next action

Listen during normal play and incorporate these source changes in the next
requested Windows build. Voice acting and bespoke musical endings remain optional
future production work; the three cues above are complete.
