"""Preserve pre-repair files and expose cyan pixels captured by the old patch mask."""
from pathlib import Path
import json, shutil
import numpy as np
from PIL import Image, ImageDraw

H = Path(__file__).resolve().parent
R = H.parents[1]
backup = H / 'revisions/patch-ownership-v1'
backup.mkdir(parents=True, exist_ok=True)
for name in ['build.py', 'fit-checks.json', 'loops-master-v1.png', 'launch-master-v1.png']:
    if not (backup / name).exists():
        shutil.copy2(H / name, backup / name)
if not (backup / 'frames').exists():
    shutil.copytree(H / 'frames', backup / 'frames')
board = Image.new('RGB', (1200, 1080), '#202a30')
draw = ImageDraw.Draw(board)
records = []
for row, path in enumerate([H/'tread-source-v1.png', H/'swim-source-v1.png', R/'character/veld-water-material-v2/north-transition-source-v2.png']):
    im = Image.open(path).convert('RGBA')
    a = np.array(im); v = a[:,:,:3].astype(float)
    base = (a[:,:,3]>200)&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>35)
    old = base&(v[:,:,2]>v[:,:,1]*1.08)
    new = base&(v[:,:,2]>v[:,:,1]*1.3)
    excluded = old&~new
    overlay = a.copy(); overlay[excluded,:3] = [255,70,180]
    for col, image in enumerate([im, Image.fromarray(overlay)]):
        image.thumbnail((580,310))
        board.paste(image,(col*600,row*360+40),image)
    draw.text((8,row*360+8),path.name+' | original / formerly patch-graded cyan in pink',fill='white')
    records.append({'source':path.relative_to(R).as_posix(),'oldPatchPixels':int(old.sum()),'newPatchPixels':int(new.sum()),'excludedCyanPixels':int(excluded.sum())})
board.save(H/'patch-ownership-audit-v2.png')
(H/'patch-ownership-audit-v2.json').write_text(json.dumps({'records':records,'oldBlueGreenRatio':1.08,'newBlueGreenRatio':1.3,'scope':'candidate source patch ownership; excludes cyan before grading and resampling'},indent=2)+'\n')
print(json.dumps(records))
