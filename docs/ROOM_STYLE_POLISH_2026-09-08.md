# Room style polish handoff

Updated: September 8, 2026 · BrineSpace · second room-art polish pass

## Objective and acceptance
Bring recent room art closer to the established retro-industrial station style. [Review the twelve native before/after comparisons](../output/room-style-polish-2026-09-08/index.html), with Bill at runtime scale and expandable installed-room views. Owner style acceptance remains pending.

## Accepted decisions and constraints
Use the owner-approved Tidal material quality, retaining departmental colors and individual functions. Preserve inward-facing south geometry, registered placement frames, functional bays, source originals and personal layouts. No new gameplay, furniture placement or room-route claims.

## Current state
- Twelve south-bank repaints in `assets/room-style-polish-v1`: Mycelium, Crew Hab, Research, Clone, Quarantine, Medical Treatment, Xeno, Biology, Emergency Isolation, Crew Lounge, Radio and Maintenance. Separate geometry, finish and department references prevented the shared pale-green cabinet treatment from spreading across unrelated rooms.
- Materials now distinguish warm cream/wood/cloth habitation, cream/teal clinical equipment, grey-green Life Support, charcoal/orange engineering and charcoal/burgundy communications/containment. Restrained vents, seams and service panels provide construction detail while keeping operational faces north.
- Twelve existing `side-*-south.json` registrations updated; previous registrations retained. Exact proportional placement frames preserved; maximum source-boundary drift is 0.0072 of registered width. Raw PNGs were not raster-edited during registration.
- `rooms/whole-room/room_door.gd` now renders recessed sliding leaves, seals, handles and threshold details. Insets sample a quiet patch of the existing riser hull texture and clip as the leaves retract.
- Forty-four furnished-room cards refreshed into `assets/room-style-polish-v1/cards`; corridor variants retained. Full catalog has 47 rooms / 167 stills; material gallery has 87 standardized records after adding twelve new native alpha exports and review records.
- Reproduction: `register_room_style_polish.py`, `capture_style_polish.gd` + UID, `record_style_polish_review.py`, `build_style_polish_gallery.py`. Existing native review/capture/card tools accept output directories. Previous review packages remain available.

## Verification
- `studio-final.log`: native owner-note fixture PASS, including R/F, autosave, repeated variant application, Listening movement and distinct door frames; final closed/half/open images reviewed.
- `comparisons-v2.log`: twelve native alpha exports and equal-world-scale comparisons with Bill PASS; all twelve reviewed. Ten current default south-wall room placements reviewed; Radio/Quarantine remain selectable south tray variants rather than default placements.
- `catalog-final.log`: 47 identities / 167 native stills PASS. All 162 registration source hashes match. Card consistency passes all 47 primary/grid/variant mappings and PNG decoding.
- Twelve review records verify source/export/reference hashes, native dimensions, transparent exterior corners and retained opaque rear-body probes. Gallery links and JavaScript syntax checked. This does not replace occupied crew-route or exported-build acceptance.
- Personal layout file preserved; tests use isolated paths. Earlier failed fixture logs are retained and are not acceptance evidence.

## Next action
Owner can annotate the polish page and export notes. Further direction should distinguish material changes from new construction or layout requests. Older standalone installation studies remain separate work; this pass does not install the entire historical candidate library.
