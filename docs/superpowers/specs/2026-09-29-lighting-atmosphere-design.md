# Lighting and atmosphere pass

Date: 2026-09-29. Status: draft for owner review. Origin: owner playtest note, Sept 28 ("We need a better
lighting system"), then "lighting pass, or some sort of effects that make the game look more professional".

## Intent

Make the station read as a lit, living place at the bottom of the sea. Owner's chosen look (audition, Sept 29,
option B, unpowered rooms lighter than in the mockup): wonder in the water outside, moody light inside.

- Outside: deep teal water with slow light shafts from above, moving caustics, drifting particles.
- Inside: warm pools of light under working lamps, soft glow around lamps and screens, a darker but still
  readable unpowered room, and slow red emergency light in a blackout.
- Whole screen: a light vignette.

Two stages, each shippable on its own. Stage 1 first because it changes the whole screen for the least cost.

## What exists today (measured or read on 2026-09-29)

- Renderer is `gl_compatibility` (`project.godot`). No 2D lights or screen-space glow are assumed.
- `scripts/underwater_fog.gdshader` already draws the water around the station: marine snow, drifting wisps
  and pulsing bioluminescent plants (`scripts/seabed_glow.gd` feeds it `glows[]`), and takes `lights[48]` /
  `directions[48]` for station lights.
- `scripts/grid_canvas.gd` keeps a light level per room (`room_light_levels`, `_room_light_level`,
  `_advance_room_lights`), fading over `RoomLighting.FADE_SECONDS` (0.65 s). Lamp fixtures are drawn by
  `rooms/whole-room/room_lighting.gd` (`draw_fixtures`, anchors at x = +/-110 from the room centre).
- Power flicker is in `room_lighting.gd` (`power_flicker`): at most 3 dips a second (photosensitivity rule),
  clock in real seconds, `steady` while paused, `reduced_motion` dims instead of flickering. Keep this rule
  for every new effect.
- A real play report (Sept 28, 21:48, 2560x1440 window, 7 rooms) showed 57 FPS mean 17.6 ms, about 2,000 draw
  calls, grid draw about 3 ms. This is the baseline to beat; a fresh baseline is measured before stage 1.

## Stage 1: atmosphere

1. **Water shader** (`underwater_fog.gdshader`): add three terms, each with its own uniform strength so
   Quality can scale them: light shafts (a few soft diagonal bands from the top of the view, fading
   downward), caustics (a slow two-layer ripple, faint), and a depth tint (deeper teal with distance
   from the station). Audition values, on a 0-1 scale: shafts 0.75, caustics 0.55, tint 0.9.
2. **Lamp halos**: an additive soft radial sprite at each lamp fixture and lit screen, drawn where
   `RoomLighting.draw_fixtures` draws the lamp, scaled by the room's light level. Threshold-and-blur bloom
   is out of scope (needs a screen copy each frame).
3. **Vignette**: one full-screen `TextureRect` (radial gradient) above the station view and below the
   HUD. Audition strength 0.34.
4. **Quality setting**: `Low / Medium / High` in Settings > Display, stored in `title_settings.gd`.
   - Low: current look plus the vignette.
   - Medium (default, owner decision): shafts, caustics, tint, halos and vignette at the audition strengths.
   - High: the same with a second caustics layer and denser particles.
5. **Reduced Motion**: shafts and caustics hold still; particles use the existing `motion` uniform (0).

## Stage 2: room lighting

1. **Light pools**: for each powered room, two soft warm pools under its lamps, drawn additively in the
   retained lights layer with the room's light level (and its fade) as strength. Colour about (1.0, 0.90,
   0.70); audition strength 0.34, pool width 0.40 and height 0.62 of a cell. Pools are clipped to the room.
2. **Unpowered rooms**: brightness floor 0.55 of normal (owner: lighter than the audition's 0.36) with a
   faint blue tint (audition 0.5 x (0, 0.02, 0.05)). They must stay readable.
3. **Blackout emergency**: unpowered rooms get slow red pulses (audition strength 0.16), one pulse per
   second at most. Reduced Motion holds the red steady at a low level. Uses the `low_power` state so it
   fires only in a real blackout, not for a room that simply has no generator yet.
4. Lighting stays deterministic from the visual clock, so it freezes with pause like the other effects.

## Performance budget and checks

- Budget: at most about 1 ms extra mean per frame at 1440p on the owner's PC, and Low must cost nothing
  measurable. Measure with `tools/soak_test.gd` on the saved 6-crew station and the F7 overlay before and
  after each stage; `tests/test_soak_budget.gd` keeps its 90 ms worst frame / 8 ms mean limits.
- Existing tests that must still pass: `test_retained_lights_parity`, the title, navigation and HUD native
  tests, and `test_overlay_text`.
- New tests: a shader-compile check for the changed `.gdshader`; a native screenshot test per stage
  (Medium, Low and Reduced Motion) saved under `output/`; a test that the emergency pulse never exceeds one
  per second and holds steady under Reduced Motion.
- Owner judges the look on their own PC at 1440p before each stage is called done.

## Not in scope

- Real dynamic 2D lights and shadow casting (`PointLight2D`); the retained-layer design would fight them.
- A full-screen bloom or colour-grading pass.
- New art. Effects are procedural (shader, gradients, additive sprites).
- Mac tuning beyond the Low/Medium/High setting; a Mac check is a follow-up.

## Risks

- The retained lights layer repaints when a room's level changes; pools must reuse its tenth-level
  quantisation so a fade does not repaint every frame.
- Additive halos can wash out light floors (the mockup overexposed at higher strengths). Keep strengths at
  the audition values and check the bright Hydroponics floor first.
- Caustics on a dark background can look like noise at 1080p; keep them faint and slow.

## Open questions

- None blocking. Owner to confirm the unpowered brightness floor of 0.55 after seeing it in the real game.
