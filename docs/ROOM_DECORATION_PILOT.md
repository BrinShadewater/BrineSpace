> Superseded: the owner rejected the uniform paired layout. Current work and evidence are in [Organic room composition](ORGANIC_ROOM_COMPOSITION.md). The original sources below remain available for reuse.

# Small-prop decoration pilot

Requested rooms: Maintenance Bay, Research Lab and Crew Lounge.

Each now has four new illustrated accessory designs, instanced as eight small static props clustered in pairs at the main equipment/furniture fronts. Maintenance has toolboxes, parts bins, cable reels and repair cases. Research has specimen trays, transport coolers, supply trolleys and sterile bins. Lounge has blanket/book baskets, plants, drink trays and personal bags. Department-colored work-area mats/trim provide another scale cue.

The main hosts use92x54 footprints, centered118 units from each axis before rotation, to reserve accessory space. Decorations have22x6 footprints,22-unit rendered width and their own depth order. Their centers are recomputed relative to their south-facing host after wall-containment adjustment: x offsets21 in either direction,20 units ahead of the front. This keeps them near the relevant equipment across rotations. Main equipment effects remain unchanged; decorations are deliberately static.

Built-in image generation made three1254-square RGBA atlases. Raw images remain intact, with actual alpha preserved. Source rectangles, hashes and placement are recorded in rooms/production-ten/decor/manifest.json; exact prompts are in prompts.json. The source-rectangle review corrected top-right atlas crops that included the next row's edges. Card-decor-v3 is selected for all three rooms and their export component lists include the atlas hashes.

The first layout was rejected: it hid props behind large equipment and overlapped some footprints when rotated. The second scattered layout was also replaced by host-relative clusters. Logs and intermediate cards are retained. Room v3 fixtures pass at1600:12 assemblies, four rotations, per-host state comparisons, containment, non-overlap and center-to-door paths. Final cropped-atlas revision is checked again at1280. Scene-level missing environment assets from concurrent development are logged separately and must not be represented as an entirely error-free game run.

This is the first decoration pilot for these three rooms, not a completed decoration pass on the other rooms. No new room costs, production, discoveries or saves are added.

## Final results

All three final room fixtures pass at verified1280x720, with zero assertions
and no ERROR entries. The mixed-station fixture verifies10 room donors,20
source/card decodes and all3 decoration atlas hashes/decodes. Bill reaches15/15
placed rooms through37 reciprocal transitions and2825 checked movement steps.
The final scene logs are clean; the environment errors described above apply
only to earlier intermediate runs. Evidence: output/production-ten/decor-final-verification.json.
No new Windows packaged-export claim is made for this revision.

## Owner rejection

The owner rejected this composition as repeated paired accessories rather than an organic room. Passing tests above remain technical evidence only. Superseding work is tracked in docs/ORGANIC_ROOM_ROLLOUT.json; none of these three pilots is organically accepted.

### Lounge relationship correction, organic v1 (incomplete)

Removed repeated accessory pairs and equal-size furniture normalization. One reading rug, one basket, a dining plant and personal bags now accompany specific activities. The drinks tray draws at source tabletop anchor (920,310), inheriting the host clamp and scale, without a floor collision footprint. Selected card: `crew_lounge-card-organic-v1.png`. Native fixture `output/production-ten/lounge-organic-v2` passed four rotations, containment and 1092 route samples; unrelated wreck environment texture errors remain in the log, so this is not a clean overall runtime pass. Card reviewed at 512 native pixels: relationships improved but the four-corner composition remains too sparse. This revision is not organic-composition acceptance. Standing lights, new supporting furniture and utility/floor detailing are still pending.
