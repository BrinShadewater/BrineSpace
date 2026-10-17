"""Review sources at manifest physical density; no mutation or pose fitting."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parent
P.mkdir(exist_ok=True)
swim=R/'bill-swim-west-coherent-v1'
entry=R/'bill-land-water-west-v10'
inputs=[swim/'manifest.json',swim/'registration.json',swim/'build.py',swim/'sources/swim-layout-v2.png',R/'crew-side-masters-v1/bill-side-master-01.png',entry/'bare/manifest.json',entry/'helmet/manifest.json',entry/'review.json']
inputs += [swim/f'frames/swim-west/{i:03}.png' for i in range(6)]
inputs += [entry/g/f'frames/land-swim-west/{i:03}.png' for g in ['bare','helmet'] for i in range(7)]
revision=R/'bill-land-water-west-v11'
inputs += [revision/'bare/frames/land-swim-west/005.png',revision/'bare/manifest.json',revision/'sources/prone-legs-v4.png']
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
before={f.relative_to(R).as_posix():sha(f) for f in inputs}
m=json.loads((swim/'manifest.json').read_text());reg=json.loads((swim/'registration.json').read_text())
assert m['standingHeight']==148 and m['pivot']==[86,88]
assert reg['scale']==.27 and all(f['scale']==.27 for f in reg['frames'])
assert sha(swim/reg['source'])==reg['sourceSha256']
frames=[]
for i in range(6):
    raw=Image.open(swim/f'frames/swim-west/{i:03}.png').convert('RGBA')
    im=Image.new('RGBA',(320,320));im.alpha_composite(raw,(74,136))
    frames.append(im)
assert frames[0].tobytes()==Image.open(entry/'bare/frames/land-swim-west/006.png').convert('RGBA').tobytes()
# Exact original standing master at148/956 source density, same feet ruler.
original=Image.open(R/'crew-side-masters-v1/bill-side-master-01.png').convert('RGBA').crop((850,0,1280,1024))
density=148/956
small=original.resize((round(original.width*density),round(original.height*density)),Image.Resampling.LANCZOS)
master=Image.new('RGBA',(320,320));master.alpha_composite(small,(125,round(224-977*density)))
def board(name,tiles):
    canvas=Image.new('RGB',(1280,720),'#182932');d=ImageDraw.Draw(canvas)
    for k,(label,im) in enumerate(tiles):
        x=(k%4)*320;y=(k//4)*360
        canvas.paste(im,(x,y+25),im);d.text((x+4,y+4),label,fill='white')
        d.line((x,y+249,x+319,y+249),fill='#5d9899')
    canvas.save(P/name)
    return canvas
tiles=[('Original standing /H148',master),('Current standing context',Image.open(entry/'bare/frames/land-swim-west/000.png').convert('RGBA')),('Repaired levelling4',Image.open(entry/'bare/frames/land-swim-west/004.png').convert('RGBA')),('New near-prone5',Image.open(entry/'bare/frames/land-swim-west/005.png').convert('RGBA'))]+[(f'Selected swim{i}',frames[i]) for i in range(4)]
board('master-entry-swim-review.png',tiles)
board('six-stroke-review.png', [('Original standing /H148',master),('New near-prone5',tiles[3][1])]+[(f'Selected swim{i}',frames[i]) for i in range(6)])
board('leg-revision-review.png',[('Original standing /H148',master),('V10 near-prone',tiles[3][1]),('V11 leg revision',Image.open(revision/'bare/frames/land-swim-west/005.png').convert('RGBA')),('Selected swim0',frames[0])]+[(f'Selected swim{i}',frames[i]) for i in range(2,6)])
close=Image.new('RGB',(1920,720),'#182932');d=ImageDraw.Draw(close)
for i,(label,im) in enumerate([tiles[0],tiles[2],tiles[3],('Selected swim0',frames[0])]):
    # Identical2x display multiplier, fixed whole canvas (no occupied-bounds fit).
    crop=im.resize((640,640),Image.Resampling.NEAREST)
    close.paste(crop,(i*480-75,30),crop);d.text((i*480+5,5),label+' /same2x',fill='white')
close.save(P/'detail-review.png')
after={f.relative_to(R).as_posix():sha(f) for f in inputs};assert before==after
report=dict(scope='Source proportion audit; no native motion or normal source mutation.',inputsStable=len(before),inputSHA256=before,swimDensity=.27,entryMasterDensity=density,physicalStandingHeight=148,allSixSwimFramesFixedScale=True,entryFinalContextExactSelectedSwim0=True,sourceIntegrityExact=True,visualAcceptance='Pending board inspection',normalSelectedChanged=False)
(P/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(P/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Bill west water proportions</title><style>body{background:#182932;color:#eee;font:18px sans-serif;margin:24px}img{display:block;width:100%;max-width:1280px;margin:24px 0}</style><h1>Bill — west water proportion audit</h1><p>Original master, current entry and selected swimming at common physical height148. No per-pose width or height fitting. Source review only; full anatomy, grade and moving joins remain pending.</p><img src="master-entry-swim-review.png"><img src="six-stroke-review.png"><img src="detail-review.png"><h2>Near-prone leg revision</h2><img src="leg-revision-review.png">''',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='inputSHA256'}))
