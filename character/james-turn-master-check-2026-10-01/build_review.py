"""Current ordered selection, fixed ruler and original source-clock review."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
# Reuse the maintained inventory logic while keeping earlier evidence untouched.
audit = (ROOT / 'character/james-animation-coverage-2026-09-30/audit.py').read_text()
exec(compile(audit, 'selection_inventory', 'exec'), {'__file__': str(HERE / 'audit.py')})
coverage = json.loads((HERE / 'runtime-coverage.json').read_text())
inputs = {}

def digest(path):
    inputs[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()

digest(ROOT / 'scripts/grid_canvas.gd')

def state(mode, key):
    path = ROOT / coverage['body' if mode == 'bare' else 'equipment'][key]['path']
    digest(path)
    manifest = json.loads(path.read_text())
    clip = next(s for s in manifest['states'] if s['id'] == key)
    images = []
    for rel in clip['frameFiles']:
        p = ROOT / rel[6:] if rel.startswith('res://') else path.parent / rel
        digest(p)
        im = Image.open(p).convert('RGBA')
        scale = 148 / manifest['standingHeight']
        if scale != 1:
            im = im.resize((round(im.width*scale), round(im.height*scale)), Image.Resampling.LANCZOS)
        canvas = Image.new('RGBA', (256, 256))
        canvas.alpha_composite(im, (round(128-manifest['pivot'][0]*scale), round(224-manifest['pivot'][1]*scale)))
        a = np.asarray(canvas)
        yy, xx = np.where(a[:, :, 3] > 180)
        images.append((canvas, {'crownY': int(yy.min()), 'footY': int(yy.max()), 'heightPx': int(yy.max()-yy.min()+1)}))
    return clip, images

def draw_pose(board, image, x, foot, size=148):
    scale = size/148
    im = image.resize((round(256*scale), round(256*scale)), Image.Resampling.LANCZOS)
    board.paste(im, (round(x-128*scale), round(foot-224*scale)), im)

report = {'scope': 'Current ordered runtime selection; every dry carry-turn source slot, common foot pivot and declared scale only. Source-clock playback; no new native/controller acceptance.', 'clips': {}}
keys = sorted(k for k in coverage['body'] if k.startswith('carry-turn-'))
cache = {}
for key in keys:
    start, end = key.split('-')[-2:]
    board = Image.new('RGB', (1040, 430), '#303b40')
    d = ImageDraw.Draw(board)
    d.text((12, 8), key+' / full source poses / fixed 148px ruler; no individual frame resizing', fill='white')
    for row, mode in enumerate(('bare', 'helmet')):
        clip, images = state(mode, key)
        masters = [state(mode, 'idle-'+direction)[1][0] for direction in (start, end)]
        cache[mode, key] = clip, images, masters
        heights = [m['heightPx'] for _, m in images]
        crown = [m['crownY'] for _, m in images]
        report['clips'][mode+'-'+key] = {'frames': len(images), 'durationMs': sum(clip['frameDurationsMs']), 'masters': dict(zip((start,end), [m for _,m in masters])), 'poses': [m for _,m in images], 'heightRange': [min(heights),max(heights)], 'crownRange': [min(crown),max(crown)]}
        foot = 205+row*205
        d.line((15,foot,1025,foot), fill='#72838c')
        chosen = [masters[0], images[0], images[len(images)//2], images[-1], masters[1]]
        for col, (im, metrics) in enumerate(chosen):
            x = 100+col*210
            draw_pose(board, im, x, foot)
            label = [start+' master','first','middle','last',end+' master'][col]
            d.text((x-65,foot-175), mode+' '+label, fill='white')
            d.text((x-65,foot+5), str(metrics['heightPx'])+'px', fill='#ced4d7')
    board.save(HERE/(key+'.png'))

# The owner's South-facing leg/height complaint: original 800ms turn plus
# stationary directional masters, shown at source and station review sizes.
key = 'carry-turn-east-south'
durations = cache['bare',key][0]['frameDurationsMs']
assert durations == cache['helmet',key][0]['frameDurationsMs']
frames = []
for index in range(len(durations)):
    board = Image.new('RGB', (960, 430), '#303b40')
    d = ImageDraw.Draw(board)
    d.text((12,8), 'James East to South / selected turn beside fixed masters / original 800ms source clock', fill='white')
    for row, size in enumerate((148,82)):
        foot = 220+row*180
        d.line((15,foot,945,foot), fill='#72838c')
        for mode, shift in (('bare',0),('helmet',100)):
            _, images, masters = cache[mode,key]
            for col, (im, metrics) in enumerate((masters[0],images[index],masters[1])):
                x = 95+col*330+shift
                draw_pose(board, im, x, foot, size)
                d.text((x-45,foot-size-22), ['East','turn '+str(index),'South'][col]+' '+mode, fill='white')
        d.text((12,foot+7), str(size)+'px review size', fill='#ced4d7')
    frames.append(board)
frames[0].save(HERE/'east-south-master-comparison.gif', save_all=True, append_images=frames[1:], duration=durations, loop=0)
frames[3].save(HERE/'east-south-midpoint.png')
report['inputs'] = inputs
report['slotsChecked'] = sum(v['frames'] for v in report['clips'].values())
report['productionInputsUnchanged'] = all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in inputs.items())
assert report['productionInputsUnchanged']
(HERE/'measurements.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'slots': report['slotsChecked'], 'clips': len(report['clips']), 'inputs': len(inputs), 'unchanged': True, 'bareRange': [min(v['heightRange'][0] for k,v in report['clips'].items() if k.startswith('bare')),max(v['heightRange'][1] for k,v in report['clips'].items() if k.startswith('bare'))], 'helmetRange': [min(v['heightRange'][0] for k,v in report['clips'].items() if k.startswith('helmet')),max(v['heightRange'][1] for k,v in report['clips'].items() if k.startswith('helmet'))]}))
