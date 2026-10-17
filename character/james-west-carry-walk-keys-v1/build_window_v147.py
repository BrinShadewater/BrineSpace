from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','local-window-v147')
s=s.replace('mapping={0:',"mapping={33:p/'local-material-phase33-v143',34:p/'local-material-phase34-v145',35:p/'local-material-phase35-v146',36:p/'master-material-phase36-v53',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[33,34,35,36,37])]")
s=s.replace('baseline=json.loads',"def source_for(i,mode):\n    return p/f'master-head-review-v16/{mode}-{i:03d}.png' if i==37 else mapping[i]/(mode+'-head-protected.png')\nbaseline=json.loads")
s=s.replace("mapping[i]/(mode+('-candidate.png' if i==24 else '-head-protected.png'))",'source_for(i,mode)')
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local33..37 window;36 older provisional candidate,37 unrepaired original').replace('pairedSources=18','pairedSources=10')
(p/'prepare_local_window_v147.py').write_text(s)
