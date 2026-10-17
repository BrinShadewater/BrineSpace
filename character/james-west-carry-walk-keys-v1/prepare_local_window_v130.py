from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','local-window-v130')
s=s.replace("22:p/'master-material-phase22-v64'","22:p/'local-material-phase22-v126'")
s=s.replace("23:p/'master-material-phase23-v58'","23:p/'local-material-phase23-v128'")
s=s.replace("24:p/'sleeve-phase24-v63'","24:p/'local-material-phase24-v129'")
s=s.replace("'-candidate.png' if i==24 else '-head-protected.png'","'-head-protected.png'")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[22,23,24,25])]")
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local phase22..25 window with earlier phase25 candidate').replace('pairedSources=18','pairedSources=8')
exec(compile(s,str(__file__),'exec'))
