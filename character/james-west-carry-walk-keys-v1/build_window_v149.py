from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1');s=(p/'prepare_local_window_v147.py').read_text().replace('local-window-v147','local-window-v149').replace("36:p/'master-material-phase36-v53'","36:p/'local-material-phase36-v148'").replace('36 older provisional candidate','36 rebuilt local candidate');(p/'prepare_local_window_v149.py').write_text(s)
