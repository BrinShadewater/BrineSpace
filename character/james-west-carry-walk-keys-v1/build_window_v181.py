from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_lower_window_v178.py').read_text(encoding='utf-8').replace('lower-window-v178','lower-window-v181')
s=s.replace("{10:'lower-material-phase10-v176',11:'lower-material-phase11-v177'}", "{13:'lower-material-phase13-v179',14:'lower-material-phase14-v180'}").replace('i in [10,11]','i in [13,14]')
s=s.replace("studies=[('local',[8,9,10,11,12,13])]", "studies=[('local',[12,13,14,15,16])]").replace('Lower finish phase8..13','Lower finish phase12..16').replace('pairedSources=12','pairedSources=10')
(p/'prepare_lower_window_v181.py').write_text(s,encoding='utf-8')
