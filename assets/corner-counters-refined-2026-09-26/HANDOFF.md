# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: closer reference match and counter depth

## Objective and acceptance
Refine two audited counter outliers and preview overlap behavior. Darker muted walnut counter and subtly mottled inset sink cabinets complete; owner review pending.

## Accepted decisions and constraints
Preserve square-room wall edges, orientation, proportions and accessories. Retain original assets. Shelf, chair and server remain unchanged because the audit did not call for broad repainting.

## Current state
Two edited masters and calibrated exports here; production.json records exact built-in image_gen edit prompts, sources.json records originals, manifest.json records hashes/dimensions. Materials and inner return side shading refined without changing intended footprint. Room-preview layout now references these exact exports.

tools/preview_corner_room.gd splits each L into north run and return draw regions using original UVs and separate sort depths. This changes the isolated fixture only. The crew member was placed back at the previously problematic position to verify the correction rather than avoiding the overlap.

## Verification
Native exported material review and Godot screenshot review complete. Darker, less golden wood and increased sink-door painted depth are visible. Return edge shading improves thickness modestly; underlying narrow return design retained. Seven draw regions represent five furniture assemblies. Native movement traveled 160.7 world units with zero clearance failures; doorway-node and pause checks passed; owner save fingerprints unchanged. At the formerly failing sink position, the character's upper body is now correctly visible in front of the north run. Does not certify every possible interaction/occlusion pose or production registration.

## Next action
Owner review of refreshed room screenshot. Production integration remains separate; previous masters preserved.
