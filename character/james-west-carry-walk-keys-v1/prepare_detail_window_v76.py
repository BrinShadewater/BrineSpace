from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','detail-window-v76')
s=s.replace("mapping={0:","mapping={2:p/'detail-phase2-v75',3:p/'master-material-phase3-v70',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('detail',[1,2,3])]")
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Detail candidate phase1/2/3 window only').replace('pairedSources=18','pairedSources=6')
exec(compile(s,str(__file__),'exec'))
