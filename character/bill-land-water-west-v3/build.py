from pathlib import Path
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation
import numpy as np
import json, hashlib

P = Path(__file__).resolve().parent
OLD = P.parent/'bill-land-water-west-v1'
S = P/'sources'
S.mkdir(parents=True,exist_ok=True)
registrations = {}
for kind, version, generation in [('crouch',4,'exec-2c5760c3-9a86-44e2-83f3-ca31153cd4ed'),('push',3,'exec-23fd84d8-f757-4075-8d82-f3f87cd535f2')]:
    rawpath = OLD/f'sources/{kind}-canvas-v{version}.png'
    raw = Image.open(rawpath).convert('RGBA')
    assert raw.width == raw.height
    a = np.array(raw)
    lab,_ = label(a[:,:,3]>250)
    counts = np.bincount(lab.ravel())
    mask = binary_dilation(lab==np.argmax(counts[1:])+1,iterations=3)&(a[:,:,3]>0)
    a[~mask]=0
    im = Image.fromarray(a).resize((320,320),Image.Resampling.LANCZOS)
    b = np.array(im)
    yy,xx = np.indices(b.shape[:2])
    sole=None
    dy=0
    if kind=='crouch':
        boot=(b[:,:,3]>180)&(xx>=130)&(xx<205)&(yy>=190)&(yy<260)
        assert boot.any()
        sole=int(yy[boot].max())+1
        dy=224-sole
    out=Image.new('RGBA',(320,320))
    out.paste(im,(0,dy))
    assert np.count_nonzero(np.array(out)[:,:,3]) == np.count_nonzero(b[:,:,3])
    out.save(S/f'{kind}-native-v{version}.png')
    registrations[kind]={'source':str(rawpath.relative_to(P.parent)),'generation':generation,'prompt':f'bill-land-water-west-v1/sources/{kind}-prompt-v{version}.txt','rawCanvas':raw.size,'wholeCanvasScale':320/raw.width,'translation':[0,dy],'soleBefore':sole,'paintedSupportPreserved':True,'nativeAlphaBBox':out.getchannel('A').getbbox()}

inputs=[OLD/'sources/reference-idle-native.png',OLD/'sources/arm-ready-native-v3.png',S/'crouch-native-v4.png',S/'push-native-v3.png',OLD/'sources/lift-native-v2.png',OLD/'sources/prone-native-v1.png',OLD/'sources/reference-swim-native.png']
poses=[Image.open(f).convert('RGBA') for f in inputs]
times=[60,70,80,60,80,90,60]
F=P/'bare/frames/land-swim-west'
F.mkdir(parents=True,exist_ok=True)
for i,im in enumerate(poses): im.save(F/f'{i:03}.png')
preserved=[]
for i in [0,1,4,5,6]:
    assert poses[i].tobytes()==Image.open(P.parent/'bill-land-water-west-v2'/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA').tobytes()
    preserved.append(i)
manifest={'name':'Bill West compact water entry revision','frameWidth':320,'frameHeight':320,'pivot':[160,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'source_trial_unselected','states':[{'id':'land-swim-west','frameFiles':[f'frames/land-swim-west/{i:03}.png' for i in range(7)],'frameDurationsMs':times,'loop':False,'facings':['west']*7,'provenance':'Five V2 poses exact; new original-master graphite quilting/badge detail crouch and push edits. Fixed whole canvas ruler. Helmet/live endpoint/native/material/Continue pending.'}]}
(P/'bare/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
poses[0].save(P/'bare/source-enter.png',save_all=True,append_images=poses[1:],duration=times,loop=0,disposal=0,blend=0)
with Image.open(P/'bare/source-enter.png') as ap:
    assert ap.n_frames==7
    for i,im in enumerate(poses):
        ap.seek(i)
        assert ap.convert('RGBA').tobytes()==im.tobytes()
        assert ap.info['duration']==times[i]
board=Image.new('RGB',(2560,720),'#182932')
d=ImageDraw.Draw(board)
master=Image.open(P.parent/'crew-side-masters-v1/bill-side-master-01.png').convert('RGB')
scale=148/956
sm=master.crop((850,0,1280,1024)).resize((round(430*scale),round(1024*scale)),Image.Resampling.LANCZOS)
for row in range(2):
    y=row*360
    board.paste(sm,(125,y+25+224-round(977*scale)))
    d.text((5,y+5),'Original West master /148 ruler',fill='white')
    for i,name in enumerate(['idle','arm ready','crouch','push-off','compact lift','near-prone','swim']):
        im=Image.open(P.parent/'bill-land-water-west-v2'/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA') if row==0 else poses[i]
        x=(i+1)*320
        board.paste(im,(x,y+25),im)
        d.text((x+5,y+5),('V2 ' if row==0 else 'V3 ')+name,fill='white')
        d.line((x,y+101,x+319,y+101),fill='#61707c')
        if i<3:d.line((x,y+249,x+319,y+249),fill='#6aa39e')
board.save(P/'master-comparison.png')
record={'scope':'Source-only seven pose500ms West entry revision, unselected. Crouch/push graphite texture and badge edits; complete material/identity acceptance pending. No native motion/helmet/Continue/normal admission claim.','registrations':registrations,'exactPreservedFrameIndices':preserved,'decodedAPNGFramesExact':7,'durationsMs':times,'totalMs':sum(times),'sourceSHA256':{str(f.relative_to(P.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs}}
(P/'review.json').write_text(json.dumps(record,indent=2)+'\n')
(P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill West compact entry revision</title><style>body{background:#182932;color:#eee;font:16px sans-serif}img{max-width:100%}</style><h1>Bill West — compact entry revision</h1><p>'+record['scope']+'</p><img src="bare/source-enter.png"><h2>V2 above / V3 below, common master ruler</h2><img src="master-comparison.png">')
print(json.dumps({'poses':7,'unchangedPoses':preserved,'decodedExact':7,'ms':sum(times),'registration':registrations}))
