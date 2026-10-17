from pathlib import Path
import json
p=Path('character/james-west-carry-walk-keys-v1');s=(p/'prepare_extended_windows_v68.py').read_text(encoding='utf-8').replace('extended-windows-v68','full-gait-review-v172')
a=s.index('mapping=');b=s.index('baseline=',a)
s=s[:a]+"ledger=json.loads((p/'material-repair-progress.json').read_bytes())\nassert ledger['candidatePhases']==49 and not ledger['remainingSourcePhases']\ndef source_for(i,mode):\n    return r/ledger['states'][i]['candidateSources'][mode]['file']\n"+s[b:]
s=s.replace("studies=[('middle',[22,23,24,25,26]),('seam',[47,48,0,1])]","studies=[('full',list(range(49)))]")
s=s.replace("mapping[i]/(mode+('-candidate.png' if i==24 else '-head-protected.png'))",'source_for(i,mode)')
s=s.replace('loop=False','loop=True').replace('Middle22..26 and seam47/48/0/1 windows only; not full49source motion or normal selection.','Full49 staged source cycle, original timings, looping; normal selection unchanged.').replace('pairedSources=18','pairedSources=98')
s=s.replace('rows[state.id][-1].get_image().get_data(),"Finite endpoint clamps"','rows[state.id][0].get_image().get_data(),"Full cycle wraps to first source"')
s=s.replace('Isolated consecutive middle/seam source windows, paired exact sources/clocks/rulers/pivots. Not full49 walking cycle/controller/rooms/Continue.','Full49 isolated looping source cycle, paired exact sources/clocks/rulers/pivots; not normal controller/rooms/Continue or continuous visual acceptance.')
s=s.replace('elapsed+=hold', '''for cycle in [1,2]:
                    check(player.frame_at_elapsed(state.id,elapsed+hold*.5+player.cycle_seconds(state.id,gear)*cycle,gear).get_image().get_data()==source.get_data(),"Multiple-cycle midpoint exact")
                elapsed+=hold''')
(p/'prepare_full_gait_v172.py').write_text(s,encoding='utf-8')
