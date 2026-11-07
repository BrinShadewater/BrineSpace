# Turbine facing handoff

## Objective and accepted direction
Continue full catalog. Owner explicitly corrected turbine to occupy the wall
pointed to by the arrow in every rotation. Initial south-only selection superseded.

## Changed state
Three new directional sources/registrations and prompts in turbine-directional-v1;
original north retained. power_room_view.gd selects wall and matching art, updates
animation anchors and keeps arrow visible. Four defaults relocate machine/console.
Card refreshed and three bindings updated. Coverage, status, bible, rollout and
maintained/installed full-wall lesson updated.

## Verification
Four native views inspected together; alignment-check.json proves wall contacts.
176 routes,188 layout keys,47 card bindings pass. Original north state rendering
retained; overhead south powered preview inspected. Final side animation anchors
implemented but temporal native validation still pending. No export.

## Remaining
Continue other catalog families and missing directions. Validate final turbine
side operating frames during next state-art audit. Full objective remains active.


State follow-up: shared library draw bypass was found and fixed with explicit
custom_library_draw metadata on power-machine replacements. Final off and two
powered timestamps captured in all four orientations; states-verified/checks.json
confirms machine-local temporal changes. Native sheet reviewed. This supersedes
the prior pending side-animation note.
