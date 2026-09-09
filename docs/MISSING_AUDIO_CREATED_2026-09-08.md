# Missing audio cues created

Updated: September 8, 2026 · Project: BrineSpace · Task: create missing audio

## Objective and acceptance

Create the construction, expedition, crew and room sounds identified in the audio
inventory, connect real triggers, and keep busy stations quiet and bounded.

## Accepted decisions and constraints

Original procedural audio, no Suno credits or external assets. Preserve gameplay,
paid building and saved preferences. Existing Windows packages remain frozen.

## Current state

Ten sounds are created in `scripts/station_audio_cues.gd` and exported as individual
22.05 kHz, 16-bit mono WAVs under `output/audio-missing-cues/`:

| WAV | Trigger / behavior |
| --- | --- |
| build_complete.wav | Actual paid room assembly completes; 2-second cooldown |
| build_blocked.wav | Assigned builder loses power, or queued order has no builder route; notify transition only, 15-second cooldown |
| launch.wav | Observed docked drone leaves; 4-second cooldown |
| footstep.wav | Nearby dry crew moves in walking state; sparse, nearest eligible actor only |
| tools.wav | Nearby equipment checking or recovered-machinery inspection; 3-second cooldown |
| repair.wav | Nearby crew repair animation; 3-second cooldown |
| ui_end.wav | Conclude Expedition or victory; survives stopped gameplay |
| ui_failure.wav | Run failure; separate descending tone, survives stopped gameplay |
| refrigeration.wav | Nearest powered, unsuspended Cold Store; quiet looping compressor |
| workshop.wav | Nearest powered, unsuspended Salvage Workshop; quiet machinery bed, fades on pause |

The controller (`station_audio.gd`) bounds work observation to every 0.8 seconds,
crew Foley to 2.5 visible cell widths, and room ambience to nine players total.
Existing stereo falloff applies. Effects and Ambience controls remain separate.
Queued route checks use the fleet's actual routing rules. Restored state is primed
silently. Repeated blocked states and simultaneous same-kind completions coalesce.

`station_audio_space.gd` resolves the two new room sources. `main.gd` now distinguishes
paid scheduling feedback from completed construction, and archive/victory outcomes
from failure without changing reward decisions. New cues lower music through the
existing priority mechanism where appropriate.

## Verification

Focused audio integration passes: launch, blocked-state repetition, nearby movement,
repair, distant silence, cue release, layer cap and actual Conclude Expedition.
The paid drone-job fixture passes its new completion-audio assertion and existing
economy, reservation, clearance, pause and checkpoint checks. Native stereo checks
pass after isolating background comms audio from the spatial probe; the original
failed probe log is retained. Targeted whitespace checks pass.

Native 32-second cue demonstration: 1,413,120 frames, peak -28.34 dBFS, zero dropped
frames, successful WAV save, zero engine errors. Ten individual WAVs have nonzero
peaks below clipping; durations and hashes are in `cues.json`. Existing raw-image
warnings are unrelated. Signal checks do not establish subjective listening quality.

Changed fixtures: `test_suno_audio.gd`, `test_audio_space.gd`, `test_drone_jobs.gd`
and `review_audio_mix.gd` (optional `--missing-cues` exports and demonstrates cues).

## Next action

Listen to the individual WAVs or `in-engine-mix.wav`; tune cue balance during normal
play. Source integration is complete. Package inclusion awaits the next Windows
rebuild. Voice acting, bespoke musical endings and optional all-clear feedback
remain possible future work, outside these ten cues.
