# Common props batch 2

Updated: 2026-09-26 · Project: BrineSpace · Task: expand neutral common props

## Objective and acceptance
Owner requested more props after the corrected ten-prop family. Create eight complementary common assets using the same simplified painted treatment, overhead camera and neutral materials.

## Accepted decisions and constraints
No department themes; sparse natural accents. Futuristic underwater-base equipment, broad painted surfaces and compressed front depth. Use fixed accepted source masters for style/camera: sp-recreation-extra3-6, sp-recreation-extra1-1, sp-science-extra3-3 and sp-operations-extra1-1. No runtime installation or owner-layout edits.

## Current state
Eight individual PNG masters: storage bench, utility cart, open shelving, recycling station, water dispenser, wall cabinet, folding stool and coffee table. Exact built-in image_gen prompts in production.json; generator source paths in sources.json; selected dimensions, alpha ranges and file/reference hashes in manifest.json. Originals remain in generated_images. review-light.jpg and review-dark.jpg show the batch normalized for comparison, not world scale.

## Verification
All eight decode as RGBA with zero-alpha backgrounds. Full generation previews and light/dark composite sheets visually reviewed for readable silhouettes, broad top surfaces, complete supports and genuine frame gaps. Cart handle, shelving cross braces and stool supports remain intact. Wall cabinet includes mounting tabs but no wall. Water dispenser is an inactive static design with a parked flask, not an operational dispensing animation. No game tests: code/registrations unchanged. Owner acceptance, world scale, wall registration and runtime interaction/clearance remain unverified.

## Next action
Owner review of eight candidates. If integration is requested, establish crew-relative scale, floor contacts/mounting and interaction footprints before registration; preserve all owner layouts. Do not replace locked reference masters with these candidates.
