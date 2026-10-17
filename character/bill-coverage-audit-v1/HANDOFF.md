# Project handoff

Updated: September 30, 2026 · BrineSpace · Bill selected coverage/consistency audit

## Objective and acceptance
Complete the full master-consistent Bill set, then full cross-animation polish.
This audit establishes the current selected source inventory and identifies
remaining replacement work. Existing keys are not proof of master consistency.

## Accepted decisions and constraints
Preserve selected matte masters, anatomical size/perspective, native helmets and
furniture-specific east bunk behavior. Keep source selection, visual matching,
autonomous activity, clearance, interruption/restore and owner acceptance separate.
No gameplay or runtime selection changes at this audit milestone.

## Current state
build_audit.py resolves catalog and literal normal-loader overrides in order,
retains manifest/loader hashes, and records selected provenance in source-audit.json.
Normal native fixture verifies source resolution against the actual loaded player.
Current inventory:186 bare/179 helmet selected states;1,652/1,598 frame references.
This includes equipment transitions and compatibility states; it is not a promise
that every state has final revised artwork. lifeRows covers18 action families,
four directions and two gear states. The18 absent rows are only north/south/west
bunk-enter/sleep/exit; actual Major Bill bunk behavior explicitly faces east.
They are not nine missing animations to invent for existing furniture.

## Findings and replacement order
The six seated actions, recovery and underwater death use revised selected
families. Eating, drinking, inspection, generic lie/sleep/get-up and death-ground
still come from major-bill-v3 packs. Native comparison shows the older life art
has broader cartoon-like heads/faces, brighter surfaces and different helmet fit
than the revised idle masters. Generic north/south sleep is also upright-looking
on the native contact and needs pose review. Do not count these as completed.
Keep the separately authored east bunk consumer intact pending its own review.

Next author inspect-east against the current east master, then independent cardinal
inspection family (both gears), followed by eating/drinking, generic rest and dry
death. Equipped eat/drink currently present inspection via crew_life.gd; a sealed
helmet does not need a new feeding-through-visor action. Preserve that behavior.
Cardinal seated comparison shows consistent matte tone/native helmet size overall;
side views and front/rear projections have different natural silhouettes. Final
arbitrary joins, motion amplitudes/pacing and full-set polish remain unproved.

## Verification
10,485 native checks PASS14.14sec: all selected keys/counts, raw PNG availability,
resolved pixels for bare/precomposed equipment, and available loaded artwork.
Non-precomposed equipment is explicitly exempt from raw-pixel equality because
the existing native fitter may alter it; this limitation is preserved in fixture.
Fresh cardinal seated and selected legacy-life82px boards visually reviewed.
All2,914 owner non-log files unchanged under scratch APPDATA. Earlier audit run
used noisy Image.load_from_file warnings; fixture now uses maintained raw-buffer
safe_image path. This is a source/renderer audit, not world journey or release proof.

## Next action
Author independent east inspection motion and then cardinal paired sources.
Continue remaining replacements, real activity/restore/clearance checks and
cross-animation material/proportion/pacing polish. Full goal remains active.
