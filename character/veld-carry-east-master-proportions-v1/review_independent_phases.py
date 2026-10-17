"""Independent authoring comparisons only; never exports a normalized gait."""
from pathlib import Path
import json, hashlib
import numpy as np
from scipy.ndimage import label, find_objects, binary_dilation
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
R = P.parents[1]
items = [
    ('Canonical held', R/'character/veld-cargo-turns-master-family-v1/corrected-east-held-density-reference.png'),
    ('Opposite contact V5', P/'raw-opposite-contact-v5.png'),
    ('Passing V8', P/'raw-passing-v8.png'),
    ('Forward swing V9', P/'raw-swing-v9.png'),
    ('Original East master', R/'character/veld-side-foundation-v1/east-standing.png'),
]
board = Image.new('RGB', (1280, 590), '#202a30')
d = ImageDraw.Draw(board)
d.text((8, 6), 'INDEPENDENT SOURCE STUDIES: 148px comparison height only, NOT gait registration. Original RGBA/grade.', fill='white')
rows = []
for i, (name, path) in enumerate(items):
    im = Image.open(path).convert('RGBA'); a = np.array(im)
    labels, _ = label(a[:,:,3] > 200)
    sizes = np.bincount(labels.ravel()); sizes[0] = 0
    n = int(sizes.argmax()); slices = find_objects(labels)[n-1]
    y, x = slices; box = [x.start, y.start, x.stop, y.stop]
    keep = binary_dilation(labels == n, iterations=2)
    a[~keep] = 0
    crop = Image.fromarray(a).crop((max(0,x.start-2), max(0,y.start-2), min(im.width,x.stop+2), min(im.height,y.stop+2)))
    scale = 148/(y.stop-y.start)
    small = crop.resize((round(crop.width*scale), round(crop.height*scale)), Image.Resampling.LANCZOS)
    frame = Image.new('RGBA',(256,256))
    offset = ((256-small.width)//2, 224-small.height+1)
    frame.alpha_composite(small, offset)
    pix = np.array(frame); sy, sx = np.where(pix[:,:,3]>128)
    _, hx = np.where(pix[sy.min():sy.min()+20,:,3]>128)
    head = int(hx.max()-hx.min()+1)
    d.text((i*256+5,29),name, fill='white')
    d.text((i*256+5,46),f'head top20 width {head}px',fill='#d2dce0')
    board.paste(frame,(i*256,40),frame)
    detail=frame.crop((45,70,215,165)).resize((255,143),Image.Resampling.NEAREST)
    board.paste(detail,(i*256,320),detail)
    lower=frame.crop((55,157,225,232)).resize((255,112),Image.Resampling.NEAREST)
    board.paste(lower,(i*256,470),lower)
    rows.append({'label':name,'source':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sourceBox':box,'mainOpaquePixels':int(sizes[n]),'backgroundAlphaTopLeft':int(np.array(im)[0,0,3]),'comparisonScale':scale,'headTop20Width':head})
    if i in (2,3): frame.save(P/('passing-v8-study.png' if i==2 else 'swing-v9-study.png'))
board.save(P/'independent-phases-v9-comparison.png')
result={'scope':'Source study only; independent148px bounding comparisons cannot be used as animation registration. No grade changes, production or native admission.','alphaExtraction':'Largest opaque alpha component with bounded2px dilation; original RGBA inside.','rows':rows}
(P/'independent-phases-v9-review.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'sources':len(rows),'headWidths':[r['headTop20Width'] for r in rows],'opaquePixels':[r['mainOpaquePixels'] for r in rows]}))
