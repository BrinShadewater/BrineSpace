from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_thigh_window_v248.py').read_text(encoding='utf-8').replace('thigh-window-v248','thigh-window-v252').replace("{48:'thigh-construction-phase48-v245'", "{47:'thigh-construction-phase47-v250',48:'thigh-construction-phase48-v245'").replace('i in [48,0,1,2]','i in [47,48,0,1,2]')
(p/'prepare_thigh_window_v252.py').write_text(s,encoding='utf-8')
