"""Package authored near-arm relaxation; immutable selected bunk is the body authority."""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw
import numpy as np
P=Path(__file__).resolve().parent; R=P.parents[1]
raw=Image.open(P/'raw-v1.png').convert('RGBA')
# One ruler, measured against first complete source pose. Never fit each pose.
scale=130/586
donors=[]
for i in range(3):
    cell=raw.crop((724*i,0,724*(i+1),724)).resize((round(724*scale),round(724*scale)),Image.Resampling.LANCZOS)
    im=Image.new('RGBA',(256,256));im.alpha_composite(cell,(31,125));donors.append(np.array(im))
mask=np.zeros((256,256),bool);mask[204:223,99:122]=True;mask[215:223,122:135]=True
board=Image.new('RGB',(1020,450),'#202a30');draw=ImageDraw.Draw(board);checks=0;bindings={}
for row,gear in enumerate(['bare','helmet']):
    source=R/f'character/dr-veld-v2/supplemental/bunk-east/{gear}/006.png'
    bindings[source.relative_to(R).as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest()
    base=Image.open(source).convert('RGBA');original=np.array(base);poses=[]
    dst=P/f'frames/{gear}/death-bunk-east';dst.mkdir(parents=True,exist_ok=True)
    for i in range(3):
        a=original.copy()
        if i:a[mask]=donors[i][mask]
        assert np.array_equal(a[~mask],original[~mask]);checks+=1
        assert not np.array_equal(a,original) if i else np.array_equal(a,original);checks+=1
        im=Image.fromarray(a);im.save(dst/f'{i:03}.png');poses.append(im)
        assert im.getbbox()==base.getbbox();checks+=1
        crop=im.crop((40,176,185,230)).resize((290,108),Image.Resampling.NEAREST)
        board.paste(crop,(i*340+10,row*220+65),crop);draw.text((i*340+10,row*220+35),f'{gear}: '+['selected live entry','relaxation','still'][i],fill='white')
    m={'name':'Veld staged supported bunk death '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_held_bunk_only_native_review_pending','states':[{'id':'death-bunk-east','frameFiles':[f'res://character/veld-bunk-death-east-v1/frames/{gear}/death-bunk-east/{i:03}.png' for i in range(3)],'frameDurationsMs':[180,280,420],'loop':False,'furnitureFrames':['bunk']*3,'depthOffsets':[100]*3}]}
    if gear=='helmet':m['equipment']='diving-helmet'
    (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    tiles=[]
    for im in poses:
        tile=Image.new('RGB',(256,256),'#202a30');tile.paste(im,(0,0),im);tiles.append(tile)
    tiles[0].save(P/f'{gear}-death-bunk-east.gif',save_all=True,append_images=tiles[1:],duration=[540,840,1260],loop=0)
board.save(P/'source-review.png')
bindings['character/veld-bunk-death-east-v1/raw-v1.png']=hashlib.sha256((P/'raw-v1.png').read_bytes()).hexdigest()
(P/'package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'sourceBindings':bindings,'rawResult':'exec-b32d13ce-f1c9-437f-8f17-6d45bddbd0d2','ruler':scale,'registration':[31,125],'insertRegions':[[99,204,122,223],[122,215,135,223]],'protected':'all pixels outside near forearm/glove, including head, shoulder badge, torso hardware, waist panel, knees, boots and bed contact','scope':'held specialised East bunk only; no partial entering/exiting coverage; no normal selection'},indent=2)+'\n')
print(f'{checks} protected-source/entry/contact checks,0 failures')
