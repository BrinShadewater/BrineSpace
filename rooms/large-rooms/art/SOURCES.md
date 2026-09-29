# Large room painted installations — 2026-09-28

Four individual true-alpha PNGs were generated with the built-in image generator and copied unmodified into this folder. They replace the code-drawn centerpieces. Moonbay also uses its mini-sub sprite at a small scale outside the station during missions. `common.gd` continues to own the 768-unit hull and exact ports; each room view owns the painted asset's fixed position and navigation blocker. The existing card baker renders from those same views. No external reference image was supplied to generation; the accepted prop style board at `docs/art-style-reference-2026-09-26.png` was used for subsequent visual comparison, not as an image-generation input.

| Asset | Source output | Native pixels | SHA-256 |
|---|---|---:|---|
| `grow_beds.png` | `exec-ad71191a-233c-4704-86f9-6a8772e7e753.png` | 1157×1359 | `32DDC274992AA3B3840C03223911D86B1DBB3EE8FB37756E29F009CA24EFABB1` |
| `cargo_gantry.png` | `exec-0074fdd3-464f-4512-89dc-2fd0938d9689.png` | 1254×1254 | `B95F73F6970BA7EFCD85AAB8EA069D1FC22D494A58A8000A30005812E10EFC4B` |
| `mini_sub.png` | `exec-2d4e521e-edae-4f59-8e71-1a5e07aa9206.png` | 1816×866 | `16FC1C038ABC8C1FA6A82C0596DBD2453A84C40326365A86D5E340C93A6D5171` |
| `tidal_turbine.png` | `exec-1e6664b8-681f-4a98-8b54-212d44ad693d.png` | 1254×1254 | `82B0B112579A7273837003A32B9396A671BAB777DD33D256478EB10DEBA6DFF4` |

All four source outputs remain under `C:/Users/Alex/.codex/generated_images/01a0eb04-3a39-7660-805c-735f4ede7ba0/`. The workspace copies are the active assets. No background removal, crop, or color transform was applied. Alpha extrema are 0–255 for every source.

## Exact generation prompts

### Grow beds

> Create a single game-ready transparent PNG sprite: a massive fixed hydroponics grow-bed installation for a top-down underwater station builder. Four long parallel planted troughs aligned vertically in a broad rectangular machine, connected by a narrow central irrigation/service spine and a few transverse pipes. Mature but orderly leafy edible plants in deep varied greens, visibly supported by matte dark green steel trays, nutrient channels, bolted frames, restrained pale mint irrigation tubing. Camera directly overhead with a slight shallow view of hardware thickness, matching detailed hand-painted industrial game sprites: controlled texture, crisp functional silhouette, readable at small gameplay scale, muted matte materials and restrained highlights. Object isolated with true transparent background and generous clear margins; no floor, wall, room, doors, people, shadows outside the object, letters, labels, logos, checkerboard, fake transparency, glossy 3D, vector style, or thick cartoon outline. Keep the overall silhouette about 0.85 width to height, visually one fixed installation spanning a four-cell room. Stylized-concept game asset.

### Cargo gantry

> Create one game-ready true-transparent cutout sprite for BrineSpace, a top-down underwater station builder: a massive fixed cargo gantry installation. A rectangular overhead yellow ochre industrial gantry frame encloses orderly dark steel storage racks and large freight containers in three functional bays, with one central crane beam, trolley, suspended lifting hook and rails. Readable single cohesive installation from directly overhead with a shallow view of hardware thickness. Matte muted yellow safety paint only on the gantry, dark charcoal and dull steel structure, restrained warm crate tones. Detailed hand-painted industrial game-sprite style, crisp functional silhouette, controlled painted texture, subtle contact shading, native-scale readability, no gloss, no metallic sparkle. About square footprint; composed so a clear perimeter walkway can exist around it in a four-cell room. Isolated object with transparent background and generous clear margins. No room, floor, wall, doors, crew, typography, logos, fake checkerboard, photorealistic 3D or vector style. Stylized-concept game asset.

### Mini-sub

> Create one game-ready true-transparent cutout sprite for BrineSpace, a top-down underwater station builder: a compact human-piloted mini-submarine seen directly overhead, long horizontal silhouette, rounded blunt pressure bow on LEFT pointing toward ocean, two modest rear thruster pods on RIGHT, central observation canopy and practical top hatch. Dry dock state, no water anywhere on or around it. Muted cyan-blue accent panels on mostly matte slate steel pressure hull, dark glass, bolted seams, access handles, small functional status lamps but no glow bloom. Industrial retro-futurist underwater vehicle, detailed hand-painted game-sprite treatment, shallow visible thickness, crisp functional silhouette and controlled texture readable at small gameplay scale. It should fit on rails within a large four-cell dry hangar; one isolated object centered in a wide rectangular composition, about 2.1 times wider than tall. Real transparent background with generous clear margins. No dock, floor, rails, wall, doors, characters, ocean, letters, logos, fake checkerboard, photorealistic 3D, vector style or thick cartoon outline. Stylized-concept game asset.

### Tidal turbine

> Create one game-ready true-transparent cutout sprite for BrineSpace, a top-down underwater station builder: a massive fixed tidal power turbine assembly viewed directly overhead. One large circular twelve-vane rotor inside a heavy square industrial containment frame, central dark axle hub, two major longitudinal pipe manifolds and bolted service housings attached to the frame. This is a practical maintained internal generator, dry room, not an exposed open-water prop. Engineering yellow appears as restrained safety panels and small hub detail; bulk surfaces are matte charcoal steel and dull warm gray with muted blue-green pipe accents. Detailed hand-painted industrial game-sprite style, shallow hardware thickness, crisp geometry and strong silhouette readable at small gameplay scale, controlled texture, no gloss, no metallic sparkle, no bloom. Square footprint, one cohesive fixed installation centered in the image, true transparent background with clear margin around all sides. No floor, room, doors, people, text, logos, fake checkerboard, photo 3D, vector, or thick cartoon outline. Stylized-concept game asset.

## Review

Reviewed the source alpha bounds, all four 512 px baked cards, 16 rotated card frames, four native station screenshots in `output/large-room-review/station/`, and Moonbay's launch and at-sea frames in `output/moonbay-review/`. Geometry remains code-authored. Gameplay tests and owner visual acceptance are tracked in `docs/LARGE_ROOMS_HANDOFF_2026-09-28.md`.
