# BrineSpace hull UI v1

Installed 2026-10-01 from the UI auditions and polish accepted for integration in this chat.

60 distinct transparent 96 x 96 icon masters (84 px maximum silhouette) use smooth downsampling at the UI display size. The original 32px exports were rejected for poor density and enlarged navigation pixelation. Four transparent source atlases live beside the exports. Regenerate individual icons from these atlases with `output/ui-quality-2026-10-01/rebuild_icons.gd`; do not enlarge a smaller export. PNG files use the repository Git LFS rules.

The native `scripts/ui_hull_style.gd` draws uniform matte grey rails, tiny recessed bolts, petrol faces and shallow raised/pressed states. Pressed indicators are dim blue; disabled indicators are dim red with an unchanged grey frame. Text remains live, bold Barlow Semi Condensed, with slightly higher vertical placement. Native geometry avoids stretching a baked frame or baking labels into textures.

`ui_icons.gd` names every complete runtime PNG path. `resource_icons.gd` shares that registry. The atlases are source assets, not runtime dependencies. Original room cards and original character portraits remain in use.

## Source lineage

Built-in image generation produced transparent exports from the polished concept sheets:

- Resources: exec-06d0b592-a4c1-4249-8868-526f75ab4e26.png
- Hazards/actions: exec-d7d6180c-6c43-457f-a65a-92a8f0d0e10a.png
- Draft/crew: exec-61ca5d5b-7684-4900-9580-e3f0e54fbd27.png (corrected transparency pass)
- Navigation/utility: exec-c14e7bb9-6ade-4bd4-9473-02a627ee3810.png

Concepts and their prompts: `output/ui-polish-2026-09-30/REVIEW.md` and `PROMPTS.txt`. Slicing measurements and native evidence: `output/ui-integration-2026-09-30/`. Rights remain reserved under the project NOTICE.md.
