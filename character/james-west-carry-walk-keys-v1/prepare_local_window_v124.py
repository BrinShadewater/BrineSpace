from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','local-window-v124')
s=s.replace('mapping={0:',"mapping={18:p/'local-material-phase18-v120',19:p/'local-material-phase19-v122',20:p/'local-material-phase20-v123',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[18,19,20,21])]")
s=s.replace("baseline=json.loads", "def source_for(i,mode):\n    return p/f'master-head-review-v16/{mode}-{i:03d}.png' if i==21 else mapping[i]/(mode+'-head-protected.png')\nbaseline=json.loads")
s=s.replace("mapping[i]/(mode+('-candidate.png' if i==24 else '-head-protected.png'))",'source_for(i,mode)')
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local phase18..21 window;21 is unrepaired original').replace('pairedSources=18','pairedSources=8')
exec(compile(s,str(__file__),'exec'))
