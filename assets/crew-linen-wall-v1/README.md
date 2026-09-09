# Crew linen wall and hamper handoff

Updated: 2026-09-08. Ongoing BrineSpace wall/prop production.

## Objective and direction

Add domestic utility furnishing to complement Crew Hab's existing beds/lounge:
linen storage, clothing repair and a small supporting hamper. Use warm matte
cream, walnut, muted rust/olive fabric and quiet charcoal hardware. The artwork
does not introduce a laundry simulation or new crew action.

## Current state

- `wall.png`: 1774x887 RGBA; fitted linen shelves, ventilated cupboard, repair
  counter, utility storage and a return bag. Width 320, visible height 76.20 units.
- `hamper.png`: 1227x1282 RGBA; canvas hamper, folded linens, push handle, folded
  wooden lip and casters. Width 34, visible height 49.54 units.

Wall V1 and hamper V2 are selected standalone candidates. Hamper V1 is retained
as rejected for silvery frame/caster highlights. V2 makes hardware matte without
globally darkening warm fabrics, but changed original RGBA into opaque RGB.
Exact built-in imagegen prompts, immutable sources and hashes are recorded.

## Verification and workflow findings

The source checkerboards contain dark neutral cells around 100-130; a copied
195 threshold would leave background. Read-only neutral100 vector registration
isolates these sources; this is not a universal threshold for pale furniture.
The hamper's enclosed handle opening uses reviewed seed (600,205). Native exports
retain cream towels and fabric while clearing exterior and undercarriage.

Both source-hash/size/alpha checks pass in `output/crew-linen-wall.log` and
`output/crew-linen-hamper.log`, with no ERROR/SCRIPT ERROR. Both 1040x900 boards
were visually inspected at native scale and in detail on light/dark grounds.
Handle/undercarriage alpha samples are zero; frame and bag samples remain present.
`manifest.json` binds the sources, exports, references and review images.

The skill records source-specific darker-background inspection, and the bible
records the relative scale and domestic activity grouping. No render-tool change
was needed for this batch. Candidate review does not imply owner acceptance.

## Next action

Select wall orientation/placement and the hamper's service position, then validate
wall contact, floor collision, routes and card consumers before installation.
The assets are not installed; existing production rooms and gameplay are unchanged.
The broader wall/prop production goal remains active.
