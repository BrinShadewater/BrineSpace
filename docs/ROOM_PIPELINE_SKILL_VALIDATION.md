# Room pipeline skill validation

Validated 2026-09-05. Scope: skill creation, no room generation or runtime changes.

## Baseline evidence

Before this skill, the generation workflow produced plausible-looking Corner and
Corridor candidates with incorrect door geometry despite explicit prompts. Local
cleanup tests correctly passed but did not detect that visual defect. Existing
provenance already flagged Corner; this is historical baseline evidence, not a
new independent no-skill agent trial.

## Inline application

Applied the skill's review sequence to `rooms/hybrid/corner.png`:

- Read `layout_04_corner`: west/south doors and elbow path.
- Decoded PNG: 1280x1280; all four corner alpha values are zero.
- Inspected full-size image: west and south walls remain continuous, with isolated
  door trim rather than usable openings. The route stripe ends at those walls.
- Verdict: cleaned, geometry failed, not integrated, not verified.
- Action: preserve image and existing correction flag; do not update live mappings.

This establishes that the documented stages can represent a technically cleaned
but structurally invalid result. It does not prove another agent will consistently
apply them; independent agent testing was not performed because execution is inline.

## Checks

- skill-creator `quick_validate.py`: passed for the project skill.
- Existing cleanup tests: 3 passed.
- References: production and lessons files exist; project tool paths exist.
- No external repository code was copied or executed.
- Skill instructions distinguish implemented cleanup from proposed templates and
  manifests. No template generator or full validation system is falsely claimed.

Project source: `skills/brinespace-room-pipeline/`. Discoverable install:
`C:/Users/Alex/.codex/skills/brinespace-room-pipeline/`. When updating the project
skill, synchronize the installed files deliberately and re-run validation.

## Art-direction update — 2026-09-05

Pre-edit inline gap check: asked the existing reference material how to distinguish
shared construction from repeated composition, and what a per-room art brief must
contain. It specified a hybrid style and reference roles, but supplied neither a
brief structure nor criteria for purposeful wear and room identity.

Inspected Med Bay and Crew Hab PNGs and their exact provenance prompts before the
edit. Both use the reactor as their only image reference. Med Bay's paired beds
are functionally readable; Crew Hab repeats beds, lockers and dining furnishings
symmetrically. This supports varying composition across the pack, not a universal
ban on symmetry. These are inline observations, not independent agent trials.

Update adds a routed art-direction reference: shared construction versus variable
identity, a six-field brief, role-specific reference selection, purposeful detail,
offline/operating readability, and separate art review findings.

Inline application after editing:

- Med Bay: retain paired treatment beds; symmetry supports the function. Review
  card-scale readability and geometry independently; no automatic rejection.
- Crew Hab: preserve readable beds and worn hull, consider varying secondary
  furnishings in a future revision. A hue change alone would not add identity.
- Next biological-room brief: specify growth equipment, steel/organic contrast,
  moisture wear, clear routes and an irrigation anchor; borrow material rendering
  without borrowing reactor machinery or radial composition.

The reference now supplies decisions for the previously missing brief fields.
No images were changed in this skill update. Better generation quality remains
unproven until a new batch and native-size comparison are reviewed. Independent
forward-testing remains unperformed under the owner's inline execution choice.
