from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'package_material_v49.py').read_text().replace("out=p/'master-material-v49'","out=p/'master-material-phase12-v51'").replace('bare-000.png','bare-012.png').replace('helmet-000.png','helmet-012.png')
exec(compile(s,str(__file__),'exec'))
