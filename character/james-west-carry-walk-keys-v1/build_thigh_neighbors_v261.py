from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'package_thigh_v256.py').read_text(encoding='utf-8')
(p/'package_thigh_v260.py').write_text(s.replace('thigh-construction-phase12-v256','thigh-construction-phase14-v260').replace('phase==12','phase==14'),encoding='utf-8')
s=(p/'prepare_thigh_window_v257.py').read_text(encoding='utf-8').replace('thigh-window-v257','thigh-window-v261')
s=s.replace("{12:'thigh-construction-phase12-v256'}", "{11:'thigh-construction-phase11-v258',12:'thigh-construction-phase12-v256',13:'thigh-construction-phase13-v259',14:'thigh-construction-phase14-v260'}").replace('i in [12]','i in [11,12,13,14]')
(p/'prepare_thigh_window_v261.py').write_text(s,encoding='utf-8')
