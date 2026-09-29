# Large room riser faces and baked wall banks — 2026-09-28

The four large rooms use the established raised-face renderer and these registered painted wall materials: Hydroponics Farm → `hydroponics_bay`, Storage Depot → `storage_bay`, Moonbay → `data_archive`, Tidal Power Plant → `tidal_condenser`. Only the screen-north edge has a 60-unit inward riser band with cap and skirt; the other edges use top-down painted hull strips. Code retains the exact four room door ports and the Moonbay/Tidal ocean face. Raised walls follow the station's Walls setting. Separate Studio wall decorations remain paused; the banks below are fixed functional fittings baked into these room views.

The four wall-bank PNGs were generated separately with the built-in image generator, true alpha, then copied unmodified to this folder. The active copies are Git LFS assets. Source outputs are retained under `C:/Users/Alex/.codex/generated_images/01a0eb04-3a39-7660-805c-735f4ede7ba0/`.

| Active asset | Source output | Native pixels | SHA-256 |
|---|---|---:|---|
| `grow_wall_bank.png` | `exec-f597cb45-8697-42c5-8e23-af425973baba.png` | 2100×749 | `935E57638243A7455FA2763D4F4ADAA339BB26CDADC4BECA5585804ED3FE448F` |
| `cargo_wall_bank.png` | `exec-39b0c189-716f-4ad4-8d9f-92b6de215e44.png` | 2100×749 | `41D5DDDB67F91A9EAECD22F24FA07D5E2F997705DF4DE024C9F1AB6206E8557C` |
| `launch_wall_bank.png` | `exec-95b40a4f-33ca-4020-8505-a1866c5eafbe.png` | 1942×809 | `CD0F4F0EE909CDF177C16729174B2516123AFA96BDAC3454C93052EE59968DC9` |
| `tidal_wall_bank.png` | `exec-d4fd070b-7341-45d3-b1d1-552bdc32bd97.png` | 1959×803 | `BF9002913C892316E39020216AC4641F3AA19F1D0C778C96F297C4244D2A3E77` |

All four RGBA sources have alpha extrema 0–255. No cleanup, crop or color transform was applied to the files. At runtime the wall banks are aspect-preservingly reduced to roughly 5 source pixels per displayed world unit, matching the established riser density; raw files and hashes remain unchanged. The accepted prop board at `docs/art-style-reference-2026-09-26.png` and the existing `assets/room-risers-v3` faces were visual references during integration, not image-generation inputs. The measured review is in `docs/LARGE_ROOM_WALL_AUDIT_2026-09-28.md`.

## Exact generation prompts

### Hydroponics

> One isolated true-transparent game sprite for a hydroponics farm riser wall art fitting in BrineSpace. A long low-profile fixed nutrient distribution manifold and crop-control bank mounted flush to a raised wall face, viewed directly overhead with shallow visible depth, front controls facing inward toward the room. Four compact valve/filter modules, dark green matte steel housing, pale mint pipework, tiny restrained green status lamps, practical access panels, no plants or pots on top. Broad horizontal silhouette about 3.5 times wider than tall, purpose-built for a narrow riser band in a top-down station room. Detailed hand-painted industrial sprite with crisp functional construction, controlled texture and matte finish consistent with an underwater station; no floor, wall background, room, windows, doorway, text, logo, fake checkerboard, gloss, bloom, isometric perspective or thick cartoon outline. Real alpha around the object and clear margins. Stylized-concept game asset.

### Storage Depot

> One isolated true-transparent game sprite for Storage Depot raised riser wall art in BrineSpace, a top-down underwater station builder. A long low-profile fixed cargo tracking and gantry service bank mounted flush to an industrial wall face: matte yellow safety rail and compact hydraulic hoist controls across dark charcoal steel panels, small mechanical tally wheels and orderly tied cable conduits, practical unlabeled indicator blocks. Directly overhead view with shallow hardware thickness, all controls and handles facing inward toward the room, broad horizontal silhouette about 3.5 times wider than tall. Detailed hand-painted industrial sprite, controlled wear and matte finish, small restrained yellow details, crisp silhouette at gameplay size. Real transparent alpha outside the single object, clear margins. No floor, wall background, room, window, doorway, text, numbers, logo, fake checkerboard, gloss, bloom, isometric rendering or thick cartoon outlines. Stylized-concept game asset.

### Moonbay

> One isolated true-transparent game sprite for Moonbay raised riser wall art in BrineSpace, a top-down underwater station builder. A long low-profile dry launch-chamber control bank mounted flush to the interior pressure wall: two heavy interlock lever housings, small cyan status indicators, a compact sonar/mission display with abstract non-text marks, insulated pipes and bolted matte steel casing. Controls and lever grips face inward toward the room. Direct overhead view with shallow hardware thickness, broad horizontal silhouette about 3.5 times wider than tall, restrained cyan against charcoal and dull steel, no water or flooding. Detailed hand-painted industrial game-sprite style, crisp functional construction and controlled texture readable at gameplay size; no bright halo or gloss. True transparent alpha around the single object and generous clear margins. No floor, background wall, room, window, doorway, submersible, crew, letters, logos, fake checkerboard, 3D render, vector style or thick cartoon outlines. Stylized-concept game asset.

### Tidal Power Plant

> One isolated true-transparent game sprite for Tidal Power Plant raised riser wall art in BrineSpace, a top-down underwater station builder. A long low-profile fixed tidal intake and generator service bank mounted flush to a raised pressure wall: two large sealed flow meters with dark round dials, heavy blue-gray pipes, compact valve wheels, a few matte ochre-yellow safety panels and practical bolted access cases. Controls face inward toward the dry room. Direct overhead view with shallow visible depth, broad horizontal silhouette about 3.5 times wider than tall, detailed hand-painted industrial game sprite with matte charcoal and dull steel, small restrained yellow details, crisp construction readable at gameplay size. True transparent alpha outside a single coherent object and clear margins. No floor, wall background, room, window, doorway, open water, people, letters, numbers, logo, fake checkerboard, glossy reflections, bloom, 3D render, vector style or thick cartoon outline. Stylized-concept game asset.

## Review

The four baked card views and native station captures were inspected at gameplay scale. The wall banks sit on sealed spans; exact door and ocean clearance and PNG decoding are checked by `test_large_room_art.gd`. All four rotations and Walls-off behavior were captured and inspected. Owner visual acceptance remains pending.
