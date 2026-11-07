# Natural crew water contact

Updated: September 8, 2026 · Project: BrineSpace

## Objective and acceptance

Owner accepted softer water/leaks and requested removal of the round blue circle
around crew. Native preview: `output/crew-wake-polish.png`; owner review pending.

## Accepted decisions and constraints

Keep depth-dependent body submersion, exposed swimming heads and critical bubbles.
Visual change only, no movement or flooding balance changes.

## Current state

`scripts/flood_visuals.gd` replaces standing and swimming closed rings with two
separated, gently animated tapered strokes. Muted highlights leave the front and
center open. Authored facing directs the short wake behind walking/swimming;
idle/treading stays close to the body. Critical oxygen bubbles remain separate.

## Verification

Native four-stage and Save/Continue fixture passes with no script errors after
correcting a local type-inference error. Wading/swimming screenshots visually
reviewed. Log: `output/crew-wake-native.log`. Scoped whitespace check passes.

## Next action

Owner visual review of the subtler contact effect. No frame-rate claim made.
