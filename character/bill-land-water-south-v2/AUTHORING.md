# Bill South matte revision authoring

Built-in image generation. Two complete source revisions replace early/middle poses in V1; no new state coverage. V1 and all original sources remain. Full master/motion/contact acceptance pending.

## Early material revision

Raw: [saved source](sources/early-grade-v2.png). Prompt: [exact prompt](sources/early-grade-prompt-v2.txt). Execution: exec-2b872392-7295-4782-b0a7-f484176f43f2.

Edit reference image1 (the complete South early-crouch Bill source) for MATERIAL COLOR ONLY. Reference image2 is the selected dry idle's final matte colour authority; reference image3 is original master detail/identity authority. Preserve reference1 exact1024x1536 canvas, transparent background, complete silhouette, all head/body/equipment sizes, boot/floor positions, joint articulation and camera. No repositioning or pose redesign.
Reduce graphite quilt cloth brightness and bright neutral seam highlights to match the darker restrained matte graphite of selected idle. Keep irregular diamond quilting, seams and local texture detail readable; do not crush dark cloth to black or blur detail. Metal cuffs/knee/ankle/boot hardware should retain master worn silver and scratches with muted highlights, not glossy white. Burgundy pads stay muted dark red. Preserve current medium brown hair, facial skin illumination and beard colour; do NOT darken the face or change anatomy. Chest cyan stays narrow restrained light, not glowing bloom. Preserve original markings/equipment sides and form. Pure colour/material polish, no new props, water, background, shadows or text. True transparent alpha.


## Middle material revision

Raw: [saved source](sources/middle-grade-v2.png). Prompt: [exact prompt](sources/middle-grade-prompt-v2.txt). Execution: exec-873cd810-05ea-463d-8dc1-02aa44a4beac.

Edit reference1, Major Bill's South middle-crouch source, to match reference2's final selected idle MATERIAL COLOR. Reference1 alone controls silhouette, pose, identity, anatomy and camera. Preserve its exact1024x1536 transparent canvas and figure registration: hair crown near y173, boots/floor near y1395, head/torso/limb dimensions, knee flex and forward lean, hand positions, chest equipment and original matte-detail design. Do not straighten his knees, lift his head, change his head size or recompose the figure.
Only reduce the overly light graphite quilted fabric and neutral seam highlights to selected idle's darker restrained matte graphite. Retain fine irregular quilt texture and readable seams. Mute shiny silver highlights while keeping worn metal and scratches. Burgundy remains muted red, cyan restrained. Leave medium brown hair/beard and readable facial skin brightness as in reference1; do NOT darken his face. No new equipment, lighting direction, shadows, scene, water or text. True transparent background. Aim for colour-only material correction with original pose preserved.


Original authoring: [V1 prompts and sources](../bill-land-water-south-v1/AUTHORING.md). Ordered reference paths and hashes: [revision evidence](matte-review.json).

## Canonical helmet packaging

Existing shell sources and SHA256 hashes are recorded per pose in helmet-review.json. build_helmet.py fits four original resources without rotation, scaling or recolouring. Initial failing fit retained in helmet-fitting-before-v1; paired body protection and visual review documented in HANDOFF.md. build_paired_review.py restores the paired source player without rebuilding art or discarding review evidence.
