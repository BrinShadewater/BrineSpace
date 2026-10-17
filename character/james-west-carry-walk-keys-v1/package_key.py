from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'package_pose.py').read_text().replace("p/'base.png'","p/inputs['baseFile']")
exec(compile(source,str(p/'package_pose.py'),'exec'))
