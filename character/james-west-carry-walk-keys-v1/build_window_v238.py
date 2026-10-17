from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_lower_window_v232.py').read_text(encoding='utf-8').replace('lower-window-v232','lower-window-v238')
s=s.replace("{43:'lower-material-phase43-v226',44:'lower-material-phase44-v227',45:'lower-material-phase45-v228',46:'lower-material-phase46-v229',47:'lower-material-phase47-v230',48:'lower-material-phase48-v231'}", "{0:'lower-material-phase0-v234',1:'lower-material-phase1-v235',2:'lower-material-phase2-v236',3:'lower-material-phase3-v237'}")
s=s.replace('i in [43,44,45,46,47,48]','i in [0,1,2,3]')
s=s.replace("studies=[('local',[42,43,44,45,46,47,48])]", "studies=[('local',[47,48,0,1,2,3,4])]")
s=s.replace('Lower finish phase42..48','Lower finish seam47/48/0..4')
(p/'prepare_lower_window_v238.py').write_text(s,encoding='utf-8')
