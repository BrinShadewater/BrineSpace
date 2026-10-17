from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_lower_window_v217.py').read_text(encoding='utf-8')
s=s.replace('lower-window-v217','lower-window-v221')
s=s.replace("{35:'lower-material-phase35-v215',36:'lower-material-phase36-v216'}", "{37:'lower-material-phase37-v218',38:'lower-material-phase38-v219',39:'lower-material-phase39-v220'}")
s=s.replace('i in [35,36]','i in [37,38,39]')
s=s.replace("studies=[('local',[33,34,35,36,37])]", "studies=[('local',[36,37,38,39,40])]")
s=s.replace('Lower finish phase33..37','Lower finish phase36..40')
(p/'prepare_lower_window_v221.py').write_text(s,encoding='utf-8')
