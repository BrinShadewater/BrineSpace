from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
base=(p/'package-upper-v15.gd').read_text()
for version,index in [(17,1),(18,2)]:
    source=base.replace('v15',f'v{version}').replace('V15',f'V{version}').replace('frames-v9/bare/002.png',f'frames-v9/bare/{index:03d}.png')
    path=p/f'package-upper-v{version}.gd';assert not path.exists();path.write_text(source)
    order=[p/'upper-crop-v15'/('previous.png' if version==17 else 'target.png'),p/'upper-crop-v15/target.png' if version==17 else p/'upper-crop-v17/raw.png',p/'upper-crop-v15/idle.png']
    records=[{'reference':str(f.relative_to(r)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'role':role} for f,role in zip(order,['edit target','incoming neighbor' if version==17 else 'early candidate neighbor','canonical West idle'])]
    # These exact local references were used; hashes recorded after calls. No pre-call freeze claimed.
    (p/f'upper-crop-v{version}/references.json').write_text(json.dumps({'references':records,'hashesRecorded':'after generation','crop':[96,56,80,80],'referenceMagnification':8,'method':'Built-in image_gen'},indent=2)+'\n')
print('Two independent native upper packages prepared, source origins preserved.')
