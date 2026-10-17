from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'audit_case_components_v5.py').read_text().replace('for i in (0,8,12,20,28,36,44,48):','for i in (1,2,3,4,5,6,7,9,10,11):')
source=source.replace("p/f'walk{i:02d}-belt-anatomy-v4.png'","p/f'walk{i:02d}-dense-carry-v6-original.png'").replace("p/f'walk{i:02d}-case-master-v5.png'","p/f'walk{i:02d}-dense-carry-v6.png'")
source=source.replace('case-master-v5-components.json','dense-start-v6-components.json')
exec(compile(source,str(p/'audit_case_components_v5.py'),'exec'))
