from pathlib import Path
import json
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1]
pack=json.loads((P/'manifest.json').read_bytes())
clips={}
for folder,file in [('james-meal-family-v1','bare-manifest.json'),('james-meal-pickup-north-v1','manifest.json'),('james-cup-pickup-north-v1','handoffs-manifest.json')]:
    for row in json.loads((P.parent/folder/file).read_bytes())['states']:
        if row['id'].endswith('-north'):clips[row['id'].removesuffix('-north')]=(P.parent/folder,row)
def image(path,folder):
    return Image.open(R/path.removeprefix('res://') if path.startswith('res://') else folder/path).convert('RGBA')
idle=image('selected/000.png',P.parent/'james-meal-pickup-north-v1')
checks=0
for row in pack['states']:
    folder,source=clips[row['provenance']['sourceAction']];index=row['provenance']['sourceIndex']
    assert image(row['frameFiles'][0],P).tobytes()==image(source['frameFiles'][index],folder).tobytes();checks+=1
    assert image(row['frameFiles'][-1],P).tobytes()==idle.tobytes();checks+=1
    assert all(path.startswith('res://') and '/../' not in path for path in row['frameFiles']);checks+=1
    if row['provenance']['sourceAction'] in ['eat','drink'] and index in [0,5]:assert row['frameCount']==6
(P/'package-evidence.json').write_text(json.dumps(dict(checks=checks,failures=0,states=len(pack['states']),maxSeconds=max(sum(s['frameDurationsMs'])/1000 for s in pack['states']),scope='All36 whole-source returns begin at exact source-index pixels, end at exact padded idle, retain canonical whole resource paths. Neutral loop poses skip reverse mouthful replay; native routes/Continue separate.'),indent=2)+'\n')
print(f'{checks} exact source-index/idle/path checks pass across36 returns')
