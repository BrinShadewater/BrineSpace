from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_thigh_run_v266.py').read_text(encoding='utf-8').replace('thigh-run-v266','thigh-run-v268').replace('[5,6,7,8,9,10]','[16,17,18,19,20,15]').replace('phase10','phase15').replace('phase==10','phase==15').replace('phase!=10','phase!=15')
s=s.replace('top row5,6,7; bottom row8,9,10','top row16,17,18; bottom row19,20,15').replace('Bottom-right10','Bottom-right15').replace('cells5..9','cells16..20').replace('adjacent pose10','adjacent pose15').replace('cell10','cell15')
s=s.replace('Retain ORIGINAL target cloth midtone brightness; no brightening to match reference-cell highlights.', 'Retain ORIGINAL target cloth midtone brightness; no brightening to match reference-cell highlights. The quilt should read as faint fine stitch lines in flat charcoal cloth, with no raised cushions, pale diamond centres or shiny rims. Do not lift the local target greys into lighter padded grey. Preserve the original unlit fabric values between stitches; add only fine subdued seams. This is a fabric construction correction, not a relighting or beauty enhancement.')
(p/'prepare_thigh_run_v268.py').write_text(s,encoding='utf-8')
s=(p/'package_thigh_run_v266.py').read_text(encoding='utf-8').replace('thigh-run-v266','thigh-run-v268');(p/'package_thigh_run_v268.py').write_text(s,encoding='utf-8')
s=(p/'prepare_thigh_window_v267.py').read_text(encoding='utf-8').replace('thigh-window-v267','thigh-window-v269').replace('[4,5,6,7,8,9,10,11]','[14,15,16,17,18,19,20,21]').replace('phase4..11','phase14..21')
start=s.index('    return p/(');end=s.index('\nbaseline=',start)
s=s[:start]+"    studies={14:'thigh-coordinated-v262/phase14',15:'thigh-boundaries-v264/phase15',16:'thigh-run-v268/phase16',17:'thigh-run-v268/phase17',18:'thigh-run-v268/phase18',19:'thigh-run-v268/phase19',20:'thigh-run-v268/phase20'}\n    return p/studies[i]/(mode+'-head-protected.png') if i in studies else r/ledger['states'][i]['candidateSources'][mode]['file']"+s[end:]
(p/'prepare_thigh_window_v269.py').write_text(s,encoding='utf-8')
