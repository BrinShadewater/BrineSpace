from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_lower_window_v191.py').read_text(encoding='utf-8').replace('lower-window-v191','lower-window-v196')
s=s.replace("{18:'lower-material-phase18-v188',19:'lower-material-phase19-v189',20:'lower-material-phase20-v190'}", "{21:'lower-material-phase21-v192',22:'lower-material-phase22-v193',23:'lower-material-phase23-v194',24:'lower-material-phase24-v195'}").replace('i in [18,19,20]','i in [21,22,23,24]')
s=s.replace("studies=[('local',[17,18,19,20,21])]", "studies=[('local',[20,21,22,23,24,25])]").replace('Lower finish phase17..21','Lower finish phase20..25').replace('pairedSources=10','pairedSources=12')
(p/'prepare_lower_window_v196.py').write_text(s,encoding='utf-8')
