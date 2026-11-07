# Revised decoration integration

All 40 current database identities use the revised decoration libraries. The
37 furnished views share the existing floor and dressing hooks; three corridor
identities use their actual hull geometry. `rooms.json` is the native capture
inventory; `manifest.json` records card hashes and library dependencies.

Replacements:

- Hab and lounge rugs: woven and braided textiles, fitted to the existing pads.
- Clinical preparation areas and bed feet: medical mats; consultation uses a
  briefing mat. Engineering workstations use tread mats; cargo and drone service
  tables use pallet plates. Growing areas use drainage and drip trays.
- Existing floor access covers and equipment grates now use reviewed PNG art.
- Equipment service runs retain their endpoints and bridge covers, with tiled
  floor cable/pipe sprites. Existing operating indicators remain code-owned.
- Corridor call points, emergency cabinets and edge drains replace drawn glyphs.
- Low north hull segments receive small department fittings and ocean slit
  windows, fitted within the existing 16-unit wall. Tall library props are not
  a reason to increase wall height. Door gaps and omitted shared edges remain
  owned by the geometry renderer.
- Rare baked interiors receive flush aisle access covers; BRINE's chamber has
  a floor alignment ring. Airlock changing benches have boot trays.

The replacements preserve aspect ratio in fitted pads. Services tile along
authored paths. Nothing is added to the collision or actor registries. Larger
machinery, furniture, character art and animated equipment retain their existing
renderers. These are decorative assets, not new interactive controls.

## Verification

- `tools/review_decoration_integration.gd`: 40 rooms, 320 rotation/state renders,
  37 shared-edge captures, all current cards and nine corridor variant cards.
- `tests/playtest_low_wall_station.gd`: 28 native station captures, zero failures.
- `tools/audit_room_dressing_hosts.gd -- --check-mat-bounds`: resolved hosts and
  existing mat envelopes checked against all 37 furnished runtime views.
- `output/decoration-integration/` contains native room and contact-sheet review.
- New raster exports are covered by Git LFS; production export presets include
  raw PNG/JSON dependencies. A new executable was not built in this pass.

Run the capture tool with Godot's native renderer (not headless). It regenerates
only this integration's card exports; earlier cards and source packs remain intact.
`tools/decoration_contact_sheet.gd` assembles four native overview pages.

The first capture run freed cached meshes while its canvas still referenced them.
The tool now clears that canvas before releasing a room; the final render run has
no renderer errors. Existing legacy image-loader export warnings elsewhere in the
project are outside this art replacement.
