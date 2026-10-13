from pathlib import Path
R=Path(__file__).resolve().parent.parent
source=(R/'tests/test_veld_east_original_motion_probe_v1.gd').read_text(encoding='utf-8')
source=source.replace('veld-east-original-motion-probe-v1','veld-east-original-motion-probe-v2')
source=source.replace('for n in range(65):','for n in range(66):')
source=source.replace('var t:float=n*cycle/32.0','''var phase_sample:=0.0
    if n>0 and n<65:
     var local_index:int=(n-1)%32
     var local_cycle:int=(n-1)/32
     var durations:Array=player.timing["carry-east"].durations
     for j in range(local_index):phase_sample+=float(durations[j])/1000.0
     phase_sample+=float(durations[local_index])/2000.0+local_cycle*player.cycle_seconds("carry-east",equipment)
    elif n==65:phase_sample=2*player.cycle_seconds("carry-east",equipment)
    var t:float=phase_sample/player.cycle_seconds("carry-east",equipment)*cycle''')
source=source.replace('float(n)/32.0*player.cycle_seconds("carry-east",equipment)','phase_sample')
source=source.replace('n in [1,31,33,63]','n in [1,32,33,64,65]')
(R/'tests/test_veld_east_original_motion_probe_v2.gd').write_text(source,encoding='utf-8')
runner=(R/'tools/run_veld_east_original_motion_probe_v1.py').read_text(encoding='utf-8').replace('motion_probe_v1','motion_probe_v2').replace('motion-probe-v1','motion-probe-v2')
(R/'tools/run_veld_east_original_motion_probe_v2.py').write_text(runner,encoding='utf-8')
print('New midpoint fixture written; failed boundary-sampled interval retained unchanged.')
