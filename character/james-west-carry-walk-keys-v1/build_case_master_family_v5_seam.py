from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'build_case_master_family_v5.py').read_text().replace("sources=[p/f'walk{index:02d}-case-master-v5.png' for index in indices]","sources=[p/('walk12-case-master-v5-seam.png' if index==12 else f'walk{index:02d}-case-master-v5.png') for index in indices]")
source=source.replace("'eight-key-case-master-v5-'","'eight-key-case-master-v5-seam-'")
exec(compile(source,str(p/'build_case_master_family_v5.py'),'exec'))
