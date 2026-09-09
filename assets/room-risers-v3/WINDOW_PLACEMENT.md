# Future window placement

These six risers intentionally contain no baked windows. Add windows later as independent wall props. The cyan gallery boxes are proposed mounting areas, not holes or already installed windows.

Coordinates below are `[x, y, width, height]` in the unrotated room wall's world space. Exact source-pixel and world rectangles are in registrations.json. Transform with the wall for the chosen orientation.

| Room | Left window box | Right window box |
|---|---|---|
| Reactor | -136.8, -247.2, 61.3, 21.1 | 74.1, -247.2, 61.3, 21.1 |
| Cryo Chamber | -136.8, -247.2, 61.3, 21.1 | 74.1, -247.2, 61.3, 21.1 |
| Data Archive | -136.8, -247.2, 61.3, 21.1 | 74.1, -247.2, 61.3, 21.1 |
| Storage Bay | -136.8, -247.2, 61.3, 21.1 | 74.1, -247.2, 61.3, 21.1 |
| Crew Lounge | -136.8, -247.2, 61.3, 21.1 | 74.1, -247.2, 61.3, 21.1 |
| Research Lab | -136.8, -247.2, 61.3, 21.1 | 74.1, -247.2, 61.3, 21.1 |

- Each box is approximately 61 × 21 world units. A complete frame up to 58 × 18 leaves a small margin; preserve its original aspect ratio.
- Keep the central doorway reserve `[-46, -252, 92, 60]` unobstructed. The existing door is 72 units wide.
- Keep pipes, sockets, trim and small end-mounted fittings visible. Do not expand a window beyond its marked box without checking the source artwork.
- Verify the actual window prop in the furnished room and every intended rotation before accepting placement. Tall room furniture can obscure a mounting area, especially in the research lab. These reservations are not a guarantee of unobstructed visibility.
- Window scenery, transparency and interaction belong to the later window prop implementation. No structural opening is implemented by this pack.
