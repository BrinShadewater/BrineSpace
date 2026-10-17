from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_lower_window_v225.py').read_text(encoding='utf-8').replace('lower-window-v225','lower-window-v232')
s=s.replace("{40:'lower-material-phase40-v222',41:'lower-material-phase41-v223',42:'lower-material-phase42-v224'}", "{43:'lower-material-phase43-v226',44:'lower-material-phase44-v227',45:'lower-material-phase45-v228',46:'lower-material-phase46-v229',47:'lower-material-phase47-v230',48:'lower-material-phase48-v231'}")
s=s.replace('i in [40,41,42]','i in [43,44,45,46,47,48]')
s=s.replace("studies=[('local',[39,40,41,42,43])]", "studies=[('local',[42,43,44,45,46,47,48])]")
s=s.replace('Lower finish phase39..43','Lower finish phase42..48').replace('pairedSources=10','pairedSources=14')
(p/'prepare_lower_window_v232.py').write_text(s,encoding='utf-8')
