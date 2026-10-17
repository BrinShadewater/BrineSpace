from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'prepare_lower_window_v175.py').read_text(encoding='utf-8').replace('lower-window-v175','lower-window-v178')
s=s.replace("return p/'lower-material-phase9-v174'/(mode+'-head-protected.png') if i==9 else r/ledger['states'][i]['candidateSources'][mode]['file']", "return p/({10:'lower-material-phase10-v176',11:'lower-material-phase11-v177'}[i])/(mode+'-head-protected.png') if i in [10,11] else r/ledger['states'][i]['candidateSources'][mode]['file']")
s=s.replace("studies=[('local',[8,9,10,11,12])]", "studies=[('local',[8,9,10,11,12,13])]")
s=s.replace('Lower finish phase8..12','Lower finish phase8..13').replace('pairedSources=10','pairedSources=12')
(p/'prepare_lower_window_v178.py').write_text(s,encoding='utf-8')
