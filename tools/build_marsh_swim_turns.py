"""Reproduce selected swimming turns from frozen authored sources."""
from pathlib import Path
import argparse, hashlib, json, shutil
import numpy as np
from scipy.ndimage import label
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-swim-turns-v1'
OUT = BASE / 'review/east-north-01'
PAIRS = ['east-north', 'west-north', 'east-south', 'west-south']

def build(install=False, pair='east-north'):
    assert pair in PAIRS
    origin, destination = pair.split('-')
    OUT = BASE / f'review/{pair}-01'
    OUT.mkdir(parents=True, exist_ok=True)
    names = [f'{pair}-01.png', 'east-north-02.png' if pair=='east-north' else f'{pair}-01.png', f'swim-{origin}-endpoint.png', f'swim-{destination}-endpoint.png']
    sources = [Image.open(BASE/'sources'/n).convert('RGBA') for n in names]
    assert sources[0].size == sources[1].size == (2172,724)
    poses = []
    records = []
    anchors = [(436,366),(1154,358),(1810,368)] if origin=='east' else [(318,366),(980,348),(1813,369)]
    targets = [(100,137),(97,132),(94,128)] if origin=='east' else [(84,137),(87,132),(90,128)]
    if pair=='east-south':
        anchors=[(350,385),(1095,379),(1766,364)]
        targets=[(97,137),(87,133),(77,128)]
    if pair=='west-south':
        anchors=[(373,444),(1156,407),(1700,398)]
        targets=[(84,137),(109,133),(78,128)]
    for i, (anchor, target) in enumerate(zip(anchors, targets)):
        source_index = 1 if i == 2 else 0
        tile = sources[source_index].crop((724*i,0,724*(i+1),724))
        labels,_ = label(np.asarray(tile)[:,:,3]>=192)
        sizes = np.bincount(labels.ravel()); sizes[0] = 0
        tile.putalpha(Image.fromarray(((labels==sizes.argmax())*255).astype('uint8')))
        scale = .23
        dense = tile.resize((round(724*scale),)*2, Image.Resampling.BOX)
        dense.putalpha(dense.getchannel('A').point(lambda a:255 if a>=128 else 0))
        offset = (round(target[0]-(anchor[0]-724*i)*scale),round(target[1]-anchor[1]*scale))
        frame = Image.new('RGBA',(184,208)); frame.alpha_composite(dense,offset)
        box = frame.getbbox()
        assert box and box[0]>0 and box[1]>0 and box[2]<184 and box[3]<208, box
        poses.append(frame)
        records.append(dict(source=names[source_index],cell=i,shoulder=anchor,target=target,scale=scale,offset=offset))
    endpoints=[]
    for source in sources[2:]:
        frame=Image.new('RGBA',(184,208));frame.alpha_composite(source);endpoints.append(frame)
    row=[endpoints[0],*poses,endpoints[1]]
    clips={f'swim-turn-{pair}':row,f'swim-turn-{destination}-{origin}':list(reversed(row))}
    states=[]
    for state, frames in clips.items():
        files=[]
        for i, frame in enumerate(frames):
            name=f'{state}-{i:03}.png';frame.save(OUT/name);files.append(name)
        forward=state.endswith(pair)
        states.append(dict(id=state,frameFiles=files,frameDurationsMs=[60,90,100,90,60],loop=False,
            facings=[origin,origin,destination,destination,destination] if forward else [destination,destination,destination,origin,origin],
            waterKinds=['transition']*5,waterPoses=[True]*5,depthOffsets=[0.0]*5))
    manifest=dict(frameWidth=184,frameHeight=208,pivot=[92,172],standingHeight=148,states=states)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    provenance=dict(sources={n:hashlib.sha256((BASE/'sources'/n).read_bytes()).hexdigest() for n in names},registration=records,
        derived='Return turn reverses forward poses. Existing endpoint pixels preserved with transparent bottom padding. '+('First two poses from source 01; third from corrected source 02.' if pair=='east-north' else f'All three poses from independently authored {pair} source 01.'))
    (OUT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    board=Image.new('RGB',(920,232),'#17212a');draw=ImageDraw.Draw(board)
    for i, frame in enumerate(row):
        board.paste(frame,(184*i,24),frame);draw.text((184*i+6,6),str(i),fill='white')
    board.save(OUT/'contact.png')
    preview=[]
    for state,frames in clips.items():
        for frame in frames:
            board=Image.new('RGB',(240,244),'#17212a');ImageDraw.Draw(board).text((8,6),state,fill='white');board.paste(frame,(28,28),frame);preview.append(board)
    preview[0].save(OUT/'motion.gif',save_all=True,append_images=preview[1:],duration=[350,90,100,90,350]*2,loop=0)
    if install:
        runtime=ROOT/'character/marsh-v2';folder=runtime/f'supplemental/swim-turn-{pair}';folder.mkdir(parents=True,exist_ok=True)
        for state in states:
            for name in state['frameFiles']:shutil.copyfile(OUT/name,folder/name)
        for name in ['manifest.json','provenance.json']:shutil.copyfile(OUT/name,folder/name)
        path=runtime/'catalog.json';catalog=json.loads(path.read_text());relative=f'supplemental/swim-turn-{pair}/manifest.json'
        if relative not in catalog['body']:catalog['body'].append(relative)
        path.write_text(json.dumps(catalog,indent=2)+'\n')
    print('10 turn frames; '+('installed' if install else 'review only'))
    return clips

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--install',action='store_true');parser.add_argument('--pair',choices=PAIRS,default='east-north');args=parser.parse_args();build(args.install,args.pair)
