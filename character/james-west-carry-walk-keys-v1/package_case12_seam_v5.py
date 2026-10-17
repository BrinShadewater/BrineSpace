from pathlib import Path
import json,hashlib,shutil,sys
p=Path(__file__).resolve().parent;r=p.parents[1];old='walk12-case-master-v5';name=old+'-seam'
inputs=json.loads((p/f'{old}-inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
inputs['admissionRegion']=[88,116,158,161]
inputs['postCallPackagingSha256']={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in [p/f'{old}-raw.png',p/f'{old}-inputs.json',Path(__file__)]}
inputs['scope']='Post-call packaging correction, same complete authored raw crop. Consume7additional right-edge columns rather than leaving original silhouette pixels detached. Original generation inventory unchanged; no new drawing/fit/grade or clipped-alpha cleanup.'
(p/f'{name}-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(p/f'{old}-raw.png',p/f'{name}-raw.png')
sys.argv=[str(p/'package_key.py'),name]
exec(compile((p/'package_key.py').read_text(),str(p/'package_key.py'),'exec'))
