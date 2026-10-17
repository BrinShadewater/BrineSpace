from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','local-window-v115')
s=s.replace('mapping={0:',"mapping={12:p/'lower-material-phase12-v111',13:p/'local-material-phase13-v113',14:p/'local-material-phase14-v114',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[12,13,14,15])]")
s=s.replace("baseline=json.loads", "def source_for(i,mode):\n    return p/f'master-head-review-v16/{mode}-{i:03d}.png' if i==15 else mapping[i]/(mode+'-head-protected.png')\nbaseline=json.loads")
s=s.replace("mapping[i]/(mode+('-candidate.png' if i==24 else '-head-protected.png'))",'source_for(i,mode)')
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local phase12..15 window;15 is unrepaired original').replace('pairedSources=18','pairedSources=8')
exec(compile(s,str(__file__),'exec'))
