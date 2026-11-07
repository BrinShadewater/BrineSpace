# Moonbay water-template experiment

Updated: October 5, 2026 · BrineSpace · R6 follow-up

## Objective and acceptance

Reuse invariant ribbon positions/phases without changing waves, clipping, pumping
or water timing. Accept only if changing water levels also remain efficient.

## Accepted decisions and constraints

**Candidate rejected; no runtime cache enabled.** Keep the previously accepted
cosine-expression hoist. A bounded sixteen-entry numeric template cache preserves
pixels, but adds work during filling. Do not replace it with a larger cache or
approximate geometry merely to make this benchmark pass.

## Current state

Source-derived reference and candidate, generator, guarded native fixture, raw
reports and owner fingerprints are under `output/moon-water-template-2026-10-05/`.
Templates use float64 coordinates/phases to preserve the original expression
order; clocks, water height, clipping and colors remain dynamic. No textures,
animation assets or gameplay resources are cached. No runtime files changed in
this interval; this handoff and current status/register record the decision.

## Verification

Native Godot 4.7.2: **336/336 byte-exact comparisons**. Initial 144 scale/water/
clock/pumping cases plus 64-frame animated, continuously filling and pumping
sequences. Candidate warm-only first run improved median large-water draw time
937.5→918.5 us. Follow-up phase medians:

| Workload | Reference | Template candidate |
| --- | ---: | ---: |
| Animated, fixed water level | 1,145 us | 1,111.5 us |
| Continuously filling | 620 us | 704.5 us |
| Pumping, fixed water level | 1,154 us | 1,139.5 us |

These are paired native fixture samples, not whole-game FPS. Changing wetted
geometry requires new templates; that overhead outweighs the warm savings in
filling. Exact pixels alone are insufficient to accept the optimization.
Zero engine errors; both run groups preserve **2,936 owner non-log files**.

## Next action

R7: measure the light-map viewport's GPU cost and prototype update-on-change
scheduling. Its current `UPDATE_ALWAYS` persists while command content is retained.
The scheduling key must also cover viewport dimensions, scroll transforms,
visibility/quality re-enable and every existing light-content invalidation.
Verify rendered pixels through fades, blackout pulses, crew lamps, pan/zoom,
resize and focus changes before enabling. Full-roster memory, long stalls and
packaged PC/Mac certification remain open.
