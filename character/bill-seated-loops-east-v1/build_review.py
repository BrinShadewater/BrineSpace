from pathlib import Path
P=Path(__file__).resolve().parent
source=(P.parent/'bill-seated-loops-south-v1/build_review.py').read_text()
source=source.replace('south','east').replace('native rear helmet','native selected east helmet')
source=source.replace('real observation sofa contact and tablet entry/exit review pending','real furniture contact, tablet entry/exit and runtime selection pending')
exec(compile(source,str(P/'build_review.py'),'exec'))
