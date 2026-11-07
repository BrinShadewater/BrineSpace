"""Prepare06 deterministic whole-source packager."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/build_marsh_south_run_passing05.py').read_text().replace('passing-05','passing-06').replace('exec-f135a5ba-5de8-4914-b347-105c357cac07','exec-15dfa08c-5b7b-4499-b566-6b67a30aba15')
(ROOT/'tools/build_marsh_south_run_passing06.py').write_text(source,encoding='utf-8')
print('Prepared06 separate whole-source packager.')
