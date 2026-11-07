"""Package imagegen-authored neutral treads and four-direction torch phases."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
import build_companion_cleanup as cleanup
import build_sprite_polish as pack

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/josh-repair-v4'
cleanup.OUT=OUT;pack.OUT=OUT
original_rows=cleanup.rows
def revised_rows(path,nrows,cols,white=False):
    if path==ROOT/'character/josh-v1/sources/motion.png':path=OUT/'sources/motion.png';white=False
    elif path==ROOT/'character/companion-personality-v1/sources/josh.png':path=OUT/'sources/personality.png'
    return original_rows(path,nrows,cols,white)
cleanup.rows=revised_rows
cleanup.build('josh')
base,clips=pack.read_pack(OUT/'josh/manifest.json')
actions,poses=pack.read_pack(OUT/'josh-actions/manifest.json')
# Rear watch no longer needs the old duplicate used to hide a reversed head.
sheet=original_rows(OUT/'sources/personality.png',4,8)
scale=70/sheet[0][0].height
poses['watch-north']=[cleanup.frame(t,scale) for t in sheet[2][:4]]
sheet=original_rows(OUT/'sources/torch-fixed.png',4,8,gutter_fraction=.45,strict_padding=False)
for row,d in enumerate(['south','west','north','east']):
    # Register all torch poses against the authored neutral body height, not flame.
    scale=70/sheet[row][0].height
    frames=[]
    for tile in sheet[row]:
        a=np.asarray(tile)
        ys,xs=np.where(a[:max(1,round(sheet[row][0].height*.2)),:,3]>0)
        anchor=(int(xs.min())+int(xs.max())+1)*.5
        body=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX)
        body.putalpha(body.getchannel('A').point(lambda a:255 if a>=128 else 0))
        x=round(46-anchor*scale);y=86-body.height
        assert x>0 and x+body.width<92 and y>0,(d,x,body.size)
        im=Image.new('RGBA',(92,92));im.alpha_composite(body,(x,y));frames.append(im)
    for action,images,durations,loop in [
        ('torch-enter',[clips['idle-'+d][0].copy(),frames[0],frames[1]],[160]*3,False),
        ('torch',frames[2:6],[180]*4,True),
        ('torch-exit',[frames[6],frames[7],clips['idle-'+d][0].copy()],[160]*3,False)]:
        key=action+'-'+d;poses[key]=images
        actions['states'].append(dict(id=key,frameDurationsMs=durations,loop=loop))
combined={**clips,**poses};pack.quantize(combined)
for m in [base,actions]:
    m['sourceSheets']=['../sources/motion.png','../sources/personality.png','../sources/torch-fixed.png']
    m.pop('source',None)
pack.save_pack('josh',base,{k:combined[k] for k in clips})
pack.save_pack('josh-actions',actions,{k:combined[k] for k in poses})
html=['<!doctype html><meta charset="utf-8"><title>Josh tread and torch pass</title><style>body{background:#18242a;color:#ddd;font:16px system-ui;padding:24px}img{image-rendering:pixelated;max-width:100%}</style><h1>Josh — tread cleanup and blowtorch</h1><p>Neutral charcoal tracks and wheels; bluish lavender upper body. Deploy, weld, stow in four directions.</p>']
for state in ['idle','walk','watch','turn','torch']:
    contact=Image.new('RGBA',(92*10,92*4),(24,36,42,255))
    for row,d in enumerate(['south','west','north','east']):
        key=state+'-'+d
        images=combined[key];durations=(base if state in ['idle','walk'] else actions)['states']
        timing=next(s['frameDurationsMs'] for s in durations if s['id']==key)
        if state=='torch':images=combined['torch-enter-'+d]+images+combined['torch-exit-'+d];timing=[160]*3+[180]*4+[160]*3
        previews=[]
        for i,im in enumerate(images):
            contact.alpha_composite(im,(i*92,row*92));bg=Image.new('RGBA',(92,92),(24,36,42,255));bg.alpha_composite(im)
            previews.append(bg.resize((276,276),Image.Resampling.NEAREST).convert('RGB'))
        name=f'{state}-{d}.gif';previews[0].save(OUT/name,save_all=True,append_images=previews[1:],duration=timing,loop=0,disposal=2)
        html.append(f'<h3>{state} / {d}</h3><img src="{name}">')
    contact.save(OUT/f'{state}-contact.png')
if (OUT/'native-torch.gif').exists():html.append('<h2>Native Godot sprite board</h2><img src="native-torch.gif">')
(OUT/'review.html').write_text(''.join(html))
(OUT/'build-report.json').write_text(json.dumps({'packs':pack.REPORT,'sourceHashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (OUT/'sources').glob('*.png')},'newClips':12,'notes':'Torch supports paid crew hull repairs; base/personality palettes shared; no mirroring.'},indent=2))
print(json.dumps(pack.REPORT))
