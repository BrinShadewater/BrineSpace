# Veld animation pilot handoff

Updated: 2026-09-27. Brine Space.

Follow-up: see VELD_ANIMATION_REFINEMENT_HANDOFF_2026-09-27.md for the v2 brightness, scale and walk corrections. This document records v1.

## Objective and acceptance
Owner selected v4 crew references and asked to begin animation fixes. Save the design lock and establish representative Veld motion before full-library production.

## Accepted decisions and constraints
Selected hashes in character/crew-turnarounds-v4/design-lock.json. Retain natural face, Balanced head direction, graphite/cobalt materials, lighter skin and asymmetric equipment. New motion is separately reviewed; runtime libraries must remain intact until quality is established.

## Current state
character/veld-animation-pilot-v1 contains three bare clips (idle-south, walk-east, interact-east), six frames each, source PNGs/prompts/rejections, extraction script, manifest, contact sheet and old/new animated WebP browser review. Profile 184x184, pivot (92,172), standingHeight 148. Existing clip durations retained. No runtime assets changed.

## Verification
Final build and sprite-skill validator passed: 18 frames, no errors/warnings. Connected-component extraction handles source spacing; corrected walk uses flat-magenta keying, other clips threshold alpha. Browser preview and contact sheet inspected. Technical checks do not certify smoothness. Idle height 148-149px; walk 146-149px; inspection 144-153px.

## Next action
Refine walk torso yaw between half-cycles and inspection anatomy/registration variation before promotion. Source colours remain unremapped; establish semantic material masks against selected exact ramps. Then native station-scale/foot-contact review in scratch APPDATA, and representative helmet/other-direction coverage. No Godot probe or save-folder access occurred this turn.
