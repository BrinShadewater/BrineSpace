from pathlib import Path
p = Path(__file__).resolve().parent
source = (p / 'build_dense_cycle_v9.py').read_text()
source = source.replace("    if i == 3: return", "    if i in (21, 34, 45, 46): return p / f'walk{i:02d}-material-v10.png'\n    if i == 3: return")
source = source.replace('dense-cycle-v9-', 'dense-cycle-v10-')
exec(compile(source, str(p / 'build_dense_cycle_v9.py'), 'exec'))
