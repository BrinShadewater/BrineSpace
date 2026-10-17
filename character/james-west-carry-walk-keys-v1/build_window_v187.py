from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_lower_window_v185.py').read_text(encoding='utf-8').replace('lower-window-v185','lower-window-v187').replace('lower-material-phase17-v184','lower-material-phase17-v186')
(p/'prepare_lower_window_v187.py').write_text(s,encoding='utf-8')
