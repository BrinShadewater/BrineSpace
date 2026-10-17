from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_lower_window_v181.py').read_text(encoding='utf-8').replace('lower-window-v181','lower-window-v185')
s=s.replace("{13:'lower-material-phase13-v179',14:'lower-material-phase14-v180'}", "{15:'lower-material-phase15-v182',16:'lower-material-phase16-v183',17:'lower-material-phase17-v184'}").replace('i in [13,14]','i in [15,16,17]')
s=s.replace("studies=[('local',[12,13,14,15,16])]", "studies=[('local',[14,15,16,17,18])]").replace('Lower finish phase12..16','Lower finish phase14..18')
(p/'prepare_lower_window_v185.py').write_text(s,encoding='utf-8')
