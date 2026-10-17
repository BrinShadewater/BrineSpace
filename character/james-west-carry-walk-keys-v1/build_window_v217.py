from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_lower_window_v214.py').read_text(encoding='utf-8')
s=s.replace('lower-window-v214','lower-window-v217')
s=s.replace("{34:'lower-material-phase34-v212'}", "{35:'lower-material-phase35-v215',36:'lower-material-phase36-v216'}")
s=s.replace('i in [34]','i in [35,36]')
s=s.replace("studies=[('local',[32,33,34,35,36])]", "studies=[('local',[33,34,35,36,37])]")
s=s.replace('Lower finish phase32..36','Lower finish phase33..37')
(p/'prepare_lower_window_v217.py').write_text(s,encoding='utf-8')
