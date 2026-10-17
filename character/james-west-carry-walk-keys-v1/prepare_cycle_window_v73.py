from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','cycle-window-v73')
s=s.replace("mapping={0:","mapping={2:p/'master-material-phase2-v69',3:p/'master-material-phase3-v70',45:p/'master-material-phase45-v71',46:p/'master-material-phase46-v72',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('seam',[45,46,47,48,0,1,2,3])]")
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Cycle boundary45/46/47/48/0/1/2/3 window only').replace('pairedSources=18','pairedSources=16')
exec(compile(s,str(__file__),'exec'))
