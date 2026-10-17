# Painted construction animation

Rooms and straight, corner and T hallways assemble in work-driven stages:
foundation joists, deck plates, pressure rails, destination hull and fittings.
Materials use neutral matte overhead artwork, clipped to the actual footprint.
The destination artwork retains its own palette and physical scale. Progress,
pauses, holds, build costs, scheduler and save data keep existing behavior.

`materials-v1.png` is the preserved generated master; `prompts.json` records its
instructions. `bake.py` crops curated atlas rows and exports three 512px strips.
`manifest.json` pins source and runtime hashes. PNGs use Git LFS.

Verification: paid crew construction and construction fitting routes pass;
final native review covers three room examples, all 12 hallway orientations,
20 progress frames, repeated paused-frame equality and unchanged orders.
Evidence: `output/construction-art-20260930-005102/summary.json` and
`output/construction-art-20260930-005431/summary.json` (2,774 owner files unchanged).
The environment loader passes 92 checks. Its two isolated runs observed concurrent
changes to real session breadcrumbs/logs; their fingerprint gates did not pass.
Evidence: `output/construction-art-20260930-005947/summary.json` and
`output/construction-art-20260930-010020/summary.json`. No owner files were restored.

Preview: `output/construction-art-v1/building-animation-v1.gif` and
`building-stages-v1.png`. These are native captures at physical display density.
Owner visual acceptance and playable-release acceptance remain pending.

Run `python assets/environment/construction-v1/verify.py` with the real game closed
for a quiet owner fingerprint interval. `--native-only` and `--assets-only` narrow
the check; every mode sets scratch APPDATA and LOCALAPPDATA.
