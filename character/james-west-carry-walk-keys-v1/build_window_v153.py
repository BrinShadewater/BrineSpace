from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','local-window-v153')
s=s.replace('mapping={0:',"mapping={36:p/'local-material-phase36-v148',37:p/'local-material-phase37-v150',38:p/'local-material-phase38-v151',39:p/'local-material-phase39-v152',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[36,37,38,39,40])]")
s=s.replace('baseline=json.loads',"def source_for(i,mode):\n    return p/f'master-head-review-v16/{mode}-{i:03d}.png' if i==40 else mapping[i]/(mode+'-head-protected.png')\nbaseline=json.loads")
s=s.replace("mapping[i]/(mode+('-candidate.png' if i==24 else '-head-protected.png'))",'source_for(i,mode)')
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local36..40 window;40 unrepaired original').replace('pairedSources=18','pairedSources=10')
(p/'prepare_local_window_v153.py').write_text(s)
