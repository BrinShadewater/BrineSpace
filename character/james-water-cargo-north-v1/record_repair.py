from pathlib import Path
import shutil,json
p=Path('C:/Users/Alex/Documents/Brine Space/character/james-water-cargo-north-v1')
original="C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-01f0c9c6-acdd-4703-9edb-2c1f3eb53184.png"
if not (p/'source-v1.png').exists():
 shutil.copyfile(p/'source.png',p/'source-v1.png')
 shutil.copytree(p/'source-crops',p/'source-crops-v1',dirs_exist_ok=True)
 shutil.copyfile(p/'source-audit.json',p/'source-audit-v1.json')
shutil.copyfile(original,p/'source-v2.png')
shutil.copyfile(original,p/'source.png')
(p/'source-v2-prompt.txt').write_text("Repair this NORTH-facing, rear-view James underwater source animation sheet while preserving the exact eighteen bodies' drawing density, anatomy, materials and three-row six-column layout. Transparent background. Correct the invented flower/radiation emblem on EVERY backpack: use the actual small muted ochre circle divided by a simple cross from the supplied water/standing master, with four angular quarters, not a flower, six petals or radiation symbol. On the TOP ROW and first MIDDLE ROW frame, orient the blowtorch nozzle FORWARD NORTH, toward the top of the image, ahead of his head along his swimming heading. Right glove holds it ahead and to the right of his head; barrel points upward, small blue-white flame points upward, not sideways right. Keep the arms and posture prone and buoyant. Improve MIDDLE ROW frames1 to4 ONLY: show a real incremental pickup, first extinguishing and stowing torch on belt while left hand reaches toward loose graphite case ahead, next both hands reach opposite side handles, next pull rigid case closer, next settle in firm grip. Frame0 remains neutral top-row0, frame5 matches bottom-row0. Keep the case chest-width and original four silver corner guards; no shrinking or yaw. Both hands remain anatomically attached, wrench stays on belt on its original side in every frame. Bottom row has restrained compact alternating kick with hands always gripping case. No new details, no black halo, no glow background, no standing or kneeling or fake floor. Exact master compact limbs, close bent boots with visible soles, camera35-degree elevated orthographic.",encoding='utf-8')
(p/'source-v2-origin.json').write_text(json.dumps(dict(original=original,method='builtin_imagegen_north_tool_backpack_pickup_repair'),indent=2)+'\n')
