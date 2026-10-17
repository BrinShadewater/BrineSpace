from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_lower_window_v198.py').read_text(encoding='utf-8').replace('lower-window-v198','lower-window-v203')
s=s.replace("{21:'lower-material-phase21-v197',22:'lower-material-phase22-v193',23:'lower-material-phase23-v194',24:'lower-material-phase24-v195'}", "{25:'lower-material-phase25-v199',26:'lower-material-phase26-v200',27:'lower-material-phase27-v201',28:'lower-material-phase28-v202'}").replace('i in [21,22,23,24]','i in [25,26,27,28]')
s=s.replace("studies=[('local',[20,21,22,23,24,25])]", "studies=[('local',[24,25,26,27,28,29])]").replace('Lower finish phase20..25','Lower finish phase24..29')
(p/'prepare_lower_window_v203.py').write_text(s,encoding='utf-8')
