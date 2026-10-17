from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1');s=(p/'prepare_extended_windows_v68.py').read_text(encoding='utf-8').replace('extended-windows-v68','local-window-v165')
s=s.replace('mapping={0:',"mapping={46:p/'local-material-phase46-v161',47:p/'local-material-phase47-v163',48:p/'local-material-phase48-v164',1:p/'textile-detail-phase1-v82',0:")
s=s.replace(",1:p/'master-material-phase1-v66'",'').replace(",47:p/'master-material-phase47-v67'",'').replace(",48:p/'master-material-phase48-v55'",'')
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[46,47,48,0,1])]")
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local46/47/48/0/1 seam source window;0 older provisional source').replace('pairedSources=18','pairedSources=10')
(p/'prepare_local_window_v165.py').write_text(s,encoding='utf-8')
