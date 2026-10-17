from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw

p = Path(__file__).resolve().parent
r = p.parents[1]
out = p / 'paired-v11'
out.mkdir(exist_ok=True)
index = json.loads((p / 'dense-cycle-v10-prompt-index.json').read_bytes())
bmf = r / 'character/crew-runtime-matte-v1/branforth/manifest.json'
hmf = r / 'character/james-shared-helmet-runtime-v1/manifest.json'
bm, hm = [json.loads(f.read_bytes()) for f in (bmf, hmf)]
bs, hs = [next(s for s in m['states'] if s['id'] == 'walk-west') for m in (bm, hm)]
assert bs['frameDurationsMs'] == hs['frameDurationsMs']
assert bm['pivot'] == hm['pivot'] == [92, 172]
assert len(bs['frameFiles']) == len(hs['frameFiles']) == len(index['poses']) == 49
files = [bmf, hmf, p / 'dense-cycle-v10-prompt-index.json', Path(__file__)]
checks, bare, gear = [], [], []
for i, row in enumerate(index['poses']):
    bf = p / row['source']
    assert hashlib.sha256(bf.read_bytes()).hexdigest() == row['sourceSha256']
    original_file, helmet_file = bmf.parent / bs['frameFiles'][i], hmf.parent / hs['frameFiles'][i]
    original, helmet = [np.array(Image.open(f).convert('RGBA')) for f in (original_file, helmet_file)]
    assert original.shape == helmet.shape == (184, 184, 4)
    delta = np.any(original != helmet, axis=2)
    yy, xx = np.where(delta)
    bounds = [int(xx.min()+36), int(yy.min()+52), int(xx.max()+37), int(yy.max()+53)]
    assert bounds == [111, 67, 146, 108], (i, bounds)
    body = np.array(Image.open(bf).convert('RGBA'))
    paired = body.copy()
    window = paired[52:236, 36:220]
    window[delta] = helmet[delta]
    mask = np.zeros((256, 256), bool)
    mask[52:236, 36:220] = delta
    assert np.array_equal(body[~mask], paired[~mask])
    im = Image.fromarray(paired)
    im.save(out / f'{i:03}.png')
    bare.append(Image.fromarray(body)); gear.append(im)
    files.extend((bf, original_file, helmet_file))
    checks.append({'phase': i, 'helmetDifferenceBounds': bounds,
                   'exactHelmetPixels': int(delta.sum()),
                   'unchangedCarryingPixels': int((~mask).sum()),
                   'bodyOutsideEquipmentDifferenceExact': True})

durations = [int(d) for d in bs['frameDurationsMs']]
common = {'frameWidth':256, 'frameHeight':256, 'pivot':[128,224],
          'standingHeight':148, 'precomposed':True, 'textureFilter':'linear',
          'status':'candidate_unselected_motion_review',
          'states':[{'id':'carry-west', 'frameCount':49, 'frameFiles':[],
                     'frameDurationsMs':durations, 'loop':True}]}
for name, paths in [('bare', [p / row['source'] for row in index['poses']]),
                    ('helmet', [out / f'{i:03}.png' for i in range(49)])]:
    m = json.loads(json.dumps(common))
    m['name'] = 'James West carrying full49 '+name+' provisional'
    m['states'][0]['frameFiles'] = ['res://'+f.relative_to(r).as_posix() for f in paths]
    (out / (name+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')

for start in range(0,49,7):
    board = Image.new('RGBA',(7*160,2*186),(48,59,63,255)); d=ImageDraw.Draw(board)
    for row, bank in enumerate((bare,gear)):
        for col,i in enumerate(range(start,min(start+7,49))):
            head=bank[i].crop((96,56,160,120)).resize((160,160),Image.Resampling.NEAREST)
            board.alpha_composite(head,(col*160,row*186+26))
            d.text((col*160+5,row*186+7),f'{i} '+('bare' if row==0 else 'helmet'),fill='white')
    board.convert('RGB').save(out / f'heads-{start}.png')

preview=[]
for i in range(49):
    board=Image.new('RGBA',(960,270),(48,59,63,255));d=ImageDraw.Draw(board)
    for row,bank in enumerate((bare,gear)):
        for j,height in enumerate((148,82,54,27)):
            scale=height/148;size=round(256*scale);x=row*480+(80,230,340,430)[j]
            board.alpha_composite(bank[i].resize((size,size),Image.Resampling.LANCZOS),
                                  (round(x-128*scale),round(252-224*scale)))
            d.text((x-35,8),('bare ' if row==0 else 'helmet ')+str(height),fill='white')
    preview.append(board.convert('RGB'))
preview[0].save(out/'paired-preview.apng',save_all=True,append_images=preview[1:],duration=durations,loop=0)
decoded=Image.open(out/'paired-preview.apng')
assert decoded.n_frames==49
for i in range(49):
    decoded.seek(i)
    assert decoded.convert('RGB').tobytes()==preview[i].tobytes()
    assert decoded.info['duration']==durations[i]
report={'inputSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
        'checks':checks,'durationMs':sum(durations),'decodedFramesExact':49,
        'perPoseFit':False,'sourceAcceptance':False,'selected':False,
        'continuousMotionWatched':False,'nativeRun':False,
        'scope':'Exact original helmet differences at original per-phase coordinates; carrying body retained elsewhere. Neck/contact/material motion review pending.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'paired':49,'durationMs':sum(durations),'outsideExact':49,'decodedExact':49}))
