from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1');s=(p/'prepare_extended_windows_v68.py').read_text(encoding='utf-8').replace('extended-windows-v68','local-window-v162')
s=s.replace('mapping={0:',"mapping={44:p/'local-material-phase44-v158',45:p/'local-material-phase45-v160',46:p/'local-material-phase46-v161',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[44,45,46,47,48])]")
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local44..48 window;47/48 older provisional sources').replace('pairedSources=18','pairedSources=10')
(p/'prepare_local_window_v162.py').write_text(s,encoding='utf-8')
