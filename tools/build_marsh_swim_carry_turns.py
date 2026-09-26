"""Registered loaded-swimming turns from frozen sources and exact selected endpoints."""
from pathlib import Path
import argparse, hashlib, json, shutil
import numpy as np
from scipy.ndimage import label
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-swim-carry-turns-v1'
PAIRS=['east-north','west-north','east-south','west-south']
REGISTRATION={
    'east-north':dict(scale=.24,anchors=[(483,400),(1236,378),(1844,376)],targets=[(119,137),(117,138),(114,138)],revisions=['01','01','02']),
    'west-north':dict(scale=.24,anchors=[(303,395),(1044,405),(1785,401)],targets=[(105,137),(108,138),(110,138)],revisions=['01']*3),
    'east-south':dict(scale=.22,anchors=[(496,415),(1171,436),(1854,457)],targets=[(119,137),(117,138),(114,138)],revisions=['01','01','02']),
    'west-south':dict(scale=.22,anchors=[(356,420),(1139,420),(1835,435)],targets=[(105,137),(108,138),(110,138)],revisions=['01']*3),
}

def write_clips(clips,durations,facings,out,provenance,install,pair):
    out.mkdir(parents=True,exist_ok=True);states=[]
    for key,frames in clips.items():
        files=[]
        for i,frame in enumerate(frames):
            name=f'{key}-{i:03}.png';frame.save(out/name);files.append(name)
        states.append(dict(id=key,frameFiles=files,frameDurationsMs=durations,loop=False,
            facings=facings if key.endswith(pair) else list(reversed(facings)),
            waterKinds=['transition']*len(frames),waterPoses=[True]*len(frames),depthOffsets=[0.0]*len(frames)))
    manifest=dict(frameWidth=224,frameHeight=208,pivot=[112,172],standingHeight=148,states=states)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    row=next(iter(clips.values()));board=Image.new('RGB',(224*len(row),232),'#17212a')
    for i,f in enumerate(row):board.paste(f,(224*i,24),f)
    board.save(out/'contact.png');preview=[]
    for key,frames in clips.items():
        for f in frames:
            b=Image.new('RGB',(300,244),'#17212a');ImageDraw.Draw(b).text((8,6),key,fill='white');b.paste(f,(38,28),f);preview.append(b)
    preview[0].save(out/'motion.gif',save_all=True,append_images=preview[1:],duration=[350,*durations[1:-1],350]*2,loop=0)
    if install:
        runtime=ROOT/'character/marsh-v2';relative=f'supplemental/swim-carry-turn-{pair}';folder=runtime/relative;folder.mkdir(parents=True,exist_ok=True)
        for state in states:
            for name in state['frameFiles']:shutil.copyfile(out/name,folder/name)
        for name in ['manifest.json','provenance.json']:shutil.copyfile(out/name,folder/name)
        p=runtime/'catalog.json';catalog=json.loads(p.read_text())
        if relative+'/manifest.json' not in catalog['body']:catalog['body'].append(relative+'/manifest.json')
        p.write_text(json.dumps(catalog,indent=2)+'\n')

def build(install=False,pair='east-north'):
    assert pair in PAIRS
    origin,destination=pair.split('-');config=REGISTRATION[pair];poses=[];records=[];sources={}
    for i,(anchor,target,revision) in enumerate(zip(config['anchors'],config['targets'],config['revisions'])):
        name=f'{pair}-{revision}.png';p=BASE/'sources'/name;sources[name]=hashlib.sha256(p.read_bytes()).hexdigest()
        raw=Image.open(p).convert('RGBA');assert raw.size in [(2172,724),(2170,725)]
        left=round(i*raw.width/3);right=round((i+1)*raw.width/3)
        tile=raw.crop((left,0,right,raw.height));labels,_=label(np.asarray(tile)[:,:,3]>=192)
        sizes=np.bincount(labels.ravel());sizes[0]=0
        tile.putalpha(Image.fromarray(((labels==sizes.argmax())*255).astype('uint8')))
        scale=config['scale'];dense=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX)
        dense.putalpha(dense.getchannel('A').point(lambda a:255 if a>=128 else 0))
        offset=(round(target[0]-(anchor[0]-left)*scale),round(target[1]-anchor[1]*scale))
        f=Image.new('RGBA',(224,208));f.alpha_composite(dense,offset);box=f.getbbox()
        assert box and 0<box[0] and 0<box[1] and box[2]<224 and box[3]<208,(pair,i,box)
        poses.append(f);records.append(dict(source=name,cell=[left,0,right,raw.height],shoulder=anchor,target=target,scale=scale,offset=offset))
    endpoints=[]
    for direction in [origin,destination]:
        name=f'swim-carry-{direction}-endpoint.png';p=BASE/'sources'/name;sources[name]=hashlib.sha256(p.read_bytes()).hexdigest()
        f=Image.open(p).convert('RGBA');assert f.size==(224,208);endpoints.append(f)
    row=[endpoints[0],*poses,endpoints[1]]
    clips={f'swim-carry-turn-{pair}':row,f'swim-carry-turn-{destination}-{origin}':list(reversed(row))}
    write_clips(clips,[60,90,100,90,60],[origin,origin,destination,destination,destination],BASE/f'review/{pair}-01',
        dict(sources=sources,registration=records,derived='Exact selected loaded frame-zero endpoints; return reverses poses. Revised third angles selected for east/north and east/south; no mirrored art.'),install,pair)
    return clips

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--install',action='store_true');p.add_argument('--pair',choices=PAIRS,default='east-north');a=p.parse_args();build(a.install,a.pair)
