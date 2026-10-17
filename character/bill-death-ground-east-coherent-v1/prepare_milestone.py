from pathlib import Path
P=Path(__file__).resolve().parent;W=P.parent/'bill-death-ground-west-coherent-v1'
s=(W/'record_milestone.py').read_text(encoding='utf-8').replace('west','east').replace('West','East')
s=s.replace('exec-a45dae4c-2fe1-4d6e-bb05-083b69932de1','exec-e80aa2db-698c-41fd-81ec-09c4a7d2da89').replace('[.28,.3065]','[.31,.343]').replace('PASS10.96s','PASS13.46s').replace('76/93/125/166/181/187','76/94/133/169/183/184')
s=s.replace('Final6px settlement is authored lowering,','Final1px settlement is authored lowering,')
s=s.replace('and full-set identity polish remain. Exact loaded pixels,pacing,dry metadata,','and full-set identity polish remain. Hash-bound independent east/west comparison\nreviewed,5 shared plane/timing checks pass; physical anatomy/detail differences\nremain for full-set polish. Exact loaded pixels,pacing,dry metadata,')
(P/'record_milestone.py').write_text(s,encoding='utf-8')
