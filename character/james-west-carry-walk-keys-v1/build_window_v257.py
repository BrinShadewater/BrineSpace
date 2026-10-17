from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_lower_window_v241.py').read_text(encoding='utf-8').replace('lower-window-v241','thigh-window-v257').replace("{30:'knee-material-phase30-v240'}", "{12:'thigh-construction-phase12-v256'}").replace('i in [30]','i in [12]').replace("studies=[('local',[28,29,30,31,32])]", "studies=[('local',[10,11,12,13,14])]").replace('Knee finish phase28..32','Unselected diagonal thigh phase10..14').replace('pairedSources=14','pairedSources=len(sources)')
(p/'prepare_thigh_window_v257.py').write_text(s,encoding='utf-8')
