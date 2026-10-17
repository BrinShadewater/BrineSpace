from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','extended-detail-window-v89')
s=s.replace("mapping={0:","mapping={2:p/'textile-detail-phase2-v78',3:p/'textile-detail-phase3-v83',4:p/'master-detail-phase4-v85',5:p/'master-detail-phase5-v86',6:p/'master-detail-phase6-v87',7:p/'master-detail-phase7-v88',0:")
s=s.replace("1:p/'master-material-phase1-v66'","1:p/'textile-detail-phase1-v82'")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('detail',[1,2,3,4,5,6,7])]")
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Detail candidate phases1..7 window only').replace('pairedSources=18','pairedSources=14')
exec(compile(s,str(__file__),'exec'))
