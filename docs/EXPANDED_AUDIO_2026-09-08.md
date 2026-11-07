# Underwater movement, work and hazard audio

Updated: September 8, 2026 · Project: BrineSpace · Task: remaining four audio groups

## Objective and acceptance

Create and connect underwater crew Foley, mining/salvage work, distinct hazard
warnings and more room-specific activity while keeping station audio bounded.

## Accepted decisions and constraints

Original procedural sounds, no Suno credits or external assets. No gameplay rules
or resource costs change. Existing Windows packages remain frozen.

## Current state

Twelve new sounds in `station_audio_cues.gd`; individual 16-bit mono WAV exports
are in `output/audio-expanded/`:

| Sounds | Runtime behavior |
| --- | --- |
| swim, suit, bubbles | Nearby moving underwater crew selects a quiet stroke, suit rustle or occasional bubble cue. No dry footsteps underwater. Shared Foley voice/cooldown limits and slight pitch/level variation apply. |
| mining_work, salvage_work | Nearest working mining/salvage drone with battery remaining supplies a localized drill/cut/scrape source. Idle, returning and exhausted drones supply no work source. |
| galley_work | Soft utensil/work-surface activity in a functioning Galley. |
| medical_work | Quiet equipment pulse for Med Bay, Medical Center or Medical Office. |
| lab_work | Instrument/relay texture for Research, Bio, Xeno or Anomaly labs. |
| cultivation_work | Water/pump detail for Hydroponics, Mycelium Nursery or Biodome. |
| warning_oxygen | Higher three-pulse warning. |
| warning_power | Lower two-pulse warning. |
| warning_hull | Slower low-frequency warning. |

`station_audio_space.gd` maps work/room sources. Room eligibility uses the existing
`powered_room_cells` dictionary, which the economy populates from functioning
`working_cells`; suspended rooms are excluded. `station_audio.gd` selects nearby
activity within three visible cell widths, at most one work/room cue per observation.
Room details have 9–12 second individual cooldowns and a shared four-second spacing.
Crew Foley stays within 2.5 cell widths. Short existing tails may finish as work
stops. These intermittent details use Effects volume; the nine continuous layers
remain on Ambience volume. No additional loop players were added.

Warnings reuse the existing single `warning` voice, 20-second cooldown, 90-second
unchanged-risk reminder and priority ducking. When several hazards coexist, select
oxygen first, then hull, then power. Food/corruption retain the original warning.
Power reserve and projected shortfall share the power signature. This is audible
classification, not a change to hazard severity or simulation logic.

## Verification

Final focused audio fixture passes: underwater movement without footsteps, actual
nearby room observer playback, all four room source groups, suspended/nonfunctioning
silence, active work source selection, returning/exhausted silence, all nine new
activity cues, three distinct warning streams and unchanged nine-layer cap.
Native spatial tests pass with balanced center, correct left/right bias and zero
measured far-source energy. The probe now allows 0.3 seconds for mixer gain ramps
to settle; its prior 0.12-second window caught residual sound. The room fixture was
also corrected to use actual camera coordinates. Initial failed logs are retained.

The 42-second native audition passes: 1,716,224 frames, -23.66 dBFS peak, zero
dropped frames, successful WAV save and no engine errors. Targeted whitespace
checks pass. Original raw-image loader warnings remain separate. Signal checks
do not establish subjective listening acceptance or worst-case station headroom.

Changed fixtures: `test_suno_audio.gd`, `test_audio_space.gd`, and
`review_audio_mix.gd` (optional `--expanded` exports and auditions the twelve cues).

## Next action

Listen to `in-engine-mix.wav` or normal gameplay, then adjust preferred balance.
Source integration for all four requested groups is complete. Include these changes
in the next requested Windows rebuild; previous packages do not contain this pass.
