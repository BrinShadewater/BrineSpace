from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1');s=(p/'prepare_extended_windows_v68.py').read_text(encoding='utf-8').replace('extended-windows-v68','local-window-v159')
s=s.replace('mapping={0:',"mapping={39:p/'local-material-phase39-v152',40:p/'local-material-phase40-v154',41:p/'local-material-phase41-v155',42:p/'local-material-phase42-v156',43:p/'local-material-phase43-v157',44:p/'local-material-phase44-v158',45:p/'master-material-phase45-v71',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[39,40,41,42,43,44,45])]")
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local39..45 window;45 older provisional source').replace('pairedSources=18','pairedSources=14')
(p/'prepare_local_window_v159.py').write_text(s,encoding='utf-8')
