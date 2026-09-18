# Owner-supplied music, second batch

September 18, 2026. Five tracks the owner added for the game and the title screen:
Deep Ocean, Oceanic Drift, Silence, Sonar Pressure and Station Pulse.

Masters were supplied as 48 kHz stereo WAVs in `C:/Users/Alex/Desktop/New tracks`
and encoded here to Ogg Vorbis at 160 kb/s, matching the first batch in
[`../suno-v1`](../suno-v1/README.md); nothing else about them was changed, and the
runs are 3:04 to 3:33 each. `manifest.json` records each title, its runtime file
and the SHA-256 of the master it came from.

They join the same playlist as the first batch through
`scripts/suno_audio_bank.gd`, so the title screen and a running station draw from
all nine tracks in one shuffled order. The owner authorized use in BrineSpace;
this record does not make a separate licensing determination.

Re-encode a replacement master with:

```
ffmpeg -i "<master>.wav" -c:a libvorbis -b:a 160k -ar 48000 -ac 2 <name>.ogg
```

Import stays on Godot's defaults, with `loop=false`: the music decks crossfade on
a track's `finished` signal, which a looping stream never emits.
