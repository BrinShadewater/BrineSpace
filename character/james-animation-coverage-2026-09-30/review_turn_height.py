"""Measure every selected dry cargo turn against actual directional masters."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
R = P.parents[1]
coverage = json.loads((P / 'runtime-coverage.json').read_text())
out = P / 'turn-height-review'
out.mkdir(exist_ok=True)

def clip(mode, key):
    path = R / coverage['body' if mode == 'bare' else 'equipment'][key]['path']
    manifest = json.loads(path.read_text())
    state = next(s for s in manifest['states'] if s['id'] == key)
    return path, manifest, state

def load(path, m, s, i):
    im = Image.open(path.parent / s['frameFiles'][i]).convert('RGBA')
    scale = 148 / m['standingHeight']
    if scale != 1:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', (256, 256))
    canvas.alpha_composite(im, (round(128 - m['pivot'][0] * scale), round(224 - m['pivot'][1] * scale)))
    a = np.array(canvas)
    y, x = np.where(a[:, :, 3] > 180)
    return canvas, dict(crownY=int(y.min()), lowestOpaqueY=int(y.max()), heightPx=int(y.max()-y.min()+1))

report = dict(scope='All selected dry carry-turn PNG slots, normalized by declared standingHeight only; alpha>180 bounds and full-pose visual boards. No per-pose fitting; not runtime motion evidence.', clips={})
for key in (k for k in coverage['body'] if k.startswith('carry-turn-')):
    start, end = key.split('-')[-2:]
    n = coverage['body'][key]['frames']
    board = Image.new('RGB', ((n+2)*170, 620), '#303b40')
    draw = ImageDraw.Draw(board)
    draw.text((10, 5), key + ' / all frames; common foot pivot, fixed declared physical scale', fill='white')
    for row, mode in enumerate(['bare', 'helmet']):
        path, m, s = clip(mode, key)
        frames = [load(path, m, s, i) for i in range(len(s['frameFiles']))]
        masters = []
        for direction in [start, end]:
            mp, mm, ms = clip(mode, 'idle-'+direction)
            masters.append(load(mp, mm, ms, 0))
        report['clips'][mode+'-'+key] = dict(manifest=path.relative_to(R).as_posix(), masters={start:masters[0][1], end:masters[1][1]}, frames=[dict(index=i, **v[1]) for i,v in enumerate(frames)], heightRange=[min(v[1]['heightPx'] for v in frames), max(v[1]['heightPx'] for v in frames)])
        for col, (im, metrics) in enumerate([masters[0]]+frames+[masters[1]]):
            x, y = col*170, 42+row*285
            crop = im.crop((70, 50, 187, 233)).resize((164,256), Image.Resampling.BILINEAR)
            board.paste(crop, (x, y+24), crop)
            label = start+' master' if col == 0 else end+' master' if col == len(frames)+1 else 'pose '+str(col-1)
            draw.text((x+4,y),mode+' '+label+' '+str(metrics['heightPx'])+'px', fill='white')
            draw.line((x,y+24+(223-50)*256/183,x+163,y+24+(223-50)*256/183), fill='#8199a5')
    board.save(out/(key+'.png'))
(out/'measurements.json').write_text(json.dumps(report,indent=2)+'\n')
for k,v in report['clips'].items():
    print(k, v['heightRange'], 'masters', {d:q['heightPx'] for d,q in v['masters'].items()})
