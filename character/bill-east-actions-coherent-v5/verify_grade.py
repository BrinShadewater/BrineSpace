"""Verify the color-only revision against the preserved scaled candidate."""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent


def main():
    before = json.loads((HERE/'review-before-grade/manifest.json').read_text())
    after = json.loads((HERE/'manifest.json').read_text())
    checks = 0
    changed = 0
    for a,b in zip(before['states'],after['states'],strict=True):
        assert a['frameDurationsMs'] == b['frameDurationsMs']
        checks += 1
        for old,new in zip(a['frameFiles'],b['frameFiles'],strict=True):
            x = np.asarray(Image.open(HERE/'review-before-grade'/old))
            y = np.asarray(Image.open(HERE/new))
            assert x.shape == y.shape == (184,184,4)
            if b['id'] == 'interact-east' and new.endswith(('001.png','002.png','003.png','004.png')):
                assert np.array_equal(x[58:,:,3],y[58:,:,3]), new
                selected = np.asarray(Image.open(HERE/'review-idle-darkened.png').convert('RGBA'))
                entries = json.loads((HERE/'helmet-registration.json').read_text())
                index = int(Path(new).stem)
                dx,dy = next(e['offset'] for e in entries if e['frame']==index)
                band = Image.new('RGBA',(184,58))
                band.paste(Image.fromarray(selected).crop((0,0,184,58-dy)),(dx,dy))
                helmet_mask = Image.new('L',(184,58))
                polygon = [(72,0),(114,0),(114,51),(110,55),(101,58),(90,55),(82,51),(75,48),(72,43)]
                ImageDraw.Draw(helmet_mask).polygon([(px+dx,py+dy) for px,py in polygon],fill=255)
                blend = np.asarray(helmet_mask).copy()
                blend[:47] = 255
                authored = Image.open(HERE/'review-before-helmet-lock'/new).convert('RGBA')
                band = Image.composite(band,authored.crop((0,0,184,58)),Image.fromarray(blend))
                assert np.array_equal(y[:58],np.asarray(band)), 'pose-registered selected helmet'
                checks += 1
            else:
                assert np.array_equal(x[:,:,3],y[:,:,3]), new
            changed += int(not np.array_equal(x,y))
            checks += 2
    states = {s['id']:s for s in after['states']}
    def frame(key,i):
        return Image.open(HERE/states[key]['frameFiles'][i]).convert('RGBA')
    idle = Image.open(HERE/'review-idle-darkened.png').convert('RGBA')
    for key,i in [('interact-east',0),('interact-east',5),('kneel-east',0),('stand-east',5)]:
        assert frame(key,i).tobytes() == idle.tobytes()
        checks += 1
    for a,b in [('kneel-east','repair-east'),('repair-east','stand-east')]:
        assert frame(a,5).tobytes() == frame(b,0).tobytes()
        checks += 1
    registration = json.loads((HERE/'source-registration.json').read_text())
    assert registration['sourceSha256'] == hashlib.sha256((HERE/'sources/actions.png').read_bytes()).hexdigest()
    prior = json.loads((HERE/'review-before-grade/source-registration.json').read_text())
    assert registration == prior
    checks += 2
    report = {'checks':checks,'failures':0,'frames':24,'changedRgbFrames':changed,'sourcePreserved':True,'bodyAlphaAndRegistrationPreserved':True,'interactHeadBand':'translated selected helmet/neck; original moving shoulders; graphite 8 percent darker; staged idle endpoints match','visualAcceptance':'pending'}
    (HERE/'grade-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    # Representative poses at gameplay scales on dark and light backdrops.
    canvas = Image.new('RGB',(840,420))
    draw = ImageDraw.Draw(canvas)
    for row,background in enumerate([(30,43,53),(176,182,178)]):
        draw.rectangle((0,row*210,840,(row+1)*210),fill=background)
        for col,(root,rel,name) in enumerate([
            (HERE.parent,'bill-shared-helmet-east-matte-v1/frames/idle-east/000.png','Idle'),
            (HERE/'review-before-grade','frames/interact-east/002.png','Before'),
            (HERE,'frames/interact-east/002.png','Graded'),
            (HERE,'frames/repair-east/002.png','Repair'),
        ]):
            im = Image.open(root/rel).convert('RGBA')
            draw.text((col*210+8,row*210+8),name,fill=(230,230,230) if row==0 else (20,20,20))
            for j,height in enumerate([82,54,27]):
                factor = height/152
                size = round(184*factor)
                small = im.resize((size,size),Image.Resampling.BILINEAR)
                canvas.paste(small,(col*210+j*65+3,row*210+150-round(175*factor)),small)
    canvas.save(HERE/'gameplay-grade-review.png')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
