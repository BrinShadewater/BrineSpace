# Shaped corridor risers and crew helmets

September 26, 2026. Owner correction: corridor, corner and tee rooms are not square rooms and require footprint-specific riser treatment. Persist this constraint in future integrations.

The preview now draws actual CorridorGeometry hull/floor outlines and CorridorDressing returns, bevels and entry exclusions, using the room's canonical rotation offset. Straight passages, L bends and T junctions keep their native narrow footprints. The 35-unit corridor riser contract is retained rather than applying the 79-unit full-room wall. Registered grey wall material supplies the hull trim. Intact decorated side bays are placed at preserved aspect ratio only on eligible north-facing horizontal boundary runs, with margins and no entrance coverage. Thin side returns and concave corners remain undecorated. This is a modular preview assembly, not newly generated whole-room bitmaps or live-game adoption. Corridor actor walking was not added.

Gallery cards for these three IDs now show actual hull captures and a Rotate shape control for all four facings. Full-room north/window modes do not apply to these shape captures. Native Shape preview opens the chosen rotation. Existing flat masters remain source artwork, not shape templates.

Airlock: built-in imagegen edited only the helmet bay using character/major-bill-v3/frames/helmet/idle-south/000.png as the character reference. Three rigid charcoal shells with broad face openings and neck collars replace respirator masks. Original wall preserved; exact prompt in airlock-prompt.txt; selected RGBA in airlock.png; source/prompt/reference hashes and measured face in registrations.json. The registration builder reapplies this override after polish-v2.

Validation: isolated full session 4da8b2828fce4a7ba541f0c651be505d passed 47 designs, 44 furnished walking checks, 185 standard states plus 12 corridor rotations, zero clearance failures, no logged errors and unchanged owner-save fingerprint. Visually reviewed all 12 corridor rotations in shape-review.png and furnished airlock helmet scale. Browser corner card and rotate control checked. Owner visual acceptance and production integration remain separate.

## Tee repetition correction

Replaced alternating repeated fittings with one arrows/map/emergency-kit composition on the long wall and one distinct fitting per visible split arm. No duplicate decorative subjects within a facing. Native tee-only session 3fd5cef5994b4aaca00db35e1595c798 passed with unchanged owner saves; all four rotations visually reviewed. Gallery cache version refreshed. Preview-only.

## Direction-aware markings

Corridor-family shape previews now replace baked arrow/map bays with native painted route symbols derived from rotated hull mouth positions. Arrows use screen/map directions and point only toward actual exits. Each rotation is asserted against independently defined RoomDatabase door masks, including the straight corridor quarter-turn offset. Tee, corner and straight isolated runs passed all twelve direction combinations (sessions 014498b186cb411a9b06edfc589f2279, 8f2ccf0b6ec948e0b2f77e42c6de0abb, 2de81865b0d0469488a38b0cc3cfe898); owner saves unchanged. Tee north/south junction markings and corner turn visually checked. Source raster markings remain historical source artwork; preview assembly no longer uses them. Preview-only.
