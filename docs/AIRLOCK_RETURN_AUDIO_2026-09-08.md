# Airlock and crew return audio

Updated: September 8, 2026 · Project: BrineSpace · Task: airlock stages and crew return

## Objective and acceptance

Make pressure-chamber progress, accepted recall and safe empty-handed return
audible without changing interlocks, expedition costs or salvage rewards.

## Accepted decisions and constraints

Original procedural sounds, no Suno credits. Preserve quiet repeated updates and
checkpoint loading. Existing Windows packages remain frozen.

## Current state

Five cues in `station_audio_cues.gd`, exported under `output/audio-airlock/`:

| File | Trigger |
| --- | --- |
| airlock_pressure.wav | Enter equalizing or depressurizing |
| airlock_release.wav | Begin opening the inner or outer hatch |
| airlock_ready.wav | Reach dry or exterior-ready state |
| ui_recall.wav | Accept the first recall request for a dispatched crew member |
| crew_return.wav | Finish returning through the dry chamber without cargo |

Airlock cues use the controller's existing phase observation and require an
operational chamber. Positions follow the room; Effects volume and individual
cooldowns apply. Unchanged phases do not repeat, and skipped intermediate phases
are not replayed as a catch-up burst. Cargo-bearing returns keep their existing
cargo sound rather than playing both cues.

`crew_expedition.gd` owns recall acceptance; `airlock_panel.gd` calls it. Already
requested recalls remain silent. `run_save.gd` finishes restoration by clearing
old one-shots and silently priming audio observation through
`station_audio.gd.reset_after_restore()`. This also cancels a pending stale
all-clear cue. Restore logic and saved data formats are otherwise unchanged.

## Verification

Focused audio fixture passes all five new streams. The station systems fixture
passes with actual outward and return interlock cycles, all three stage sounds,
single recall acceptance, silent repeated recall, empty-handed safe return and
unchanged cargo counts. A deliberately mismatched pre-restore phase verifies that
checkpoint restoration does not replay ready/release cues. Final fixture logs have
zero engine errors. Native stereo capture saved successfully with no clipping or
dropped frames, but its first shutdown reported two resources still in use. A
verbose diagnostic repeat exited cleanly: 1,306,624 frames, -28.62 dBFS peak,
zero dropped frames and no engine errors. Both logs and recordings are retained
under `output/audio-airlock/`; the clean repeat is `in-engine-mix-diagnostic.wav`.
Targeted whitespace checks pass. The intermittent capture-tool shutdown warning
is not claimed fixed; signal checks do not establish subjective listening quality.

Changed fixtures: `test_station_systems.gd` and `review_audio_mix.gd` (optional
`--airlock-cues` exports and auditions all five sounds).

## Next action

Listen to the WAVs or normal expedition sequence. Package these source changes in
the next requested Windows rebuild. Underwater swimming/suit Foley and active
mining/salvage sounds remain outside this airlock/return pass.
