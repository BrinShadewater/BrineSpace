from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_extended_windows_v68.py').read_text(encoding='utf-8').replace('extended-windows-v68','lower-window-v175')
a=s.index('mapping=');b=s.index('baseline=',a)
s=s[:a]+"ledger=json.loads((p/'material-repair-progress.json').read_bytes())\ndef source_for(i,mode):\n    return p/'lower-material-phase9-v174'/(mode+'-head-protected.png') if i==9 else r/ledger['states'][i]['candidateSources'][mode]['file']\n"+s[b:]
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('local',[8,9,10,11,12])]")
s=s.replace("mapping[i]/(mode+('-candidate.png' if i==24 else '-head-protected.png'))",'source_for(i,mode)')
s=s.replace('Middle22..26 and seam47/48/0/1 windows only','Lower finish phase8..12 source window only').replace('pairedSources=18','pairedSources=10')
(p/'prepare_lower_window_v175.py').write_text(s,encoding='utf-8')
