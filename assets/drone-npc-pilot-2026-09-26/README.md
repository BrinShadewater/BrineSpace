# Construction drone motion pilot

South-facing review only. Not installed in gameplay; approved-v10 is unchanged.

- `review/motion-preview.gif`: idle rotor, swimming rotor, and coarse tool cycle, enlarged and at provisional gameplay size.
- `review/tool-contact-sheet.png`: four generated tool keys.
- `review/bible-comparison-light.png` and `bible-comparison-dark.png`: accepted v10 versus revised pilot at equal widths, with hash-verified locked machinery exports.
- `review/construction-room-scale.png`: production room and Bill, approved source overlaid at 28.9, 48 and 69.12 world units. This is a scale comparison, not navigation or occlusion acceptance.
- `manifest.json`, `frames/`, `strips/`: 53 frame files across three clips. Four authored tool poses; repeated holds are not additional articulated poses.
- `sources/`: accepted reference copy, original generated v1, corrected generated v2, status lamp and exact generation prompts. v1 retained as the rejected bright-cyan comparison.

Rebuild: `python assets/drone-npc-pilot-2026-09-26/build_pilot.py`.
Style board: `python assets/drone-npc-pilot-2026-09-26/audit_style.py`.

## Bible audit

Authority: `docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md`, its locked catalog,
and accepted v10 sources. Department UI cyan is not the paint specification.

| Check | Finding |
|---|---|
| Cyan | v1 was too saturated/bright (median saturation .565 versus v10 .412). v2 reduces it to .290, slightly grayer than v10. Lens emission remains distinct. v2 is a review candidate, not an exact palette match. |
| Density | Export mapping is .34 world units/library pixel. Provisional 69.12-unit hull is approximately 203 source/export pixels; no small PNG upscaling. The accepted v10 85px drone was a motion-study proportion, not an approved NPC footprint. Density mapping does not certify painted detail quality. |
| Theme | Heavy mechanical underwater ROV, charcoal/steel, localized cyan, gripper and work tool retained. No yellow paint or spaceship features added. |
| Perspective | Steep overhead south-facing view is consistent with v10. No opposite views have been generated or mirrored. Camera-angle matching is visual, not measured 3D geometry. |
| Painted finish | Revised poses remain smoother and more strongly outlined than the locked pump/valve family. They need refinement before a full batch. |

## Verification and limits

Generic sprite manifest validator: zero errors/warnings. All exported frames RGBA,
nonempty and inside transparent borders. Both independent library reference hashes
verified. Light/dark boards and four pose keys visually inspected. Native scale
fixture captured successfully using a scratch APPDATA and copied layouts; owner
save recursive path/size/mtime fingerprints unchanged. This was a metadata
fingerprint, not a claim of cryptographic content comparison.

The 120-frame GIF packages the timing study; continuous playback has not been
visually accepted. Tool motion has only four keys and conspicuous timed holds.
Swimming currently tests rotor activity, not full thrust/attitude/body travel.
Separate build/repair actions, contact targets, other directions, final size,
runtime effects, navigation and live docking remain open. Blue operational lamp
only in this pilot; red stopped and yellow charging semantics remain requirements.

Next: refine material/palette against v10 before authoring intermediate arm poses
and directional views. Do not promote this pilot over the accepted art bundle.
