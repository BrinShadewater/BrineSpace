"""Layer contract and illustrative departure review; not a gameplay fixture."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
reg = json.loads((P / 'registration.json').read_text())
checks = []
def check(name, value):
    checks.append({'name': name, 'pass': bool(value)})

bare = Image.open(P / 'body-bare.png').convert('RGBA')
helmet = Image.open(P / 'body-helmet.png').convert('RGBA')
case = Image.open(P / 'case.png').convert('RGBA')
b, h = np.array(bare), np.array(helmet)
y, x = np.indices(b.shape[:2])
head = reg['headTarget']
allowed = ((x-head[0])/14)**2 + ((y-(head[1]-1))/14)**2 <= 1
px, py = reg['helmetPosition']
pw, ph = reg['helmetPatchSize']
allowed[py:py+ph, px:px+pw] = True
check('paired bodies exact outside declared head/shell area', np.array_equal(b[~allowed], h[~allowed]))
check('paired full body canvas', bare.size == helmet.size == (256, 276))
check('one source physical ruler', all(t['fixedScale'] == reg['fixedScale'] for t in reg['tracking']))
check('finite grade', all(np.isfinite(reg[k]).all() for k in ['neutralGain', 'goldGain', 'faceGain', 'hairGain', 'caseGain']))
check('raw source fingerprint', hashlib.sha256((P/'source.png').read_bytes()).hexdigest() == reg['sourceSha256'])
cx,cy = reg['casePosition']; cw,ch=case.size
check('detached case original crop size', case.size == tuple(np.array(reg['caseProvenance']['crop'][2:])-reg['caseProvenance']['crop'][:2]))
check('case remains at original native scale', reg['caseProvenance']['nativeScale']==1.0)
case_donor=Image.open(P.parent/'james-water-cargo-east-v1/frames/bare/swim-pickup/001.png').convert('RGBA')
cv=np.array(case); donor=np.array(case_donor)[cy:cy+ch,cx:cx+cw];visible=cv[:,:,3]>0
check('every retained case pixel exactly selected', np.array_equal(cv[visible],donor[visible]))
case_core=cv[:,:,3]>180
corey,corex=np.where(case_core)
check('original opaque case physical size', [int(corex.max()-corex.min()+1),int(corey.max()-corey.min()+1)]==[40,33])
check('complete original opaque case coverage', int(case_core.sum())==1226)
check('release body has no opaque intersection with case', not np.any(case_core & (b[cy:cy+ch,cx:cx+cw,3]>180)))
for gear in ['bare','helmet']:
    entrance=Image.open(P/f'frames/{gear}/000.png').convert('RGBA')
    donor=np.array(Image.open(P.parent/f'james-water-cargo-east-v1/frames/{gear}/swim-pickup/001.png').convert('RGBA'))
    reconstructed=entrance.copy();reconstructed.alpha_composite(case,(cx,cy));rv=np.array(reconstructed)
    check(gear+' selected entrance alpha reconstruction',np.array_equal(rv[:,:,3],donor[:,:,3]))
    check(gear+' selected entrance visible RGB reconstruction',np.array_equal(rv[:,:,:3][donor[:,:,3]>0],donor[:,:,:3][donor[:,:,3]>0]))
check('registered selected head anchor', np.allclose(head, [141.5378198256979,118.2267791396747]))

selected = {gear: Image.open(P.parent / f'james-water-cargo-east-v1/frames/{gear}/swim-pickup/001.png').convert('RGBA') for gear in ['bare','helmet']}
metrics = {'scope': 'Authored layer candidate and offline straight departure illustration only; no runtime/world/save evidence.', 'bodyBounds': bare.getbbox(), 'helmetBounds': helmet.getbbox(), 'caseBounds': case.getbbox(), 'caseAnchor': reg['casePosition'], 'selectedBounds': {g: im.getbbox() for g, im in selected.items()}, 'checks': checks}

frames = []
native_scale = 82/148
for step in range(25):
    # Uniform ruler at both display sizes. Translate the complete body only.
    displacement = round(40 * min(step, 20)/20)
    board = Image.new('RGB', (920, 360), '#303b40')
    draw = ImageDraw.Draw(board)
    draw.text((12, 8), 'East release candidate — offline layer preview', fill='white')
    draw.text((12, 27), 'Selected pickup | release at shared 148px ruler | departure at native 82px ruler', fill='white')
    for row, (gear, body) in enumerate([('bare',bare), ('helmet',helmet)]):
        top = 58 + row*146
        draw.text((12,top),gear,fill='white')
        crop = selected[gear].crop((35,85,235,180))
        board.paste(crop,(12,top+25),crop)
        release = body.copy()
        release.alpha_composite(case,tuple(reg['casePosition']))
        crop = release.crop((35,85,235,180))
        board.paste(crop,(285,top+25),crop)
        departure = Image.new('RGBA',(256,276))
        departure.alpha_composite(body,(-displacement,0))
        departure.alpha_composite(case,tuple(reg['casePosition']))
        # Transparent case pixels may legitimately reveal the body beneath them.
        # Certify the fixed independent layer and its visible opaque composite.
        case_layer = Image.new('RGBA',(256,276))
        case_layer.paste(case,tuple(reg['casePosition']))
        cp = np.array(case_layer)[cy:cy+ch,cx:cx+cw]
        check(f'{gear} departure {step} fixed case layer pixels', np.array_equal(cp,np.array(case)))
        cp = np.array(departure)[cy:cy+ch,cx:cx+cw]
        opaque = np.array(case)[:,:,3] == 255
        check(f'{gear} departure {step} opaque case composite', np.array_equal(cp[opaque],np.array(case)[opaque]))
        crop = departure.crop((0,80,240,185))
        crop = crop.resize((round(crop.width*native_scale),round(crop.height*native_scale)),Image.Resampling.LANCZOS)
        board.paste(crop,(620,top+35),crop)
    draw.text((620,330),f'Body offset: {displacement*native_scale:.1f}px; case offset: 0px',fill='white')
    frames.append(board)
frames[0].save(P/'departure-review.gif',save_all=True,append_images=frames[1:],duration=[80]*24+[600],loop=0)
frames[-1].save(P/'departure-contact.png')
metrics['checks']=checks
metrics['passed']=sum(c['pass'] for c in checks)
metrics['failed']=sum(not c['pass'] for c in checks)
(P/'layer-evidence.json').write_text(json.dumps(metrics,indent=2)+'\n')
print(json.dumps({k:metrics[k] for k in ['passed','failed','bodyBounds','helmetBounds','caseBounds','selectedBounds']}))
assert metrics['failed']==0
