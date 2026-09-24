# New music mix review

Updated September 22, 2026. Owner requested review of newly added music.

## Scope and decisions
Found five newer tracks in the runtime bank: Deep Ocean, Oceanic Drift, Silence,
Sonar Pressure and Station Pulse. These play alongside four original Moonlit
tracks. Pending owner confirmation that no other batch was intended.
No music sources, runtime gains or user preferences changed. No generation.

## Verification
Fresh FFmpeg integrated-loudness and true-peak measurements of all nine complete
OGGs confirm every track reaches -17.50 LUFS after its existing individual gain.
New-track source levels range from -16.91 to -15.39 LUFS; existing attenuation
ranges from -0.59 to -2.11 dB. Their decoded true peaks are below -3.9 dBTP before
attenuation. The player adds its existing -23 dB background level, user volume,
fade envelope and priority-cue ducking. Equal integrated loudness does not prove
identical momentary loudness or subjective balance.

tests/test_suno_audio.gd passes, including all runtime dependencies and gain
entries, two-deck transition, quiet interval, cue duck/recovery, independent mute,
settings persistence and music continuity across scene exit.

Native 32-second capture deliberately starts on a new-track pair, Oceanic Drift
then Station Pulse. It mixes ambience and scheduled UI, construction, door,
power, cargo, terminal, discovery and warning cues. The log confirms pair=true
at the boundary and the incoming track active with the outgoing deck released.
Capture: 1,409,024 stereo frames, peak -14.82 dBFS, zero dropped frames, WAV save
success, exit0 and no logged engine errors. This is one mixed transition, not
auditory approval of every track pairing or a worst-case peak guarantee.

Evidence: output/music-review-2026-09-22/measurements.json, measure.py,
capture.gd, capture.log, regression.log and new-music-mix.wav.

## Repair
tools/polish_suno_audio.py previously replaced the complete mix profile from
original-batch measurements, dropping the newer gains and brightness lookup.
It now merges measured gain entries into the current profile and preserves the
remaining metadata/functions. Missing dictionaries fail explicitly.
tests/test_audio_profile_preservation.py passes two checks covering newer-track
preservation, unchanged brightness/functions and malformed-profile rejection.
The batch was not regenerated; current correct audio assets remain untouched.

## Next action
Listen to the supplied in-engine recording for preferred music/effect balance.
Identify any additional batch if these are not the intended new tracks. No
further gain adjustment is justified by the current measurements alone.
