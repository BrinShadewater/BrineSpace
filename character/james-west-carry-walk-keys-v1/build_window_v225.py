from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_lower_window_v221.py').read_text(encoding='utf-8').replace('lower-window-v221','lower-window-v225')
s=s.replace("{37:'lower-material-phase37-v218',38:'lower-material-phase38-v219',39:'lower-material-phase39-v220'}", "{40:'lower-material-phase40-v222',41:'lower-material-phase41-v223',42:'lower-material-phase42-v224'}")
s=s.replace('i in [37,38,39]','i in [40,41,42]')
s=s.replace("studies=[('local',[36,37,38,39,40])]", "studies=[('local',[39,40,41,42,43])]")
s=s.replace('Lower finish phase36..40','Lower finish phase39..43')
(p/'prepare_lower_window_v225.py').write_text(s,encoding='utf-8')
