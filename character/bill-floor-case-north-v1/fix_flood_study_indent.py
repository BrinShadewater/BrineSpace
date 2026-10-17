from pathlib import Path
import shutil
P=Path(__file__).resolve().parent;R=P.parents[1]
dest=P/'flood-motion-first-interval';dest.mkdir(exist_ok=True)
for source in [P/'flood_readability_v2.gd',R/'tests/test_bill_floor_case_flood_motion_v2.gd',R/'output/bill-floor-case-flood-motion-v2/native.log',R/'output/bill-floor-case-flood-motion-v2/validation.json']:
 if not (dest/source.name).exists():shutil.copy2(source,dest/source.name)
v=P/'flood_readability_v2.gd';v.write_text(v.read_text().replace(chr(9),' '))
print('Retained parse failure and normalized copied wake indentation.')
