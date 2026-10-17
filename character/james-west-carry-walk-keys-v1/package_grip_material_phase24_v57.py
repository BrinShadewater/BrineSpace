from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'package_grip_phase24_v56.py').read_text().replace("out=p/'case-grip-phase24-v56'","out=p/'case-grip-material-phase24-v57'")
exec(compile(s,str(__file__),'exec'))
