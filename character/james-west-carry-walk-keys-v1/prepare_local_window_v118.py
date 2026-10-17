from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','local-window-v118')
s=s.replace('mapping={0:',"mapping={14:p/'local-material-phase14-v114',15:p/'local-material-phase15-v116',16:p/'local-material-phase16-v117',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[14,15,16,17])]")
s=s.replace("baseline=json.loads", "def source_for(i,mode):\n    return p/f'master-head-review-v16/{mode}-{i:03d}.png' if i==17 else mapping[i]/(mode+'-head-protected.png')\nbaseline=json.loads")
s=s.replace("mapping[i]/(mode+('-candidate.png' if i==24 else '-head-protected.png'))",'source_for(i,mode)')
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local phase14..17 window;17 is unrepaired original').replace('pairedSources=18','pairedSources=8')
exec(compile(s,str(__file__),'exec'))
