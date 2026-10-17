from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'build_eight_keys.py').read_text()
start=source.index('sources=[');end=source.index('\n',start)
source=source[:start]+"sources=[p/f'walk{index:02d}-case-master-v5.png' for index in indices]"+source[end:]
source=source.replace('eight-key-','eight-key-case-master-v5-')
source=source.replace('Earlier8..36meters still uncorrected.','Actual standing carry reference is original-selected-idle-based provisional local3, not a newly owner-locked master. Case/grip/material/tool occlusion and complete motion remain provisional.')
exec(compile(source,str(p/'build_eight_keys.py'),'exec'))
