# Art consistency audit and portrait installation

**Follow-up implemented:** the title redraw and mirrored habitat fields were corrected after this audit. See [current fixes and comparisons](ART_FIXES_2026-09-09.md). The findings below preserve the earlier review state.

Updated: 2026-09-09 · BrineSpace · Source project, no new executable.

## Objective and acceptance

Audit art families for palette, material, tone and presentation consistency. Preserve the owner's authored room layouts and distinct departments. The [visual review board](art-consistency-2026-09-09/review.html) contains before/after portraits, all room cards, native rotations, sprite samples, habitat captures and remaining findings. [Structured audit](art-consistency-2026-09-09/audit.json).

## Accepted decisions and constraints

The owner explicitly selected the **pixel-textured V2 portrait set** for installation during this audit. BRINE V13 remains the portrait reference. Matte room materials, clinical versus industrial finishes, character identities, sparse three-to-four-asset furnishing and BRINE's restored layout exception remain authoritative. Palette anchors describe relationships; they are not a global recoloring filter.

## Current state

- `scripts/architects.gd` and `scripts/companions.gd` select all seven `character/portraits-realism-v2` portraits. Architect selection, communications, companion selection and Continue previews share those loaders. Original sources and both generated revisions remain intact; the V2 manifest records installation without altering source hashes.
- `scripts/checkpoint_preview.gd` now fits portraits proportionally instead of stretching them to a fixed rectangle.
- `tools/audit_art_consistency.py` inventories Git-visible rasters, source hashes and coarse color diagnostics. Static reference matches are hints, not a live-asset count.
- `tools/preview_art_consistency.gd` captures native habitat, portrait UI and checkpoint contexts and samples the actual merged runtime sprite packs. Run with isolated APPDATA/LOCALAPPDATA. `tools/build_art_consistency_review.py` builds the review board from those captures plus the room-render report.
- Room geometry, color sources, card mappings, department doors, fleet art, navigation badges and world tint remain unchanged after review. Current shared steel/cream construction and limited department accents are coherent. Portrait installation is this pass's production art change.

## Audit coverage and findings

| Family | Review | Decision |
|---|---|---|
| Rooms and cards | All 47 families, 188 native orientations; runtime/editor prop rectangles compared | Retain palettes and layouts; no geometry differences |
| Portraits | Eight cast identities; seven V2 sources inspected full size; architect comms and all selection rows captured at 1600×900 and 960×540 | Install owner-selected V2; retain BRINE |
| Actor sprites | 66 representative idle, walking, repair and swimming samples from seven actual runtime packs | Retain charcoal suits, department accents, ivory android and companion identities |
| Environment | Source contact sheets, seven native habitat contexts; decorative water, wreckage, rocks and vegetation | Retain subdued world tint and varied biology; detailed sources recede at runtime |
| Doors and drones | Current department concept source, current fleet atlas, assembled rooms and station context | Retain shared industrial construction; chroma-key source matting is intentional |
| UI and title | Current badge/switch sources; native title and gameplay HUD at two sizes | Retain readable badge accents; title style difference remains documented below |

The source-inventory snapshot, taken before copying review evidence into docs, contains **9,080 rasters / 346 directory families / zero decode errors**. It includes archived revisions. This is not a claim that 9,080 images are active, individually visually accepted or tested in an export. Animation review is representative, not every frame or transition. Room sheets use a read-only copy of the owner's saved layouts; personal saves and layout files were not changed.

Two visible issues remain rather than being mislabeled as consistent:

1. **Title illustration:** stronger outlines, simpler facial rendering and brighter cyan than the current portrait cast. Its existing owner cover composition and animated layers were retained. A coordinated title redraw is the strongest next art improvement; reducing saturation alone would not resolve the rendering-style difference.
2. **Habitat tiling:** salt and sulfur ground show mirrored repetition at wider views. Their palette fits, but this audit does not certify seamless tiling. Address source structure and repeated sampling together in a terrain-focused pass.

## Verification

- Full raster inventory: zero decode errors. Local CSV/JSON and logs: `output/art-consistency/`.
- Native room renderer: `RENDER COMPLETE 188`; zero editor/runtime prop rectangle differences. Six full orientation sheets visually reviewed, plus all 47 current cards.
- Environment source ledger: **21 identities / 24 immutable sources verified**, no unregistered candidates. Hash/alpha checks do not confer visual acceptance.
- Native art fixture: **ART CONSISTENCY PASS**, 33 captures, 66 sprite samples, seven source hashes and portrait consumers verified. Representative UI screenshots and all seven habitat contexts reviewed.
- `test_navigation_badges`: PASS, native, two HUD sizes; `test_title_screen`: PASS, native. Logs ending `1788986683586406900` in `output/maintenance-20260909/`.
- `test_architect_selection`: PASS; `test_compact_comms`: PASS, native. Logs ending `1788986844957798100`. Dialogue pause/restoration and explicit close remain intact.
- Continue portrait aspect correction inspected in the final native art fixture. Source PNG warnings are the existing raw-loading convention; no script errors were reported. No new export was built or validated.

## Next action

Review the installed V2 cast in the source game. For the next substantial art revision, bring the title illustration toward BRINE V13 and the installed cast while preserving its logo, tank, independent float and monitor registration. The audit and targeted consistency pass are delivered; title redraw and terrain tiling are explicitly outstanding art work.
