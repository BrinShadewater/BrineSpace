from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_lower_window_v203.py').read_text(encoding='utf-8').replace('lower-window-v203','lower-window-v208')
s=s.replace("{25:'lower-material-phase25-v199',26:'lower-material-phase26-v200',27:'lower-material-phase27-v201',28:'lower-material-phase28-v202'}", "{29:'lower-material-phase29-v204',30:'lower-material-phase30-v205',31:'lower-material-phase31-v206',32:'lower-material-phase32-v207'}").replace('i in [25,26,27,28]','i in [29,30,31,32]')
s=s.replace("studies=[('local',[24,25,26,27,28,29])]", "studies=[('local',[28,29,30,31,32,33])]").replace('Lower finish phase24..29','Lower finish phase28..33')
(p/'prepare_lower_window_v208.py').write_text(s,encoding='utf-8')
