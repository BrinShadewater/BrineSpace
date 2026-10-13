"""Adapt deterministic whole-source packager; preserve rejected04 evidence."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/retain_marsh_south_run_passing_source.py').read_text()
source=source.replace('passing-04','passing-05').replace('exec-746cff84-13c0-4677-b551-1b8d73a18979','exec-f135a5ba-5de8-4914-b347-105c357cac07')
source=source.replace('Retained unselected; wrong support side in complete generated figure','Retained unselected; visually correct support side, packing and whole-cycle review pending')
source=source.replace('Wrong support side','Correct side / pending').replace('Requested viewer RIGHT support, generated viewer LEFT support. Do not mirror or patch. Entire complete figure retained as rejected directional attempt.','Correct viewer RIGHT support in raw source; head/torso/grade/stride and alpha edges pending whole-cycle review.')
(ROOT/'tools/build_marsh_south_run_passing05.py').write_text(source,encoding='utf-8')
print('Prepared separate05 whole-source packager;04 retained unchanged.')
