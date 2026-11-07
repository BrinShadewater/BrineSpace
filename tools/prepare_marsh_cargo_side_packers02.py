"""Build whole redraw packers, preserving01 sources and exact endpoints."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for f in ['east','west']:
    s=(ROOT/f'tools/pack_marsh_cargo_{f}_unload01.py').read_text()
    s=s.replace(f'{f}-unload-01',f'{f}-unload-02')
    (ROOT/f'tools/pack_marsh_cargo_{f}_unload02.py').write_text(s)
print('side02 complete-figure packers prepared;01 originals preserved')
