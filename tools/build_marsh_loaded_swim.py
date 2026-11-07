"""Selected loaded-swimming repairs, preserving other runtime states."""
from pathlib import Path
import json,shutil,hashlib
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
from prepare_marsh_swim_cargo import build as prepare_loop,ROOT,BASE
KEYS=['swim-pickup-east','swim-carry-east']
DIRECTIONS=['east','west','north','south']
def build(install=False,direction='east'):
    assert direction in DIRECTIONS
    KEYS=[f'swim-pickup-{direction}',f'swim-carry-{direction}']
    prepare_loop(direction);out=BASE/f'review/{direction}-chain-01';out.mkdir(parents=True,exist_ok=True)
    loop=[Image.open(BASE/f'review/{direction}-loop-01/{i:03}.png').convert('RGBA') for i in range(4)]
    raw=Image.open(BASE/f'sources/{direction}-pickup-01.png').convert('RGBA')
    edges=[0,525,1010,1585,2172];anchors=[(219,300),(779,350),(1355,440),(1975,476)]
    targets=[(108,94),(114,112),(120,132),(120,136)];poses=[];records=[]
    if direction=='west':
        edges=[0,543,1086,1629,2172]
        anchors=[(390,277),(842,298),(1314,335),(1866,388)]
        targets=[(118,88),(104,108),(104,127),(104,136)]
    if direction=='north':
        edges=[0,543,1086,1629,2172]
        anchors=[(332,282),(848,311),(1358,331),(1851,426)]
        targets=[(112,80),(112,98),(112,119),(112,137)]
    if direction=='south':
        edges=[0,543,1086,1629,2172]
        anchors=[(276,214),(811,300),(1358,232),(1903,438)]
        targets=[(112,80),(112,103),(112,90),(112,138)]
    for i,(anchor,target) in enumerate(zip(anchors,targets)):
        tile=raw.crop((edges[i],0,edges[i+1],724))
        # Preserve detached case components in the first reach pose.
        labels,_=label(np.asarray(tile)[:,:,3]>=192);sizes=np.bincount(labels.ravel());sizes[0]=0
        keep=np.flatnonzero(sizes>=500);tile.putalpha(Image.fromarray((np.isin(labels,keep)*255).astype('uint8')))
        scale=.24 if direction=='south' else .28 if direction=='north' else .30
        dense=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX)
        dense.putalpha(dense.getchannel('A').point(lambda a:255 if a>=128 else 0))
        offset=(round(target[0]-(anchor[0]-edges[i])*scale),round(target[1]-anchor[1]*scale))
        f=Image.new('RGBA',(224,208));f.alpha_composite(dense,offset);box=f.getbbox()
        assert box and box[0]>0 and box[1]>0 and box[2]<224 and box[3]<208,(i,box)
        poses.append(f);records.append(dict(cell=[edges[i],0,edges[i+1],724],anchor=anchor,target=target,scale=scale,offset=offset))
    empty=Image.new('RGBA',(224,208));empty.alpha_composite(Image.open(BASE/f'sources/salvage-{direction}-endpoint.png').convert('RGBA'),(20,0))
    clips={KEYS[0]:[empty,*poses,loop[0]],KEYS[1]:[loop[i] for i in [0,1,2,3,2,1]]}
    states=[]
    for key,frames in clips.items():
        files=[]
        for i,f in enumerate(frames):name=f'{key}-{i:03}.png';f.save(out/name);files.append(name)
        states.append(dict(id=key,frameFiles=files,frameDurationsMs=[150 if key==KEYS[0] else 180]*6,loop=key==KEYS[1],facings=[direction]*6,waterKinds=['swim-pickup' if key==KEYS[0] else 'swim-carry']*6,waterPoses=[True]*6,depthOffsets=[0.0]*6))
    manifest=dict(frameWidth=224,frameHeight=208,pivot=[112,172],standingHeight=148,states=states)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    sources=[f'{direction}-loop-{"02" if direction=="north" else "01"}.png',f'{direction}-pickup-01.png',f'salvage-{direction}-endpoint.png']
    (out/'provenance.json').write_text(json.dumps(dict(sources={n:hashlib.sha256((BASE/'sources'/n).read_bytes()).hexdigest() for n in sources},pickupRegistration=records,derived='Pickup uses exact salvage first frame and exact loaded-swim endpoint. Four loop poses played 0,1,2,3,2,1 to retain six-frame timing.'),indent=2)+'\n')
    board=Image.new('RGB',(224*6,232),'#17212a')
    for i,f in enumerate(clips[KEYS[0]]):board.paste(f,(224*i,24),f)
    board.save(out/'contact.png');preview=[]
    for key,frames in clips.items():
        for f in frames:
            b=Image.new('RGB',(280,244),'#17212a');ImageDraw.Draw(b).text((8,6),key,fill='white');b.paste(f,(28,28),f);preview.append(b)
    preview[0].save(out/'motion.gif',save_all=True,append_images=preview[1:],duration=[150]*6+[180]*6,loop=0)
    if install:
        runtime=ROOT/'character/marsh-v2';relative=f'supplemental/loaded-swim-{direction}/manifest.json';folder=(runtime/relative).parent;folder.mkdir(parents=True,exist_ok=True)
        catalog=json.loads((runtime/'catalog.json').read_text())
        for rel in catalog['body']:
            if rel==relative:continue
            p=runtime/rel;m=json.loads(p.read_text());filtered=[s for s in m['states'] if s['id'] not in KEYS]
            if len(filtered)!=len(m['states']):m['states']=filtered;p.write_text(json.dumps(m,indent=2)+'\n')
        for s in states:
            for name in s['frameFiles']:shutil.copyfile(out/name,folder/name)
        for name in ['manifest.json','provenance.json']:shutil.copyfile(out/name,folder/name)
        if relative not in catalog['body']:catalog['body'].append(relative)
        (runtime/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
    return clips
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--install',action='store_true');p.add_argument('--direction',choices=DIRECTIONS,default='east');args=p.parse_args();build(args.install,args.direction)
