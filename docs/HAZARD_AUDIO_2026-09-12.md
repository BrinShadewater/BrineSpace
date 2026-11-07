# Hazard audio handoff

Updated: 2026-09-12. Project: BrineSpace.

## Objective and accepted decisions
Owner chose to skip nozzle art because the fitting is not visible, and approved hazard audio, a combined fire/flood/repair check and a refreshed playable build. No new nozzle asset was made.

## Current state
scripts/station_audio_cues.gd adds original synthesized leak drips (0.65s), sprinkler hiss (1.5s), electrical crackle (0.55s) and a metal creak (1.7s). No external sound downloads or generator credits. scripts/station_audio.gd selects the nearest active source per hazard, uses existing spatial attenuation/effects volume, bounds repeats and stops stale voices. Creaks follow increasing damage stages, with an 8s global cap. Restore clears prior hazard observations. Pause freezes playback and voice lifetime; audio-only bookkeeping does not consume gameplay RNG.
Tests: tests/test_hazard_chain.gd with paired UID, registered in fire subsystem. Includes real reactor heat ignition, 40 seconds unsuppressed fire, sprinkler power interruption, remaining hull leak, physical crew travel/patch/full weld and powered drainage. No crack or water was injected to make the main chain pass; a separate stage-boundary probe tests the creak.

## Verification
Headless hazard-chain and existing Suno audio regression passed. Native hazard chain passed with zero script errors, including pause of active spatial sound. Spatial audio playback needs a physics frame before it can be inspected; fixture waits for that instead of treating a just-requested stream as already playing. Evidence: output/hazard-chain-native.log. After 40 simulated seconds, fire was 0.6, crack 0.041636 and room water 0.029552096. Crew reached the reactor, fitted the patch, welded, survived and spent 3 Metal total. Pumps drained the residual water. Four PCM previews in output/<cue-name>.wav have zero clipped samples; peak amplitudes 0.287 to 0.499 before runtime attenuation. These checks establish behavior and headroom, not owner acceptance of the sound mix.
Release manifest and assertion-safety tests passed (2 tests each). Build identity and actual package evidence are recorded separately in HAZARD_RELEASE_2026-09-12.md.

## Next action
Owner listening/playtest for subjective mix and pacing. Long expedition balance is not established by the controlled integration fixture.
