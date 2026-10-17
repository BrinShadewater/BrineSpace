from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','lower-window-v100')
s=s.replace("mapping={0:","mapping={3:p/'textile-detail-phase3-v83',4:p/'lower-material-phase4-v99',5:p/'lower-material-phase5-v98',6:p/'local-material-phase6-v93',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('lower',[3,4,5,6])]")
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Lower material candidate phases3..6 window only').replace('pairedSources=18','pairedSources=8')
exec(compile(s,str(__file__),'exec'))
