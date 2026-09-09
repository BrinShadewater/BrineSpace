# Companion motion and flood behavior

Use for nonhuman companion animation, flood response or session closeout. Current
project choices live in `character/ACTIVE_ASSETS.json` and `docs/CURRENT_STATUS.md`;
do not infer the selected pack from the oldest character README or highest suffix.

## Source extraction and registration

Inspect actual column counts and row facings before slicing. A requested eight-column
sheet may contain six; opposite-facing cells can occur within an otherwise correct
row. Record reassigned, omitted, reversed and composed poses in the build script or
report. Preserve rejected sources and exact prompts. Do not mirror asymmetric robots.

Keep strict silhouette/divider checks. For a narrow two-pixel gutter, choose the cut
that leaves padding on both crops; a median rounded down can land on the silhouette.
Use reviewed explicit row cuts when automatic gutter detection fails. Do not disable
padding checks globally or erase disconnected paws/cargo to make extraction pass.

Calibrate anatomical landmarks, not full bounding height. A raised cat tail, crouched
legs, horizontal swimmer or extended torch changes bounds without changing body size.
A bonnet/head anchor can register a cat stroke; a torch source needs the robot's body
anchor rather than the flame's center. Quantize water extensions separately when dry
pixels are already accepted. Keep wheeled/tracked bases neutral even when upper armor
is colored. Border-connected white keying must preserve white fur and metal interiors.

## Behavior and rendering

Keep water mode, dry personality action and movement transition clocks separate.
Advance them with simulation time, checkpoint them and stop them on pause. Flood
interruption must clear pending dry actions and repair effects, not merely change the
visible sprite. Gate pet/action UI through the same availability rule as its handler.
Hold shutdown's terminal pose; a long-running clock must not periodically replay boot.

Distinguish a prone swimmer's horizontal body from an upright floating robot's chassis
footprint. Include the full relevant width and test from the actual rescue position,
around props and across doorways. Do not use a human swimmer's head offsets or oxygen
submersion mask for buoyant companions. Their surface line and wake belong to the
renderer, with moving and stationary water clips identified separately.

Block unsafe route nodes and guard movement segments; blocking only the repair bonus
does not stop a robot walking into deep water. Reopen nodes after drainage. Preserve
shared geometry caches and temporary crew exclusions when updating water restrictions.

## Review and closeout

Use the production sprite loader and native flood renderer at station scale. Set zoom,
let layout settle, then set the target cell and focus: zoom refresh can replace inspector
metadata and silently capture the wrong room. Verify the intended actor is visible.

Run `tools/audit_character_bindings.py` to check the active registry, PNG bytes and
declared bindings. It does not execute controllers or approve motion. Use focused
native tests for changed routing, interruption and checkpoints; retain prior passing
evidence when unchanged. Reconcile generated, installed, sampled and packaged status
separately. Preserve known legacy state aliases instead of claiming all states are new.

Do not rebuild every pack merely to close a session. Update the current inventory,
visual bible and dated handoff, sync only changed maintained skill files to the installed
mirror, and report whether an executable was actually rebuilt.
