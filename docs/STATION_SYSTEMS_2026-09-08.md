# Station systems pass — September 8, 2026

Owner requested clearer diagnostics, complete exterior crew expeditions, a
transmission archive, and adaptive sound. These changes extend existing station
health, airlock, checkpoint, Codex and audio-setting systems.

## Player behavior

- Room inspection now links directly to the supply breakdown and room resume
  action. A different next-cycle interruption gets its own remedy. Drone bays
  and the Core include stored-power charging demand, separate from cycle inputs.
- Select a powered Diving Airlock, choose an awake architect, fit their helmet,
  then dispatch a salvage expedition. Dispatch reserves 2 Oxygen for the whole
  journey. Crew walk to the chamber, enter, flood/equalize, swim to a surveyed
  finite scrap site, recover one load, return, drain and exit into dry preparation.
  One scrap load is 1 Metal and 1 Data, credited only on safe return and subject
  to existing storage capacity. No extra character supplies are granted.
- Recall returns without extracting a new load. Power loss holds the chamber;
  exterior crew can travel back and wait for the airlock to be restored. The
  complete trip's breathing reserve is paid upfront, with no separate drowning
  countdown in this pass. Construction cannot occupy the reserved route. An
  expedition locks out manual pressure-cycle and helmet controls for that crew.
- Codex > Transmissions replays the opening message. A functioning Listening
  Post recovers a receiver fragment; a successful crew salvage return recovers
  an exterior recorder. Recovered text is stored through the existing progression
  record. Unrecovered recordings are not displayed. Replays do not start a loop.
- Original synthesized machinery hum, hull stress and receiver interference
  respond to room power, station integrity and a functioning Listening Post.
  Loading and replay screens have a quiet receiver layer. Existing Master volume,
  mute and unfocused-mute settings govern all layers. These are sound textures,
  not a new music soundtrack.

## Implementation and compatibility

`crew_expedition.gd` owns dispatch/travel; actor snapshots carry the optional
expedition state, route, cargo and recall flag. Existing checkpoints without this
extension remain supported. Validation rejects malformed state and missing or
inconsistent return airlocks before restoration. NPC death clears the reservation.
The rendering uses existing helmet/swimming art; no character raster art changed.

`transmission_archive.gd` is the single source for the opening and recovered
recordings. The existing loading terminal handles replay. `station_audio.gd`
generates bounded four-second PCM loops in memory; no downloaded audio or extra
asset-import step is required. Main gameplay receives narrow integration points.

## Verification

Godot 4.6.1 native and headless checks cover actual locker fitting, all ten trip
phases, all four airlock orientations and all three architects, oxygen payment,
double-dispatch rejection, power-loss holding, exterior checkpoint restoration,
finite cargo, safe return, recall, reserved routes, malformed checkpoints,
transmission persistence and sealed content, replay/skip behavior, diagnostic
link actions, and adaptive sound levels. Native station and archive screenshots
were reviewed. The loading transition regression exercises New Loop and Continue.

The controlled paid-opening check preserved normal costs and failure rules. In
the five-minute mining observation, one generator delivered 8 Metal and incurred
242 seconds waiting for stored Power; two delivered 34 Metal with zero such wait.
Both survived with an awake architect. Blueprints were controlled by the fixture;
this is an automated opening comparison, not a human pacing verdict. No economy
rebalance was made.

Commands: `--path . --script res://tests/test_station_systems.gd`,
`--path . --script res://tests/test_loading_transition.gd`, and
`--headless --path . --script res://tests/playtest_paid_opening.gd`.
The systems test accepts `-- --capture-dir=<existing directory>` for native images.

Existing raw-image export warnings remain. No exported package or release was
created, and the earlier packaged-build acceptance does not cover this source pass.
Human sound-mix and expedition-pacing review remain useful next steps.
