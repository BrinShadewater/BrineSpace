from pathlib import Path
import shutil,json
p=Path("C:/Users/Alex/Documents/Brine Space/character/james-water-turn-north-east-v1")
original="C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-2c2da48d-732b-469d-aca5-03f1990f47c3.png"
if not (p/'source-v1.png').exists():
 shutil.copyfile(p/'source.png',p/'source-v1.png')
 shutil.copytree(p/'source-crops',p/'source-crops-v1',dirs_exist_ok=True)
 shutil.copyfile(p/'source-audit.json',p/'source-audit-v1.json')
 shutil.copyfile(p/'registration.json',p/'registration-v1.json')
shutil.copyfile(original,p/'source-v2.png')
shutil.copyfile(original,p/'source.png')
(p/'source-v2-prompt.txt').write_text("Repair ONLY the TOP ROW full body swimming turn in reference 1. Preserve the bottom row helmet heads exactly, with transparent background. The next two references are the exact selected bare and helmet swim endpoints, which govern anatomy and material. Six top-row poses are north to east, yaw 0,18,36,54,72,90 degrees. Use the SAME orthographic elevated 35 degree camera and buoyant prone body pitch as endpoints. Correct the current disproportionate lengths: keep the same actual physical skull, neck-to-waist, thigh, shin and boot lengths across all poses. Compact body and moderately bent knees exactly like supplied endpoints. Do not lengthen the legs or straighten the knees beyond the endpoint bend. Shoulders and legs must never expand midturn. Both arms stay extended FORWARD together along his travel heading, hands together ahead of head; no hanging or side-reaching arm, no stroking or waving. Rotate whole body in yaw gradually, including head, chest, belt, legs and arms as one coherent swimmer, no sudden view-angle jump. Keep original muted graphite, soft silver and LIMITED muted gold accents. Preserve wrench attached to belt. Do not invent extra gold straps or bands on the legs or backpack; use exact original suit details from endpoints. Top first and last pose should match provided endpoint anatomy and limb pose. Use one source drawing density for entire sheet, with consistent physical head and joint dimensions. Bottom-row helmet heads and empty transparent space preserved exactly. Six clear components each row, generous gutters, no text, no clipping.",encoding='utf-8')
(p/'source-v2-origin.json').write_text(json.dumps(dict(original=original,method='builtin_imagegen_body_repair',preserveHelmetDonors='source-crops-v1'),indent=2)+'\n')
