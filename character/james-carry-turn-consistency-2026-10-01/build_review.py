"""Fixed-registration selected cargo turn review; no asset changes."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
R = P.parents[1]
coverage = json.loads((R / 'character/james-animation-coverage-2026-09-30/runtime-coverage.json').read_text())
cache = {}
records = []

def load(mode, key):
    file = R / coverage['body' if mode == 'bare' else 'equipment'][key]['path']
    if file not in cache:
        cache[file] = json.loads(file.read_text())
    m = cache[file]
    s = next(s for s in m['states'] if s['id'] == key)
    paths = [R / f.removeprefix('res://') if f.startswith('res://') else (file.parent / f).resolve() for f in s['frameFiles']]
    return m, s, paths

def plane(path, manifest):
    # Existing scale contract; no frame-wise bounding-box resizing.
    assert manifest['standingHeight'] == 148
    im = Image.open(path).convert('RGBA')
    out = Image.new('RGBA', (256, 256))
    out.alpha_composite(im, (128-int(manifest['pivot'][0]),224-int(manifest['pivot'][1])))
    return out

keys = [k for k in coverage['body'] if k.startswith('carry-turn-')]
for key in keys:
    start, end = key.removeprefix('carry-turn-').split('-')
    count = load('bare', key)[1]['frameCount']
    board = Image.new('RGB', ((count+2)*256, 560), '#303b40')
    draw = ImageDraw.Draw(board)
    for row, mode in enumerate(['bare','helmet']):
        m,s,paths = load(mode,key)
        start_m,_,start_paths = load(mode,'idle-'+start)
        end_m,_,end_paths = load(mode,'idle-'+end)
        items = [('master '+start,plane(start_paths[0],start_m))]
        for i,path in enumerate(paths):
            im = plane(path,m)
            a = np.array(im)
            yy,xx = np.where(a[:,:,3]>192)
            records.append({'mode':mode,'key':key,'index':i,'path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'boundsAlpha192':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],'heightAlpha192':int(yy.max()-yy.min()+1),'pivot':m['pivot'],'standingHeight':m['standingHeight'],'durationMs':s['frameDurationsMs'][i]})
            items.append((key+' '+str(i),im))
        items.append(('master '+end,plane(end_paths[0],end_m)))
        for col,(label,im) in enumerate(items):
            x,y=col*256,row*280
            board.paste(im,(x,y+24),im)
            draw.text((x+4,y+4),mode+' '+label,fill='white')
            # Standing master crown/sole reference; body includes held cargo.
            draw.line((x,y+101,x+255,y+101),fill='#63747b')
            draw.line((x,y+247,x+255,y+247),fill='#63747b')
    board.save(P/(key+'.png'))
summary=[]
for key in keys:
    for mode in ['bare','helmet']:
        rows=[r for r in records if r['key']==key and r['mode']==mode]
        summary.append({'key':key,'mode':mode,'references':len(rows),'crownRange':[min(r['boundsAlpha192'][1] for r in rows),max(r['boundsAlpha192'][1] for r in rows)],'soleRange':[min(r['boundsAlpha192'][3] for r in rows),max(r['boundsAlpha192'][3] for r in rows)],'heightRange':[min(r['heightAlpha192'] for r in rows),max(r['heightAlpha192'] for r in rows)]})
(P/'review-evidence.json').write_text(json.dumps({'sourceReferences':len(records),'summary':summary,'records':records,'scope':'Fixed pivot and standingHeight; alpha bounds include cargo and are flags, not anatomical proof. Review both masters and all whole-source poses. No scaling, translation fitting, grading or runtime changes.'},indent=2)+'\n')
print(json.dumps({'sourceReferences':len(records),'states':len(keys),'summary':summary}))
