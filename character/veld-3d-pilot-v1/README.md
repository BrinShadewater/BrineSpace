# Veld 3D-source pilot

Authorized September 27, 2026. Status: reference preparation complete; model generation blocked. No model, rig, animation or rendered sprite has been produced.

## Intended comparison

Create one reusable Veld model from the owner-selected v4 design, with detachable helmet, then render four directions of idle, walk and sample inspection using a fixed orthographic camera. Review at 148px standing source height and approximately 45px gameplay height beside existing art before runtime installation. The helmet must wrap the same head/body, not change their scale. Use the same scene, materials, light rig and exposure for every frame.

Veld: natural adult face, balanced head size, warm light skin, dark bun with silver streak, no glasses. Graphite quilted suit, cobalt shoulder patches, ivory chest modules, dark straps and muted steel. Three canisters on anatomical right hip; instrument on left. Helmet lamps neutral white. Selected source and palette remain in `../crew-turnarounds-v4/`.

## Prepared inputs

Run `python character/veld-3d-pilot-v1/prepare_references.py` from the repository root. Eight crops retain the source pixels and dark background without labels. `references.json` records their bounds and hashes. Use the four bare crops together for the base model. Helmet views are equipment references; do not generate an unrelated second body.

Candidate catalog model: `multi_image_to_3d` (Meshy). Suggested first trial settings: textured, rigged, A-pose, symmetry off, target 30,000 triangles, casual walk action 30. These are planned settings, not a submitted job or validated result. Auto-generated topology, face, side-specific equipment and skinning require visual inspection. The helmet and inspection animation may require authored work after generation.

## Blocker and next action

The current Higgsfield catalog exposes image-to-3D models, but no callable `generate_3d` tool exists in this session. `estimate_image_cost` rejects this model and explicitly requires `generate_3d`. Chrome's signed-in library reports all credits used; the balance API reports 2 credits, with no trial/unlimited allowance. No exact 3D cost was obtainable. No generation, upgrade or purchase was submitted.

Restore access to the 3D generation command (or an accessible Meshy workflow), establish its cost/available balance, and generate the base mesh from the prepared views. Then inspect the actual mesh before rig/render expansion. Local Blender was not found on PATH or under the standard Blender Foundation installation directory; that is not an exhaustive installation audit.

Existing runtime art and owner save data are untouched. Prepared inputs do not establish 3D quality or consistency.
