# Audio coverage and third polish pass

Follow-up: the [ten-cue implementation](MISSING_AUDIO_CREATED_2026-09-08.md) now
fills the construction, expedition, nearby crew and two room-texture gaps below.
This inventory records the audit before that implementation.

Updated: September 8, 2026 · Project: BrineSpace · Task: sound polish and missing audio

## Objective and acceptance

Find silent player feedback paths, fill the highest-value small gaps using existing
assets or original procedural cues, and verify their actual game triggers.

## Accepted decisions and constraints

Keep the quiet, aging underwater station character and Moonlit soundtrack. No new
Suno generation or credits. Do not add constant UI chatter or change game rules.
This audit covers current source call sites; older packages have their own scope.

## Current state

New original cues in `scripts/station_audio_cues.gd`: a subdued two-pulse receiver
notification and a brief rising save confirmation. `station_audio.gd` applies
Effects volume, per-kind voice limits, and cooldowns (8 seconds for comms, 1 second
for save confirmation). Both run during pause as menu feedback. Mechanical sample
rotation now starts at a random supplied variant using the audio-only generator.

`crew_comms.gd` notifies only when an accepted message starts an empty waiting
queue. Duplicate, rejected and additional queued messages do not trigger a sound.
History replay and text reveal stay quiet. `main.gd` adds confirmation to explicit
Save, with the existing rejection cue on failure; automatic saves do not chime.

## Coverage inventory

| Area | Current coverage | Missing or next useful addition |
| --- | --- | --- |
| Music | Four tracks, crossfades, rests, priority ducking | Dedicated expedition conclusion/failure music transition; current music continues |
| Station beds | Ocean, machinery, receiver, airlock, drone, life support, core | Distinct refrigeration, workshop and cultivation textures; currently represented by shared station layers |
| Building | Placement/rejection and observed power on/off | Dedicated order completion and newly blocked-order cue, coalesced across simultaneous jobs |
| Crew comms | New queue notification added in this pass; archive terminal cue exists | No spoken dialogue; no speech generation proposed |
| Save | Manual success/failure feedback added in this pass | No additional automatic-save sound needed |
| Crew movement/work | Door closure and recovered cargo | Sparse nearby footsteps, tool handling and repair activity; keep distant crews silent |
| Expeditions | Moving drone bed, airlock water/door and cargo return | Distinct launch and expedition conclusion/failure cues |
| Discovery and danger | Discovery, warning, integrity-dependent pressure bed | Distinct recovery/all-clear feedback; optional, below completion/outcome priority |

Highest-value next work: construction completion/blocked transitions, then
expedition outcomes. Reuse and edit existing mechanical recordings before spending
generation credits. Crew Foley is lower priority because it can easily clutter
large stations. Hover sounds, per-character text ticks and repeating queued-message
pings are intentionally omitted.

## Verification

The focused audio fixture passes with zero engine errors, including real comms
enqueue/duplicate behavior and paused manual Save writing an isolated fixture file.
It also retains prior audio asset, mute, crossfade, cooldown and ducking coverage.
Native stereo capture passes: 1,404,928 frames, peak -17.68 dBFS, zero dropped
frames, successful WAV save and no engine errors. Evidence is under
`output/audio-pass-three/`. Targeted whitespace checks pass. Existing raw-image
warnings are separate. This bounded capture does not establish subjective listening
acceptance or worst-case headroom for every possible station.

## Next action

Listen to the updated mix, then prioritize construction and expedition cues.
This source pass is not included in previous Windows packages.
