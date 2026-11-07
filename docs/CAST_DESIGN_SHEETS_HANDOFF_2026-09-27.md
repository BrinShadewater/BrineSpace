# Cast design sheets handoff

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Prepare the other cast members' design sheets beside Veld for selecting consistent animation masters.

## Accepted decisions and constraints
Owner selected Veld Balanced and requested lighter skin. Preserve identities, poses during palette remapping, equipment sides and existing runtime assets. New generated designs have not yet received visual acceptance.

## Current state
`character/cast-design-sheets-v1/` contains Bill, Branforth, Marsh, Margot, Josh and River sheets, source prompts, SHA-256 review manifest and a seven-character gallery including Veld. No runtime replacements.

## Verification
Visually inspected all six generated sheets. Verified six valid PNGs, gallery image paths and HTTP serving. Human sheets provide proportion/material references. Companion sheets are softer than the human pixel treatment; their decorative slogans are not game copy. No Godot tests needed for concept-only assets.

## Next action
Review character identity and proportions with the owner, correct any selected details, then finalize common pixel treatment and exact numeric material palettes before producing animation frames. Generated swatches alone do not enforce exact colours.
