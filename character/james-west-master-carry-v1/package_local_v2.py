from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'package_local.py').read_text(encoding='utf-8')
for name in ['local-inputs.json','local-raw.png','local-carry-pose.png','local-master-comparison.png','local-station-scale.png','local-crop-comparison.png','local-review.json']:
    source=source.replace("'"+name+"'","'"+name.replace('local-','local-v2-',1)+"'")
exec(compile(source,str(p/'package_local_v2.py'),'exec'))
