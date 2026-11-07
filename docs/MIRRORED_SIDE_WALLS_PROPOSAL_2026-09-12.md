# Proposal: one authored side wall, mirrored — September 12, 2026

Owner idea, raised during the Higgsfield pilot: author two pieces per wall asset —
one wide (north/south) and one side — and mirror the side for the opposite wall,
instead of authoring east and west separately. **Nothing is implemented.**
`full_wall_prop.gd` is central to room rendering, so this was propose-first.
**Implemented for new assets only on 2026-09-12** - see "Owner decision" below.

## Why it is worth doing

1. **It removes a real source of drift.** The accepted research side strips are
   `303x974` (east) and `279x979` (west) — hand-authored twins that do not match.
   Every separately authored pair can drift like this.
2. **The pilot showed the same failure in one sitting.** Generating east and west
   from the same brief produced two different banks: different layout order,
   different proportions. Mirroring the east one produced a correct, consistent
   west (`output/higgsfield-pilot-2026-09-12/gate-side-board.png`, panels 1 and 3).
3. **It halves the authoring and generation cost** for every new wall asset.
4. **Mirroring is safe for this art.** The bible bans text in artwork, lighting is
   even from above, and mirroring is exactly what the opposite wall needs: the
   equipment ends up facing inward, and outer-edge pipework stays on the outer edge.

## What already exists

- `RoomLayoutStore.draw_flip()` applies a negative-X transform per prop, reading
  `flip/<id>` through `flip_axes()`.
- Studio exposes flipping (`flip_selected`), and it persists: `test_room_layout_editor`
  asserts both axes survive a disk reload and that the runtime honours them.
- So the *drawing* half of this idea is already shipped and tested.

## What would have to change

1. **Side selection** (`rooms/full-wall-v1/full_wall_prop.gd:52-66`): today it picks a
   separate registration per side by name (`side-<asset>-east` / `-west`) from
   `side_views`. It would instead load the single authored side registration and set a
   horizontal flip when the prop sits on the opposite wall.
2. **Registration polygons must mirror with the art.** `pieces` polygons are read in
   `full_wall_prop.gd:31` and `:238`, `room_asset_library.gd:63` and `:106`, and
   `split_wall_prop.gd:72`. If the texture flips and the polygons do not, placement and
   clearance are wrong for any asymmetric bank. This is the part that decides whether
   the change is small or not.
3. **Studio must preview the same flip**, or authored layouts will disagree with the
   running game — the exact class of bug the shared placement envelope just fixed.

## What must not change

- **North and south cannot be mirrored.** A vertical flip would put the worktop under
  the cabinets. Those stay separately authored.
- **No existing art or registration is overwritten.** Registrations are SHA-256 welded;
  adopting this for an existing asset means a new revision linked to the previous one.
- **Opt-in per asset.** Existing assets keep their authored west art until an owner
  decision retires it; nothing is regenerated wholesale.

## Verification if it goes ahead

- Native captures of one converted asset in all four rotations, beside the authored
  pair it replaces.
- Placement and clearance checks on an asymmetric bank, since that is where mirrored
  polygons would fail.
- The native layout lane, plus `tests/test_layout_keys.py` and the flip assertions in
  `test_room_layout_editor`.
- Studio-versus-live comparison, because the two must agree about the flip.

## Owner decision, 2026-09-12

**New assets only.** The mechanism ships; no existing asset is converted.

An asset opts in by adding one registration, `side-<asset>-side.json`, whose
`direction` is `east` or `west`. `full_wall_prop.load_mirrored_side()` loads it,
serves the authored wall from it directly and the opposite wall from
`RoomAssetLibrary.mirror_registration()`. Authored `side-<asset>-east/west`
registrations always win, so adopting this never overwrites or retires accepted art.

Mirroring happens in the registration rather than at draw time. The polygons are
reflected about the region's own centre line, and `RoomAssetLibrary.source_uv()`
makes the mirrored geometry sample the unmirrored source pixel, so the raster flips
with the polygons - the failure mode this proposal identified as the crux. The pivot
sits on that centre line, so width, height, outline and `wall_mount` are unchanged and
placement is untouched. Every registration draw path routes its UVs through
`source_uv()`, Studio included, so Studio and the running game cannot disagree.
North and south are never consulted; only `east` and `west` mirror.

### What a future conversion would also have to do

`default-layouts.json` addresses side registrations as library ids, for example
`library/side-research-analysis-wall-east` and `-west` at quarters 2 and 3. Retiring
an authored side file orphans those keys: `tests/test_layout_keys.py` reports
`names no registration or common asset`, and the props silently vanish from the room.
A conversion revision therefore has to repoint those layout keys as well as link the
new registration to the one it supersedes.
