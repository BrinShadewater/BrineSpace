from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1');s=(p/'prepare_extended_windows_v68.py').read_text(encoding='utf-8').replace('extended-windows-v68','local-window-v171')
s=s.replace('mapping={0:',"mapping={47:p/'local-material-phase47-v163',48:p/'local-material-phase48-v164',1:p/'local-material-phase1-v168',2:p/'local-material-phase2-v169',3:p/'local-material-phase3-v170',4:p/'lower-material-phase4-v99',0:")
s=s.replace("0:p/'master-material-v49'","0:p/'local-material-phase0-v167'").replace(",1:p/'master-material-phase1-v66'",'').replace(",47:p/'master-material-phase47-v67'",'').replace(",48:p/'master-material-phase48-v55'",'')
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[47,48,0,1,2,3,4])]")
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local47/48/0/1/2/3/4 repaired-start seam source window').replace('pairedSources=18','pairedSources=14')
(p/'prepare_local_window_v171.py').write_text(s,encoding='utf-8')
