from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','local-window-v109')
s=s.replace('mapping={0:',"mapping={9:p/'local-material-phase9-v105',10:p/'local-material-phase10-v107',11:p/'local-material-phase11-v108',12:p/'master-material-phase12-v51',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[9,10,11,12])]")
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local consecutive phase9..12 material window').replace('pairedSources=18','pairedSources=8')
exec(compile(s,str(__file__),'exec'))
