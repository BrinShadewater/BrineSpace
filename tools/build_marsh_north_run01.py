"""Use the complete-sheet packager with North's actual146 neutral calibration."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/build_marsh_west_run01.py').read_text().replace('west','north').replace('West','North').replace('exec-18ce8756-64cb-4a2f-a4fd-d86cb2787e38','exec-35310d7b-3b5c-4960-8e3e-fdaebde77cc0').replace('scale=147/','scale=146/').replace("'neutralOccupiedTargetHeight':147","'neutralOccupiedTargetHeight':146").replace('repeats foreground leading half-strides','repeats left-support contact/passing halves').replace('repeats near-leading half strides. Bare temple/material/body improved','repeats left-support contact/passing halves. Rear identity/material/body reviewed')
exec(compile(source,str(ROOT/'tools/build_marsh_north_run01.py'),'exec'),{'__file__':str(ROOT/'tools/build_marsh_north_run01.py'),'__name__':'__main__'})
