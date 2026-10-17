from pathlib import Path
p=Path(__file__).resolve().parent
for phase,version in [(0,249),(47,250)]:
 s=(p/'package_thigh_v244.py').read_text(encoding='utf-8').replace('thigh-construction-phase0-v244',f'thigh-construction-phase{phase}-v{version}').replace('if phase==0',f'if phase=={phase}').replace('[48,0,1,2]','[47,48,0,1]')
 (p/f'package_thigh_v{version}.py').write_text(s,encoding='utf-8')
