# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: BRINE artwork and animation session wrap-up

## Objective and acceptance
Session closed at the owner's request. Another session is integrating the new artwork. Latest requested appearance: slim BRINE in the blue one-piece suit, 10% larger than v8, smooth floating motion, no central cyan tube line and no BRINE label on the collar. These are the final preview choices; production integration is still pending.

## Accepted decisions and constraints
Preserve existing character likeness, understated palette and room perspective. Keep the tube casing clear of lettering. Preserve saved room layouts and owner data. Do not select an earlier revision merely because it contains a standalone body file.

## Current state
Final preview: `character/brine-scale-v10-2026-09-26/float-preview.gif`; full room: `room-preview.png` in that folder.

Integration inputs:
- `character/brine-scale-v10-2026-09-26/source-atlas.png`: final tube atlas with center line removed; fixed 1254-square source registration. It is an atlas, not a standalone tube sprite.
- `character/brine-face-v7-2026-09-26/body.png`: final character raster, 45x139. Later revisions reuse it.
- `character/brine-scale-v10-2026-09-26/preview_room.gd`: final body size (184.8 source units high, top 584.6, centered at x626), and no-op nameplate override.
- Inheritance is v10 -> `character/brine-label-v9-2026-09-26/preview_room.gd` -> `character/brine-smooth-v8-2026-09-26/preview_room.gd` -> `rooms/underwater/brine-core/brine_core_view.gd`. V9 lettering is intentionally disabled by v10. V8 owns the eight-second drift mesh, rigid facial region, body-only linear filtering and separate foreground overlay pass.
- `assets/brine-core-corners-corrected-2026-09-26/manifest.json`: selected corner assets, registration and placement. Read its local HANDOFF for full corner integration details.
- `tools/preview_brine_corners.gd` and `.ps1`: current isolated room assembly and verification launcher, including corrected corners, final atlas and comparison character.

Changes and outputs remain in the shared working tree; no commit or production integration was performed here. Preserve paired script UID files. Earlier revisions are retained as references.

## Verification
Final isolated native run: `output/brine-corner-preview/session-aa8bf2d1568f413fa675606c2f569d1d`. Passed loop closure and rigid-face assertions; captured 200 samples at 25 fps over eight seconds. Owner save fingerprint unchanged. Refreshed GIF and visually checked the clean collar, removed center line and enlarged figure fitting inside the tube.

## Next action
The other artwork session can integrate these inputs. Carry over the final no-label override, size and body/foreground draw order, not just the raster files. Validate actual production occlusion, layer lifetime, native scale and room appearance after integration; preview checks do not establish production acceptance. No further edits are pending in this session.

## Later production integration
The September 26 animation polish pass installed the selected figure, atlas and
motion into the production chamber. This supersedes the pending-integration status
above for the chamber (not the separate corner proposals). See
[production polish handoff](ANIMATION_POLISH_HANDOFF_2026-09-26.md).
