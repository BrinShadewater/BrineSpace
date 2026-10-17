from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','local-window-v134')
s=s.replace('mapping={0:',"mapping={27:p/'local-material-phase27-v133',0:")
for old,new in [("24:p/'sleeve-phase24-v63'","24:p/'local-material-phase24-v129'"),("25:p/'master-material-phase25-v59'","25:p/'local-material-phase25-v131'"),("26:p/'master-material-phase26-v65'","26:p/'local-material-phase26-v132'")]:s=s.replace(old,new)
s=s.replace("'-candidate.png' if i==24 else '-head-protected.png'","'-head-protected.png'")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[24,25,26,27,28])]")
s=s.replace("baseline=json.loads", "def source_for(i,mode):\n    return p/f'master-head-review-v16/{mode}-{i:03d}.png' if i==28 else mapping[i]/(mode+'-head-protected.png')\nbaseline=json.loads")
s=s.replace("mapping[i]/(mode+('-head-protected.png'))",'source_for(i,mode)')
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local phase24..28 window;28 is unrepaired original').replace('pairedSources=18','pairedSources=10')
exec(compile(s,str(__file__),'exec'))
