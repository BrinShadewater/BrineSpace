# Reactor and Gravity Loom wall-bank handoff

Updated: 2026-09-08. Project: BrineSpace.

## Objective and direction

Continue the owner's ongoing wall-length asset/prop production and improve the
workflow and bible from observed results. Keep modest scale and matte materials.
These two banks add equipment-specific identities rather than more screen arrays.

## Deliverables and selected sources

- `reactor.png`: coolant service filters, armored cabinets and guarded shutdown
  controls. Selected V2, 1882x836 RGBA; 320-unit diagnostic width, 93.21 high.
  V1 retained as rejected for reflective pipe/cap/handle highlights.
- `loom.png`: calibration rings, unequal reference weights, measurement probe,
  instrument column, open supported case and drawers. V1, 1923x817 RGBA;
  320-unit diagnostic width, 96.11 high. Work surfaces stay subordinate to the
  existing central apparatus.

All original sources and exact built-in imagegen prompts remain alongside exports.
`manifest.json` records selection, dimensions, hashes, reference roles and findings.
Sources are opaque RGB; neutral registrations use 228 for Reactor's white exterior
and 160 for Loom's checkerboard. These are source-specific thresholds. The Loom's
ring centers show the real worktop, and the open case has foam lining; neither is
exterior background to remove.

## Verification

Native Godot source-hash/size/alpha export checks PASS in
`output/reactor-loom-wall-reactor.log` and `output/reactor-loom-wall-loom.log`, with
no ERROR/SCRIPT ERROR. Both 1040x900 scale boards were visually inspected on dark
and light backgrounds, including the fitted detail view. Transparent exterior
corner samples pass. Sources and export hashes are recorded independently.

Reactor V2 reduces shiny detail without a blanket dark tint. Loom varies the
working heights and materials while retaining a shared plinth and wall-contact
rail. Matte appearance does not require an all-charcoal room palette. These
findings refine the skill and bible; they are agent review, not owner acceptance.

## Remaining work

Both assets are standalone horizontal south-facing fronts. No room placement,
card binding, operating animation or package is changed. Cross-room ports and
central-machine perimeter routes require a split layout or authored inward side
views before installation. The ongoing production goal remains active; a useful
next batch is directional Airlock wall components using the existing matte bank.
