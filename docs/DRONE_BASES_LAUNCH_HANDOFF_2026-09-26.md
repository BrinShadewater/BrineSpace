# Drone bases and first launch previews

Updated: 2026-09-26 · BrineSpace

## Objective and accepted direction
Owner requested standalone bases for three drones and explicitly included first
pad-lowering animation previews. Mining drives on the ocean floor; Construction
and Salvage propel themselves through water. All use steel/charcoal and muted cyan,
with no yellow machine details.

## Current state
Deliverables: `C:/Users/Alex/Desktop/BrineSpace Clean Prop Exports/drone-animation-bases`.
Three transparent base PNGs, three empty open-pad concept PNGs, base lineup,
manifest and exact image-generation provenance. Construction reuses its reviewed
cyan identity; Mining and Salvage are reconstructed standalone from their bays.
Salvage has self-contained propulsion pods and no dock tether. Existing occupied
bay exports remain unchanged. Empty-pad concepts are new proposed launch states,
not registered replacements for the occupied pads.

`launch-preview.gif` shows all three 10-second sequences. `launch-preview.html`
adds playback, scrubbing and speed controls. `build_previews.py` rebuilds the GIF
locally from saved PNGs. These are exploded cutaway motion studies using whole
sprites and schematic cradle guides, not finished articulated sprite animations.

## Launch contract
**Current v5 refinement:** surface-level doors now span the whole upper hatch opening,
including the visible well walls; closed panels conceal the water. A brief texture
displacement at entry/recovery adds settling water movement alongside the splash.
Generated braided steel cable, winch and clevis art replaces thin guide lines
(`hoist-cable-source.png`, exact prompt alongside). Two hoists support the cradle.
Current artifacts are `launch-recovery-v5.gif` and `.mp4`; v4 remains preserved.
The 23-second state sequence and slow warm-white lamps remain. Contact-sheet
review covers door coverage, lift travel and closure; runtime integration is pending.

**Current v4 launch/recovery study:** owner requested footprint-matched splashes,
slower light-like strobes, hatch closing/opening, and physical recovery hardware.
`launch-recovery-v4.gif` uses a generated open lift cradle and split sliding hatch
panels (`hatch-lift.png`, `hatch-doors.png`). `build_cycle_preview.py` rebuilds it.
Launch: warning/open 1–3s; cradle descent 3–7s; clear 7–9s; close 9–11s.
Return: open 13–15s; lift recovery 15–19s; close under raised cradle 19–21s;
secured hold through 23s. This is a proposed rail-guided elevator mechanism.
Warm-white/soft amber beacons flash once every two seconds with a soft halo.
The splash is sized to the moving vehicle footprint and split behind/in front
of the hull at water contact; it is still transformed VFX art, not fluid simulation.
Whole-body and cradle motion remain prototype compositing, not a final animation rig.
Prior v1–v3 media are historical. Owner review and engine integration remain pending.

**Latest owner amendment:** departure lamps flash yellow, and a small splash marks
water entry. Current artifact is `launch-preview-v3.gif` (8 seconds, 38 encoded
frames from 80 samples). The generated transparent `water-entry-splash.png` is
expanded/faded for one second inside the aperture. Keyframes reviewed; all three
hidden-drone checks still pass. `build_hatch_preview.py` and HTML select v3;
`build_hatch_preview_v2.py` preserves the prior build. This remains a motion study.

**Owner correction, current:** drones become hidden beneath the base after leaving
the hatch. Show visible water inside the well and cyan departure lamps. The current
`launch-preview-v2.gif` replaces the exploded cutaway: whole-sprite descent is clipped
to the aperture, lamps pulse during departure then settle, and no exterior travel
is drawn. Three new `*-water-pad.png` sources preserve the earlier empty pads.
`build_hatch_preview.py` rebuilds this eight-second study; water appearance is baked
into the generated pad art, while lamps and drone movement animate. Keyframes were
visually reviewed; all three hidden-drone assertions and alpha checks pass; the GIF
has 58 encoded frames from 80 samples and exactly 8000ms duration. HTML now displays
this GIF; prior interactive cutaway is archived as `launch-preview-v1.html`.
Browser review remains unverified after the earlier denial. No runtime changes.

The following earlier cutaway timings are historical only:
Construction/Salvage: secured 0–1s; lower 1–4.5s; release/stabilize 4.5–5.5s;
water departure 5.5–9.4s. Mining: secured 0–1s; supported descent 1–6s;
seabed contact/release 6–7s; drive away 7–9.4s. Hold to 10s, then preview resets.
These review timings are proposals, not changes to game simulation.
Keep the mining rover supported until contact; it cannot swim. Match wheel travel
to distance and suspension to terrain in final locomotion. Construction tool
handedness must remain stable; do not mirror asymmetric views. Animate propulsion,
tools, cradle/clamps and stationary rim separately. Author underwater occlusion
and pressure-lock transitions during game integration.

## Verification
Base identities and open pads visually reviewed; launch phase contact sheet reviewed.
All six art sources have alpha transparency. Generic sprite validator passes for
the three base references after adding 32px transparent padding to Mining/Salvage;
unpadded sources retained. GIF duration is 10 seconds from 100 samples at 10fps;
identical hold samples are coalesced in encoding.
Browser access to localhost was denied, so interactive HTML playback is unverified.
No alternative browser access attempted. Offline GIF provides the review artifact.

## Remaining work
Owner visual review; final directional views, wheel/propeller/tool cycles,
registered empty/occupied dock layers and game integration. The current renderer
uses launch-position interpolation and scale adjustment in grid_canvas.gd; these
previews do not validate or modify that runtime behavior. No game assets or code changed.
