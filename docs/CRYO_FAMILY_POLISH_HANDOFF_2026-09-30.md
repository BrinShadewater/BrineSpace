# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: Cryopod family polish and source installation

## Objective and acceptance

Owner requested a density, perspective, art style, consistency and animation
pass over the cryopod assets made in this conversation, followed by game wiring.
Reviewed selected human closed/open shells, three fall/rise sets, selected crew
joins, Margot's chamber/door and two broken masters, cold/fog layers and landing.
Latest owner-approved geometry and choreography remain the authority.

## Accepted decisions and constraints

Human crew slowly step, fall, hold and rise; colour returns after floor contact.
Margot stays centered, unfreezes, makes a little hop, and lands at her live spawn.
Her full painted door travels82px and retains9px top overlap. One density per
actor/prop family; no per-pose fitting. Preserve pause, power, save and recovery
rules. Earlier rejected studies remain preserved. Marsh charging is separate.

## Current state

Added character/cryo-material-pass-v1 with three cool-neutral padded open pods,
explicit masks, source/output hashes,32 selected-raster audit and review/README.
Added tools/build_cryo_material_pass.py: deterministic masked colour calibration,
zero resampling, exact alpha and unmasked exterior. Original sources retained.

scripts/architect_cryo_art.gd now binds these exports through whole literal
paths, uses the shared mild(.66,.82,1) cold grade, and keeps the open housing
opaque under the closed reveal to prevent mid-opening shell darkening.
Both core and derelict human wards already share this renderer. Margot's v5
chassis/door, selected actor and broken masters were reviewed and their existing
production bindings retained. Updated timing assertions and native human fixture
output; fixture now waits for observable startup before freezing the scene.

## Verification

Three-actor packaging test PASS: exact selected idle endpoints, single density,
ground contact, unclipped silhouettes, fall/rise join and durations. Material
builder verifies exact alpha and unmasked pixels.32 production rasters readable;
LFS filters confirmed for the new open pod and retained door.

Focused exit timing PASS, zero failures; cryo recovery regression PASS. Final native human PASS: actual selected
textures, paused pixel equality, grounded save/Continue, all three core landings,
rotated found/repaired ward releases and real rendered endpoint equality.
Native Margot PASS: door/aperture/top overlap, rim clearance, mild cold timing,
hop, selected density, paused texture identity, full opaque final cat silhouette
and exact live release point.101 sample compositor packaging PASS.

Visual review: native human phase contact and Margot master/motion phase sheets
at fixed scale. Human evidence: output/cryo-fall-landing-grade-v7/ with86-sample
motion GIF. Margot: character/cryo-ward-layered-v5/thaw-and-exit.gif; regenerated
from final native compositor samples. Margot found-art inspection preserves worn
room shading but omits exterior fog for inspection, so does not certify exploration
visibility. Agent visual review remains separate from owner acceptance.

All Godot runs isolated APPDATA and LOCALAPPDATA. Final human, Margot and timing
runs each report all compared real profile files unchanged, active log excluded.
Full logs/fingerprints: output/margot-cryo-landing-v13/combined-*. Source whitespace
check passes. No executable export, commit or upload requested or performed.

## Next action

Owner review in the source game. Playable export requires the separate maintained
release workflow. No implementation work remains for this requested source pass.
