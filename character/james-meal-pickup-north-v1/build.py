"""Stage whole authored pickup poses at one master-derived scale; no runtime install."""
from pathlib import Path
import json, hashlib, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label

P = Path(__file__).resolve().parent
R = P.parents[1]
sys.path.insert(0, str(R / 'character/james-meal-family-v1'))
from build import feet, grade

raw = Image.open(P / 'source.png').convert('RGBA')
a = np.array(raw)
labs, _ = label(a[:, :, 3] > 180)
counts = np.bincount(labs.ravel()); counts[0] = 0
keys = sorted(np.argsort(counts)[-6:], key=lambda k: np.where(labs == k)[1].mean())
assert all(counts[k] > 10000 for k in keys)
centers = [np.where(labs == k)[1].mean() for k in keys]
edges = [0] + [round((centers[i] + centers[i+1]) / 2) for i in range(5)] + [raw.width]
cells = [raw.crop((edges[i], 0, edges[i+1], raw.height)) for i in range(6)]
runtime = R / 'character/crew-runtime-matte-v1/branforth'
manifest = json.loads((runtime / 'manifest.json').read_bytes())
state = next(s for s in manifest['states'] if s['id'] == 'idle-north')
master = Image.open(runtime / state['frameFiles'][0]).convert('RGBA')
meal = Image.open(R / 'character/james-meal-north-v1/frames/eat/000.png').convert('RGBA')
def extent(im):
    y, x = np.where(np.array(im)[:, :, 3] > 180)
    return dict(crown=int(y.min()), sole=int(y.max()), height=int(y.max()-y.min()+1))
scale = extent(master)['height'] / extent(cells[0])['height']
target = feet(master)
rows = []
records = []
for i, cell in enumerate(cells):
    anchor = feet(cell)
    at = (round(target[0]-anchor[0]*scale), round(target[1]-anchor[1]*scale))
    out = Image.new('RGBA', master.size)
    out.alpha_composite(cell.resize((round(cell.width*scale), round(cell.height*scale)), Image.Resampling.LANCZOS), at)
    out = grade(out, 'north')
    dest = P / 'frames' / f'{i:03d}.png'; dest.parent.mkdir(exist_ok=True)
    out.save(dest)
    rows.append(out)
    records.append(dict(sourcePose=i, sourceExtent=extent(cell), packagedExtent=extent(out), translation=at))
board = Image.new('RGB', (8*184, 240), '#303b40')
for i, im in enumerate([master]+rows+[meal]):
    board.paste(im, (i*184, 30), im)
    ImageDraw.Draw(board).text((i*184+8, 8), (['idle master']+[f'authored {j}' for j in range(6)]+['held meal'])[i], fill='white')
board.save(P / 'contact.png')
frames=[]
for im in [master]+rows+[meal]:
    view=Image.new('RGB',(820,330),'#303b40')
    ImageDraw.Draw(view).text((8,8),'Staged NORTH pickup / exact idle / held meal / 82px / 54px / 27px',fill='white')
    for sprite,x in [(im,30),(master,235),(meal,430)]:view.paste(sprite,(x,90),sprite)
    for h,x in [(82,630),(54,710),(27,780)]:
        s=h/148;small=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.BILINEAR)
        view.paste(small,(x,262-round(172*s)),small)
    frames.append(view)
frames[0].save(P/'review.gif',save_all=True,append_images=frames[1:],duration=[650,180,150,180,220,180,180,650],loop=0)
selection=dict(status='staged_source_contact_review_pending_not_installed',source='source.png',prompt='prompt.txt',generationTool='built-in imagegen',generatedOriginal='C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-ebefe2c1-5dad-448e-aa7c-2cdd2bce7c29.png',sourceSha256=hashlib.sha256((P/'source.png').read_bytes()).hexdigest(),fixedScale=scale,masterHeight=extent(master)['height'],poses=records,derivation='Whole authored figures, one fixed scale, foot translation, existing north matte/gold curve; exact accepted idle and held meal are comparison anchors only.',remaining=['Counter hand-height/contact review','Idle and held-meal endpoint continuity','Cup acquisition/dish deposit and interrupts','Native transition and Continue proofs','Owner visual review'])
selection['exactToolPrompt']='tool-prompt.txt'
selection['visualReview']='Agent reviewed contact board: fixed scale gives147–148px body; stable feet, belt wrench and matte material. Bowl rises near shoulder in authored reach; native hand/worktop contact and endpoint joins unproven. Staged, not installed.'
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
print(json.dumps(dict(scale=scale,extents=[r['packagedExtent'] for r in records],alphaZeroPixels=int((a[:,:,3]==0).sum()),status=selection['status'])))
