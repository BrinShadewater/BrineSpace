from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_lower_window_v211.py').read_text(encoding='utf-8')
s=s.replace('lower-window-v211','lower-window-v214')
s=s.replace("{33:'lower-material-phase33-v209'}", "{34:'lower-material-phase34-v212'}")
s=s.replace('i in [33]','i in [34]')
s=s.replace("studies=[('local',[31,32,33,34,35])]", "studies=[('local',[32,33,34,35,36])]")
s=s.replace('Lower finish phase31..35','Lower finish phase32..36').replace('pairedSources=12','pairedSources=10')
(p/'prepare_lower_window_v214.py').write_text(s,encoding='utf-8')
