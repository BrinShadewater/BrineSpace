# Companion personality handoff

Updated: September 9, 2026. Project: BrineSpace.

## Objective and accepted direction

Owner authorized all proposed companion personality additions: Margot sits,
grooms, naps and accepts petting; River makes curious head movements, quiet
beeps and inspects discarded equipment; Josh pivots on treads, gestures with his
head and watches nearby repairs. Companion unlocks and expedition selection remain.

## Implementation

- `scripts/companion_npc.gd`: independent action/transition clocks, cooldowns,
  authored pose playback, equipment/repair approach paths and stationary gestures.
  Personality rests occur between walking periods. Recovery-container inspection
  is available after a River/Josh compartment is repaired; otherwise River scans.
  Josh observes a living architect in repair/weld state, or looks around when
  no reachable repair target exists. No work bonus or resource consumption added.
- `scripts/companions.gd`: optional personality save records, finite/species
  validation, legacy record defaults and pet interaction. Saved action progress,
  pending interest route, cooldowns and pending chirp survive Continue.
- `scripts/main.gd`: Crew journal Locate links and Pet Margot. Petting closes
  the journal, restores its prior running state, focuses her room and triggers
  the reaction. If the expedition was already paused, resume before petting.
- `scripts/station_audio.gd` and `station_audio_cues.gd`: original two-note
  0.42-second River cue, -30 dB event gain, 18-second audio cooldown, spatial
  placement, existing Effects mute/volume and pause handling.
- `character/companion-personality-v1/` plus `tools/build_companion_personality.py`:
  28 clips / 96 frames. Separate expansion manifests leave accepted locomotion,
  portraits and pod art intact. Cat stationary actions face south; robots have
  all four directions. Exact prompts, sources, hashes and derivations retained.

## Verification

Final Godot import and all three expansion manifest validators pass.
`tests/test_companion_personality.gd` passes natively: every action's midpoint
Continue, fixed ground anchor, return to idle, paused clock/cooldowns, journal
pet action, waking from a nap, repeated-click rejection, disk Continue, malformed
timers/species actions, old saves, River's actual approach/inspection, Josh's
approach to a repair worker, independent station RNG, cue duration, effects mute,
audio cooldown and paused rejection. `tests/test_companions.gd` regression passes.

Logs: `output/companion-personality-{final-import,native,regression}.log`.
Native captures and cue: `output/companion-personality/`. Agent reviewed cat
silhouettes at station scale, robot shapes, action phases and the journal control.
Fixtures construct links and hold a worker in repair state to exercise the trigger;
they do not establish normal-play frequency/balance or complete construction QA.
Final native and regression runs have no reported errors.

## Next action and limits

Review the [animation page](../character/companion-personality-v1/review.html).
Owner timing/animation acceptance remains open. Main action GIFs and native stills
are available; full-speed end-to-end transition acceptance is not claimed.
Petting is a player journal interaction with a cat reaction, without a separate
architect hand animation. Survival, feeding, gameplay bonuses and additional
companion jobs remain outside scope. Local Godot source only; no executable rebuilt.
