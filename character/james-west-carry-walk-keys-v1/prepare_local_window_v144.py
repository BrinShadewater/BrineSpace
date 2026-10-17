from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_extended_windows_v68.py').read_text().replace('extended-windows-v68','local-window-v144')
s=s.replace('mapping={0:',"mapping={33:p/'local-material-phase33-v143',30:p/'knee-protection-phase30-v142',31:p/'local-material-phase31-v139',32:p/'local-material-phase32-v140',0:")
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[30,31,32,33,34])]")
s=s.replace("baseline=json.loads", "def source_for(i,mode):\n    return p/f'master-head-review-v16/{mode}-{i:03d}.png' if i==34 else mapping[i]/(mode+'-head-protected.png')\nbaseline=json.loads")
s=s.replace("mapping[i]/(mode+('-candidate.png' if i==24 else '-head-protected.png'))",'source_for(i,mode)')
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Local phase30..34 window;34 is unrepaired original').replace('pairedSources=18','pairedSources=10')
exec(compile(s,str(__file__),'exec'))
