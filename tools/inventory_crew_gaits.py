"""Report selected gait poses and aliases; pixel uniqueness is not gait acceptance."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
rows=[]
for actor,folder in {'veld':'dr-veld-v2','branforth':'chief-engineer-branforth-v2','marsh':'marsh-v2'}.items():
    art=ROOT/'character'/folder
    catalog=json.loads((art/'catalog.json').read_text())
    clips={}
    for rel in catalog['body']:
        path=art/rel
        manifest=json.loads(path.read_text())
        for state in manifest['states']:
            if not state['id'].startswith(('walk-','run-')): continue
            hashes=[hashlib.sha256(Image.open(path.parent/file).convert('RGBA').tobytes()).hexdigest() for file in state['frameFiles']]
            clips[state['id']]={'hashes':hashes,'durations':state['frameDurationsMs'],'strides':manifest.get('strideDistanceCells',{})}
    for key,clip in clips.items():
        rows.append({'actor':actor,'state':key,'frameCount':len(clip['hashes']),
                     'uniquePixels':len(set(clip['hashes'])),'timingsMs':clip['durations'],
                     'strides':clip['strides'],
                     'identicalWalk':key.startswith('run-') and clip['hashes']==clips.get(key.replace('run-','walk-'),{}).get('hashes')})
out=ROOT/'output/crew-replacement-2026-09-12/gait-inventory.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'states':len(rows),'runWalkAliases':[row['actor']+'/'+row['state'] for row in rows if row['identicalWalk']]}))
