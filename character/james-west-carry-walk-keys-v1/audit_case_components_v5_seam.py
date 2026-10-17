from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'audit_case_components_v5.py').read_text().replace("b=components(p/f'walk{i:02d}-case-master-v5.png')","b=components(p/('walk12-case-master-v5-seam.png' if i==12 else f'walk{i:02d}-case-master-v5.png'))")
source=source.replace('case-master-v5-components.json','case-master-v5-seam-components.json')
exec(compile(source,str(p/'audit_case_components_v5.py'),'exec'))
