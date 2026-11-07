# Suno mix polish

These 15 short event edits come from the retained `../suno-v1/` clips. The source
WAV masters remain in Downloads. `manifest.json` records source hashes, exact edit
windows, loudness and runtime gain. No new sound generation was used.

Reproduction: run `python tools/audit_suno_mix.py`, then
`python tools/polish_suno_audio.py`. The latter updates the explicit audio bank and
`scripts/station_audio_mix.gd`. If the original preparation tool is rerun, rerun
these two tools afterward to restore polished runtime selections.

The event edits remove long lead-ins and select measured transients that previously
fell after runtime cutoffs (notably door_01 and placement_03). Five-millisecond
attack and shaped tails soften edit boundaries. Constant gain matches most event
variants to -23 LUFS without compression; the quietest placement is constrained by
the +6 dB boost cap. Corrected event true peaks do not exceed -3 dBTP before the
additional gameplay attenuation.

Existing Ogg music/loop files are not re-encoded. Per-stream gains match the four
Moonlit tracks to -17.5 LUFS, interior to -19, ocean to -20, airlock to -27 and drones
to -18 before their respective mix levels. This preserves source dynamics.

The runtime adds six-second equal-power music crossfades, temporary 5 dB music
ducking for priority cues, and eased ambience/motion levels. Motion loops begin on
activation and stop after fading. A separate cosmetic RNG offsets ambient starts.
Warnings announce changed risks and remind after 90 seconds if unchanged; their
existing text and gameplay conditions remain intact.

Automated waveform measurements guide these edits. They do not establish a
subjective listening judgment of generated content or musical phrasing. The
in-engine audition is under `output/audio-polish/in-engine-mix.wav`.
