from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'package_start_bridge_v15.py').read_text().replace('start-bridge-v15','start-bridge-v17')
exec(compile(source,str(p/'package_start_bridge_v15.py'),'exec'))
