"""Package four complete authored reach poses, retaining exact idle endpoints."""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import hashlib, json, copy, shutil

R = Path(__file__).resolve().parents[1]
P = R/'character/bill-east-reach-donor-motion-v1'
F = P/'frames/interact-east'
F.mkdir(parents=True, exist_ok=False)
idle = R/'character/bill-east-idle-master-motion-v1'
idle_source = idle/'frames/idle-east/000.png'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
report = dict(status='provisional_unselected', frames=[], inputs={str(idle_source):sha(idle_source)},
              normalAdmission=False, visualReviewed=False, nativeRun=False)
for slot in range(6):
    dst = F/f'{slot:03}.png'
    if slot in [0,5]:
        shutil.copyfile(idle_source,dst)
        method='exact whole idle0 endpoint alias'
    else:
        raw = P/f'sources/raw-{slot:03}.png'
        receipt = json.loads((P/f'provenance/{slot:03}.json').read_text())
        assert sha(raw)==receipt['rawSha256']
        image = Image.open(raw).convert('RGBA').resize((352,352),Image.Resampling.LANCZOS)
        alpha = np.asarray(image)[:,:,3]>127
        overflow=alpha.copy();overflow[52:236,68:252]=False
        assert not overflow.any(), f'opaque crop overflow at slot{slot}'
        image.crop((68,52,252,236)).save(dst)
        method='independent built-in whole-pose edit from detailed idle0; uniform352canvas and184crop'
        report['inputs'][str(raw)] = sha(raw)
        report['inputs'][str(P/f'provenance/{slot:03}.json')] = sha(P/f'provenance/{slot:03}.json')
    pixels=np.asarray(Image.open(dst).convert('RGBA'));y,x=np.where(pixels[:,:,3]>127)
    report['frames'].append(dict(slot=slot,bounds=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],
                                 soleEdge=int(y.max()+1),sha256=sha(dst),method=method))
assert all(row['soleEdge']==172 for row in report['frames']), 'floor registration differs'
old=json.loads((R/'character/bill-east-idle-interact-joined-v1/manifest.json').read_text())
state=copy.deepcopy(next(s for s in old['states'] if s['id']=='interact-east'))
state['frameFiles']=['res://'+(F/f'{i:03}.png').relative_to(R).as_posix() for i in range(6)]
state['provenance']='Four whole poses independently edited from detailed authored idle0; exact idle endpoints; family-review.json.'
manifest={k:v for k,v in old.items() if k!='states'}
manifest.update(name='Bill East detailed-donor reach family',states=[copy.deepcopy(old['states'][0]),state])
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
frames=[Image.open(F/f'{i:03}.png').convert('RGBA') for i in range(6)]
for name,mult in [('interaction-normal.png',1),('interaction-slow.png',4)]:
    frames[0].save(P/name,save_all=True,append_images=frames[1:],duration=[t*mult for t in state['frameDurationsMs']],loop=0,disposal=0,blend=0)
    with Image.open(P/name) as media:
        assert media.n_frames==6
        for n,im in enumerate(frames):media.seek(n);assert media.convert('RGBA').tobytes()==im.tobytes()
assert sum(state['frameDurationsMs'])==760
board=Image.new('RGB',(1680,850),'#17252d');draw=ImageDraw.Draw(board)
for row,(label,folder) in enumerate([('Registered prior family',R/'character/bill-east-idle-interact-joined-v1/frames/interact-east'),('Detailed idle donor family',F)]):
    draw.text((15,row*425+12),label,fill='white')
    for n in range(6):
        im=Image.open(folder/f'{n:03}.png').convert('RGBA').resize((368,368),Image.Resampling.NEAREST)
        crop=im.crop((80,0,348,368));board.paste(crop,(n*280+6,row*425+40),crop)
        draw.text((n*280+12,row*425+402),f'slot{n}',fill='white')
board.save(P/'family-review.png');(P/'family-review.json').write_text(json.dumps(report,indent=2)+'\n')
print('Six slots, four independent whole-pose edits, exact idle endpoints, all sole172; twelve APNG frames exact.')
