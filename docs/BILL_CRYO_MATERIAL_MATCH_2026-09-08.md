# Bill recovery pod material match

Bill's six recovery frames now use assets/material-polish-cryo-recovery-v1/bill/wake-0.png through wake-5.png. Both architect_cryo_art.gd and the generic ward renderer load this pack. The original pose order, 418x627 canvas, (210,560) pivot and seven-second playback remain unchanged. No recovery behavior or NPC movement code changed.

The initial candidate had a baked checkerboard and remains preserved as a rejected runtime source. An imagegen background-only correction produced bill-wake-white.png. Read-only neutral silhouette registration plus a native Godot transparent render produced the usable frames; the generated PNG itself was not raster-edited by scripts. Exact prompts, source hash, frame hashes and geometry are retained. output/register_bill_wake_material.py and output/bake_bill_wake_material.gd record the export procedure. Re-export requires a new destination because the exporter refuses overwrite.

All six exported PNGs have actual alpha and fit within the fixed frame bounds. All six Bill poses were visually inspected through the native architect renderer at 150-unit pod width, showing no obvious background blocks or clipped silhouettes. The explicit renderer produced 18 occupied frames and three recovered-state renders without ERROR; only Bill's material frames changed. This proves source loading and per-frame rendering, not full game transition acceptance. The open glass retains a narrow highlight and must remain consistent when matching the other architects.

Veld and Branforth still use their original occupied pod materials and are next. The broader wall, riser, biological-room, shared-prop and animation material goal remains incomplete. No executable rebuild.
