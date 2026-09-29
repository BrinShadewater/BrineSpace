# Large room wall and art consistency audit — September 28, 2026

## Scope and references

Reviewed Hydroponics Farm, Storage Depot, Moonbay, and Tidal Power Plant against `BRINESPACE_VISUAL_AESTHETIC_BIBLE.md`, its September 26 accepted prop board, the registered room riser faces, and the existing painted top-down hull material. Checked each of the 16 native card rotations, the Walls-off set, four station captures, and Moonbay's eight mission states. The owner has not yet visually accepted this pass.

## Findings and corrections

| Check | Finding and action |
|---|---|
| Wall perspective | The previous pass rotated a 60-unit upright riser onto east, west, and south edges. The riser now occupies only screen north in every room rotation. East, west, and south use the existing top-down painted pressure-hull material. Walls-off uses low top-down walls on all four edges. |
| Wall art placement | Each fixed control bank moves to a sealed part of the screen-north riser for every rotation. Door openings keep a 92-unit reservation; ocean openings keep a 192-unit reservation. No bank crosses either opening. |
| Pixel density | The four focal installation sources render at about 3.1–3.9 source pixels per world unit. The accepted top-down hull material is about 3.0 horizontally; registered riser faces are about 5.2. The raw wall banks were 12–13 pixels per displayed world unit, so their runtime textures are aspect-preservingly reduced to exactly about 5.0. Original PNGs and hashes remain unchanged. Native card captures show readable forms without the former fine-detail aliasing. |
| Size and clearance | A station port remains 92 units wide. Moonbay's two inner pressure doors are 192 units wide and rotate with the bay. The in-room mini-sub now occupies at most 160 units across its launch path, leaving at least 16 units on each side of a door. Its cradle remains 466×234 units, with the sub visibly clear of the inner walls. This is a visual/art clearance check; mission collision and navigation retain their established contracts. |
| Materials and palette | The green, yellow, cyan, and yellow identities remain accents over matte steel and charcoal. The reused painted hull and door surfaces match the station's established construction. The four painted focal pieces retain the accepted overhead/cutaway view; wall banks are shallow, inward-facing fittings on the north riser. No tall frontal wall face appears on the other edges. |
| Moonbay state | Painted inner north/south walls and side returns surround the dry bay. The station door and ocean gate show separate full-length leaves, frames, and open pockets. Native mission captures show the chamber through flooding, launch, return, draining, and damage states without a permanently flooded starting bay. |

## Verification

`test_large_room_art`, `test_large_room_integration`, `test_large_room_paid`, `test_moonbay_missions`, and `test_moonbay_save` pass 5/5 under scratch `APPDATA` (`output/test-runs/20260928-232925-headless`). Native card baker captured all 16 raised and 16 Walls-off rotations; four room cards were rebaked. Station and mission review scripts exited successfully under scratch `APPDATA`. The isolated checkout still logs missing unrelated `brineui`/icon atlas resources; room walls and mission imagery render in the captures.

## Remaining review

Owner visual acceptance and a normal long-run playtest remain open. The latter should tune rare-card timing, economy, and mission pacing; these art changes do not change those rules.
