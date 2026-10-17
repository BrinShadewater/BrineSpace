from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_local_window_v141.py').read_text().replace('local-window-v141','local-window-v144').replace("29:p/'local-material-phase29-v136',30:p/'local-material-phase30-v138'","33:p/'local-material-phase33-v143',30:p/'knee-protection-phase30-v142'").replace('[29,30,31,32,33]','[30,31,32,33,34]').replace('if i==33','if i==34').replace('phase29..33 window;33','phase30..34 window;34')
(p/'prepare_local_window_v144.py').write_text(s)
