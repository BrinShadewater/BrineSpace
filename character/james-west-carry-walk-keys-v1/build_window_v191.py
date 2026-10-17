from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_lower_window_v187.py').read_text(encoding='utf-8').replace('lower-window-v187','lower-window-v191')
s=s.replace("{15:'lower-material-phase15-v182',16:'lower-material-phase16-v183',17:'lower-material-phase17-v186'}", "{18:'lower-material-phase18-v188',19:'lower-material-phase19-v189',20:'lower-material-phase20-v190'}").replace('i in [15,16,17]','i in [18,19,20]')
s=s.replace("studies=[('local',[14,15,16,17,18])]", "studies=[('local',[17,18,19,20,21])]").replace('Lower finish phase14..18','Lower finish phase17..21')
(p/'prepare_lower_window_v191.py').write_text(s,encoding='utf-8')
