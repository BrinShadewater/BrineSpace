# Door art and animation redesign

Updated: September 26, 2026. Preview collection, awaiting owner review.

## Objective and accepted constraints
Redo door artwork and animations to match the risers/caps. Preserve 72-unit clear
openings, 92-unit mounting bays, room ports, footprints and the accepted layering.
New paired sliding pressure doors use shared matte steel with restrained teal.

## Deliverables and implementation
raised-source.png (1254 square) and low-source.png (2172 by 724) were generated
with built-in image_gen, with genuine alpha, then copied unchanged into this pack.
Exact prompts: prompts.json. Crop registrations, dimensions and hashes:
registrations.json. Original generated files remain under the Codex generated_images
folder; original door-polish-v1 art is unchanged. Both new masters use Git LFS rules.
Reference roles: brine_core riser master supplies materials; old raised door supplies
geometry. New raised art supplies subject identity for the overhead companion.

New tools/preview_door_art.gd and paired UID implement registered rigid leaves,
stationary frames, cropped pocket retraction and the common eased travel curve.
Opening duration 1.05 seconds; closing 0.85 seconds. The first 10 percent releases
the seal, travel ends at 94 percent, then holds seated. No texture squeezing as
leaves open. Short corridor leaves crop vertically at consistent artwork scale.
Preview integration: tools/preview_riser_room.gd, tools/preview_riser_variations.gd.
Shared rooms/doors/door_finish.gd and rooms/underwater/corridor_wall_art.gd expose
an opt-in preview hook; production defaults remain null and keep current art.
All room door directions and corridor families use the new skin in revised mode.

review.html plays 25 native Godot positions each for BRINE, straight, corner and
tee corridors (100 frames total, listed in animation-captures.json). It includes
pause, endpoints, position scrubber, room selection and enlarged door details.
Browser playback is a captured preview; native motion is continuous and reversible.

## Verification
Source alpha and eight registered crop bounds checked. Motion endpoints, monotonic
travel and no overshoot asserted. Full 47-room native capture/clearance pass:
output/riser-room-preview/session-672a802db4874cedbbb9d9127702812e.
Final scale retests with new sequences: session-950e1f80f70847d3846bf8dd35988991
(BRINE), session-b6b702c385d04b938a25dda6fbeafddc (straight),
session-645d360bb3d444988e2e8bef401f8091 (corner),
session-08e724c8701e49198c2fe87a305a97d7 (tee), all under the same output folder.
All passed; owner save fingerprints unchanged. Browser open endpoint, play/pause
state and room selection checked; native closed/mid/open BRINE and corridor
captures inspected. No live-game/export or door collision behavior change claimed.

## Next action
Owner visual review at review.html. Production adoption remains a separate step.
