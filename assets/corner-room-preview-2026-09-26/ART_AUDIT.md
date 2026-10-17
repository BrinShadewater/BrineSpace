# Room preview art audit

Scope: five props in layout.json and their native room rendering, September 26, 2026. Compared with accepted science cabinetry, wood bookcase and upholstered sofa. Native comparison boards: art-audit-light.png and art-audit-dark.png. No source art changed.

## Density and filtering
Preview places every prop at 0.34 world units per export pixel, approximately 2.94 pixels/world unit. This convention matches the established reference-family scale approximately; it does not prove consistent world proportions. Props are painted sprites, not coarse pixel art. Characters retain their distinct accepted sprite identity and renderer scale; do not resample them to the prop ratio.

Audit found the external Study canvas did not explicitly select nearest filtering even though the room node does. Since that external canvas performs the draw calls, set its texture_filter explicitly to NEAREST to match the live grid. Re-ran native verification and visually checked revised-open.png afterward. Native reference boards avoid zoom/filter ambiguity.

## Style and color
Supply shelf is the closest reference match: muted painted metal, readable bands and restrained texture. Server broadly matches, with more noticeable diagonal scuffs than the reference. Reading chair is a simpler, cleaner interpretation of the accepted upholstery; slate blue and wood arms fit the palette, without needing the sofa's brass decoration or heavy wear.

Wood corner counter is noticeably lighter and more golden than the accepted bookcase. A slight shift toward darker, less yellow wood would tighten consistency. Sink counter's large pale surface is compatible with science cabinetry, but broad uniform door faces and limited tonal variation make it flatter/cleaner than the reference. Subtle painted variation and stronger construction shading would help more than extra scratches or global darkening. The pale worktop also draws considerable attention against this dark reactor shell; that is a contrast/composition observation, not a ban on pale materials.

## Perspective and room fit
Square-room counter footprint and straight rear edges now suit room axes. The long return still reads as a flat strip with its vertical volume mostly represented by the end face; it is less convincing than the standalone reference furniture. This remains the clearest perspective/construction weakness. The chair's diagonal facing was requested and is intentional; it should not be forced square to match the cabinets.

In the real room render the counters read as compact cabinets; visual compatibility does not certify standing work height. Whole-L single-depth sorting can hide a nearby character's upper body incorrectly. This was observed during preview setup and avoided by moving stationary crew for the screenshot, not fixed in the asset. Production use needs split depth regions or equivalent occlusion registration. Existing movement tests use provisional fixture footprints and do not establish that visual occlusion is correct.

## Result
Broad family match, not exact visual parity. Priorities: improve L-return depth and working-height readability; tone down golden wood; add restrained painted depth to the sink cabinet. Preserve the shelf and chair unless owner requests changes. Native preview checks pass after filtering fix, and owner saves remain unchanged. No production integration or artwork repaint performed during audit.
