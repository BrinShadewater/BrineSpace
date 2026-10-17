from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
manifest=R/'character/james-cargo-material-joined-v1/bare-manifest.json';pack=json.loads(manifest.read_bytes())
rows=[];groups={}
for state in pack['states']:
    if not (state['id'] in ['pickup-east','carry-east','unload-east'] or state['id'].startswith('carry-turn-') and 'east' in state['id']):continue
    for i,rel in enumerate(state['frameFiles']):
        file=(manifest.parent/rel).resolve();im=Image.open(file).convert('RGBA');bbox=im.getbbox();content=im.crop(bbox)
        h=hashlib.sha256(content.tobytes()).hexdigest();row={'key':state['id'],'index':i,'source':file.relative_to(R).as_posix(),'visibleBounds':bbox,'contentHash':h};rows.append(row);groups.setdefault(h,[]).append(row)
(P/'cargo-alias-evidence.json').write_text(json.dumps({'rows':rows,'exactCroppedRGBAGroups':[g for g in groups.values() if len(g)>1],'scope':'Current selected cargo material pack East pickup/gait/unload and retained East-involving turn states only. Full visible cropped RGBA hash, not semantically similar poses.'},indent=2))
for key in ['pickup-east','carry-east','unload-east']:
    print(key,[(r['index'],[(x['key'],x['index']) for x in groups[r['contentHash']] if x!=r]) for r in rows if r['key']==key])
print('Rows',len(rows),'shared exact groups',sum(len(g)>1 for g in groups.values()))
