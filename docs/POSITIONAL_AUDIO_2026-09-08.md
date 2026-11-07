# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: Positional station sound

## Objective and acceptance
Continue approved audio improvements: camera-relative sound, separate effects and
ambience controls, room character, occasional music gaps and missing cues.

## Accepted decisions and constraints
Keep supplied assets and polished mix. Existing costs, resource conditions, saves
and discoveries are unchanged. No external generation, credits, publication or
replacement of a previously accepted Windows package.

## Current state
`station_audio_space.gd` maps sources through the actual scrolled/zoomed grid. A
listener follows the grid viewport; doors, construction, power changes, crew cargo,
and machinery/water/drone loops use positional playback. Warnings, discoveries,
transmissions and ocean stay global. Aggregate drone deliveries use the most
recent nearby drone source when available. Six local layer categories select their
nearest powered/active source at 5 Hz; continuous layers remain capped at seven.

Core has a quiet electrical tone; powered life support has airflow. Draining reuses
the water loop at a lower level. `station_audio_cues.gd` synthesizes blueprint
selection/rejection, power-down and hull-creak cues. Hull creaks occur every 55–95
active-play seconds. After each two tracks, music rests for 18–30 seconds; other
boundaries retain crossfades.

Settings save Effects and Ambience volume alongside Music/Master. Changes affect
existing playback immediately. Continuous machinery/drone/airlock beds count as
ambience; one-shot feedback counts as effects. Restore Audio Defaults resets all
three categories. Original audio and polished derivatives remain intact.

## Verification
Focused tests cover category controls/persistence, draining, power loss and music
rest/resume, alongside previous audio checks. Native `test_audio_space.gd` captures
the stereo mixer: left/right sources favor matching channels, center balances both,
and a distant source is silent. Real scroll/zoom transforms and seven-layer cap
are checked. Evidence is under `output/audio-space/`. Final settings review is
complete: all three category sliders fit in the inspected native settings capture
(`output/title-settings.png`), and title/settings-to-gameplay assertions pass.
Focused audio, station-system and native spatial checks pass. The stereo probe
measured left/right energy approximately (0.000040, 0.000028) and
(0.000028, 0.000041); centered energy was balanced and distant energy was zero.
Import, UID pairs and targeted whitespace checks pass. Existing raw-image warnings
are separate from audio validation. No physical-speaker listening is claimed.
CURRENT_STATUS had one Windows-1252 dash corrected to UTF-8 to permit its update.

## Next action
Listen in normal play to judge room character, falloff and preferred volumes.
Signal measurements do not establish subjective listening acceptance. These are
source changes; previously frozen Windows packages remain unchanged.
