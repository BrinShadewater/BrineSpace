# Crew turnarounds handoff

Updated: 2026-09-27. Brine Space.

## Objective and acceptance
Complete front/rear/both side views with helmet off and on for Bill, Veld, Branforth and Marsh.

## Accepted decisions and constraints
Preserve current names/roles, natural faces, shared suit materials, Veld's blue markings and Balanced head direction, white helmet lamps and exact material palette strips. Opposite sides must retain anatomical tool ownership.

## Current state
`character/crew-turnarounds-v4/` contains four eight-view PNG studies, self-contained palette SVGs, prompts, source/output hashes, deterministic palette-layout builder and gallery. V3 face/visor close-ups remain linked. No runtime changes.

## Verification
All four generation calls succeeded. Agent visually reviewed 32 views, including opposed directions, helmet states, white lamps and asymmetric canisters/wrench/temple hardware. PNG sizes 1536x1024; SVG parsing and embedded PNG byte equality passed; all four served HTTP 200. Palette specification is byte-identical to v3. Static design review only, not motion or native-scale acceptance. Side poses are illustrative and some are slightly three-quarter rather than strict orthographic profiles.

## Next action
Owner review of complete turnarounds, then freeze selected references and test a representative sprite pair before animation expansion. Palette strips define targets; generated art is not yet exactly remapped to those values.
