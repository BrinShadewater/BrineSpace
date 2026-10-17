from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_lower_window_v238.py').read_text(encoding='utf-8').replace('lower-window-v238','thigh-window-v248')
s=s.replace("{0:'lower-material-phase0-v234',1:'lower-material-phase1-v235',2:'lower-material-phase2-v236',3:'lower-material-phase3-v237'}", "{48:'thigh-construction-phase48-v245',0:'thigh-construction-phase0-v244',1:'thigh-construction-phase1-v246',2:'thigh-construction-phase2-v247'}").replace('i in [0,1,2,3]','i in [48,0,1,2]')
s=s.replace("studies=[('local',[47,48,0,1,2,3,4])]", "studies=[('local',[47,48,0,1,2,3])]").replace('Lower finish seam47/48/0..4','Unselected thigh construction47/48/0..3').replace('pairedSources=14','pairedSources=len(sources)')
(p/'prepare_thigh_window_v248.py').write_text(s,encoding='utf-8')
