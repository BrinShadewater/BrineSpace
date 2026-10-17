from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_lower_window_v208.py').read_text(encoding='utf-8')
s=s.replace('lower-window-v208','lower-window-v211')
s=s.replace("{29:'lower-material-phase29-v204',30:'lower-material-phase30-v205',31:'lower-material-phase31-v206',32:'lower-material-phase32-v207'}", "{33:'lower-material-phase33-v209'}")
s=s.replace('i in [29,30,31,32]','i in [33]')
s=s.replace("studies=[('local',[28,29,30,31,32,33])]", "studies=[('local',[31,32,33,34,35])]")
s=s.replace('Lower finish phase28..33','Lower finish phase31..35')
(p/'prepare_lower_window_v211.py').write_text(s,encoding='utf-8')
