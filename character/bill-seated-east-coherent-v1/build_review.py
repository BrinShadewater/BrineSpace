from pathlib import Path
P=Path(__file__).resolve().parent
source=(P.parent/'bill-seated-south-coherent-v1/build_review.py').read_text()
source=source.replace('south','east').replace('native rear helmet','native selected east helmet')
source=source.replace('South sofa base: upright seated endpoint after the forward lowering poses.','East seated base: two independent middle lowering poses bridge the bend into seated rest.').replace('real sofa contact','real furniture contact')
exec(compile(source,str(P/'build_review.py'),'exec'))
