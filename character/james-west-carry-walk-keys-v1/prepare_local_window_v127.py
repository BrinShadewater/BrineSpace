from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','local-window-v127')
s=s.replace('mapping={0:',"mapping={20:p/'local-material-phase20-v123',21:p/'local-material-phase21-v125',0:")
s=s.replace("22:p/'master-material-phase22-v64'","22:p/'local-material-phase22-v126'")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[20,21,22,23])]")
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local phase20..23 window with earlier phase23 candidate').replace('pairedSources=18','pairedSources=8')
exec(compile(s,str(__file__),'exec'))
