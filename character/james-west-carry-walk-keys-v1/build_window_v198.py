from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_lower_window_v196.py').read_text(encoding='utf-8').replace('lower-window-v196','lower-window-v198').replace('lower-material-phase21-v192','lower-material-phase21-v197')
(p/'prepare_lower_window_v198.py').write_text(s,encoding='utf-8')
