# Equipment and deposit feedback

Updated: September 8, 2026 · Project: BrineSpace · Task: continue filling sound gaps

## Objective and acceptance

Add feedback for finished diving-equipment changes and newly exhausted deposits,
without replaying unchanged state or adding constant background noise.

## Accepted decisions and constraints

Original procedural audio, no Suno credits or gameplay changes. Keep existing
volume controls, distance gating and frozen Windows packages.

## Current state

Three cues in `station_audio_cues.gd`, exported under `output/audio-equipment/`:

- `helmet_lock.wav`: a restrained latch/seal when a nearby active crew member's
  completed helmet state changes to equipped.
- `helmet_release.wav`: a soft release when that completed state changes to removed.
- `site_empty.wav`: a descending mechanical cue when a surveyed deposit changes
  from positive units to zero within three visible cell widths.

`station_audio.gd` observes these changes with its existing 0.8-second work sampler.
Helmet cues use the crew proximity filter and two-second cooldowns. Depletion has
an eight-second cooldown to coalesce nearby completions. Initial/restored state is
primed silently by the existing observer reset. Starting or cancelling an equipment
animation alone does not change the observed completed helmet state. Empty deposits
do not repeat their cue. All three use Effects volume and localized attenuation.

## Verification

The final focused audio fixture passes: helmet fit/removal transitions, unchanged
equipment silence, new depletion and unchanged-empty silence, plus prior audio
coverage. An earlier fixture failure came from carrying an active repair voice
into the independent swimming check; the fixture now drains it while the actor is
offscreen. Logs are retained in `output/audio-equipment/`. Native stereo audition
passes: 1,306,624 frames, peak -29.06 dBFS, zero dropped frames, successful WAV save
and no engine errors. Targeted whitespace checks pass. This bounded capture does
not establish subjective listening acceptance or worst-case station headroom.

Changed fixtures: `test_suno_audio.gd` and `review_audio_mix.gd` (optional
`--equipment` exports and auditions these three sounds).

## Next action

Listen to the exported cues in context. This is a source pass; the previously
exported Windows builds remain unchanged.
