from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_lower_window_v238.py').read_text(encoding='utf-8').replace('lower-window-v238','lower-window-v241')
s=s.replace("{0:'lower-material-phase0-v234',1:'lower-material-phase1-v235',2:'lower-material-phase2-v236',3:'lower-material-phase3-v237'}", "{30:'knee-material-phase30-v240'}").replace('i in [0,1,2,3]','i in [30]')
s=s.replace("studies=[('local',[47,48,0,1,2,3,4])]", "studies=[('local',[28,29,30,31,32])]").replace('Lower finish seam47/48/0..4','Knee finish phase28..32')
(p/'prepare_lower_window_v241.py').write_text(s,encoding='utf-8')
