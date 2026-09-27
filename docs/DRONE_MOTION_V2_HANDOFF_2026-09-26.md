# Project handoff

Continuation: owner approved the next reach/stow and collection-sequence work.
See [the job-sequence handoff](DRONE_JOB_SEQUENCES_HANDOFF_2026-09-26.md) for the
current 48-clip supplement and remaining runtime integration scope. The counts
below describe the preceding cardinal-loop milestone.

Updated: 2026-09-26 · Project: BrineSpace · Task: northwest bend, size pass and cardinal actions

## Objective and acceptance
Owner said the revised art was better, requested another propeller pass, movement
in all directions, mining/collection/welding/repair and a pulsing top light.
Owner liked the missing-arm repair, then requested a stronger rightward bend in
the northwest left arm, a proportional size pass, and actions in N/E/S/W. This
revision delivers those review assets; owner acceptance remains pending.

## Accepted decisions and constraints
Retain muted-cyan/steel identity, asymmetric tools and .34 world units/library
pixel. Top status meanings remain blue operational, red stopped, yellow charging
or out of power. Provisional south hull width remains 69.12 world units.
The singular-drone request was used to make all four visual work studies on this
drone; optional role-allocation question unanswered. Existing fleet roles unchanged.

## Current state
`assets/drone-motion-v2-2026-09-26/` holds independent eight-heading sources,
corrected rotor rigs, sixteen authored work contacts, layered loops, status pulses,
PNG frames, atlases, provenance/prompts, GIFs and an interactive `index.html`.
2448 body frames, 1632 effect frames, 153 status frames; 51 atlases. These counts
include deterministic local articulation, not that many newly generated poses.
Local review is served at `http://127.0.0.1:8767/` (delivery process 204840).
No runtime, saves, owner layouts, commits or release changes.
Selected `sources/northwest-curve-v4.png` bends the left tool up/right and narrows
its barrel/forearm. Rebuilt 102 northwest frames/two atlases. Three independent
`work-*-v3.png` sheets supply the twelve new cardinal clips. Original sources
remain retained. All 1683 pre-existing frames outside northwest are hash-identical.
New builders: `build_cardinal_work.py`, `build_cardinal_review.py`. Updated preview
keeps the work action selected when heading changes, restricting work to cardinals.
`review/size-pass.png` and `review/SIZE_PASS.md` record proportional comparison.
Exact prompts are beside all generated sources; built-in imagegen was used.

## Verification
Current pack validator passes eight travel headings and sixteen work combinations,
all frame paths/alpha/borders, active motion and timing. 144 atlas/frame samples
match byte-for-byte. Earlier generic validator evidence covers only the old pack.
Source hashes pass. Blade masks preserve pixels outside the rotor annulus,
including housings/hub highlights. All three lamp states pass brightness checks;
white-source fade bug corrected. Direction/pose boards, same-scale comparisons and
representative active phases visually inspected; all sixteen live browser work
selections reached loaded playback. Evidence: `review/browser-cardinal-checks.json`,
per-clip browser captures, `cardinal-work.gif`, phase boards and pack-validation.json.
Fixed scale/registration avoids independently fitting poses to their bounds.
Natural perspective/foreshortening remains; this is not exact 3D dimensional proof.
Godot was not run in this revision; prior isolated scale fixture remains evidence
only for its original approved-source overlay.

## Next action
Owner review of the curved arm, size comparison and sixteen contact loops. Continue
full approach, grip/release and pick-up/drop-off transitions. Settle final physical
scale, then integrate animation/state mapping into Godot.
Do not promote candidate sources over accepted-v10 or change fleet roles silently.
