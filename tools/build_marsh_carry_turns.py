"""Registered carry turns; cargo stays in front of the rotating actor."""
import json,hashlib,shutil
from pathlib import Path
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-carry-turns-v1'
PAIRS=['east-north','west-north','east-south','west-south']
def build(install=False,pair='east-north'):
    assert pair in PAIRS
    origin,destination=pair.split('-')
    out=BASE/f'review/{pair}-01';out.mkdir(parents=True,exist_ok=True)
    names=[f'{pair}-01.png',f'carry-{origin}-endpoint.png',f'carry-{destination}-endpoint.png']
    raw=Image.open(BASE/'sources'/names[0]).convert('RGBA');assert raw.size==(2172,724)
    poses=[];records=[]
    centers=[442,1089,1713] if origin=='east' else [479,1100,1785]
    if pair=='east-south':centers=[357,1080,1810]
    if pair=='west-south':centers=[480,1076,1687]
    for i,center in enumerate(centers):
        tile=raw.crop((724*i,0,724*(i+1),724))
        labels,_=label(np.asarray(tile)[:,:,3]>=192);sizes=np.bincount(labels.ravel());sizes[0]=0
        tile.putalpha(Image.fromarray(((labels==sizes.argmax())*255).astype('uint8')))
        scale=.25 if origin=='east' else .265
        if pair=='east-south':scale=.23
        if pair=='west-south':scale=.24
        dense=tile.resize((round(724*scale),)*2,Image.Resampling.BOX)
        dense.putalpha(dense.getchannel('A').point(lambda a:255 if a>=128 else 0))
        box=dense.getbbox();offset=(round(92-(center-724*i)*scale),172-box[3])
        frame=Image.new('RGBA',(184,184));frame.alpha_composite(dense,offset)
        box=frame.getbbox();assert box and box[0]>0 and box[1]>0 and box[2]<184 and box[3]<184
        poses.append(frame);records.append(dict(cell=i,sourceCenter=center,scale=scale,offset=offset))
    row=[Image.open(BASE/'sources'/names[1]).convert('RGBA'),*poses,Image.open(BASE/'sources'/names[2]).convert('RGBA')]
    clips={f'carry-turn-{pair}':row,f'carry-turn-{destination}-{origin}':list(reversed(row))};states=[]
    for key,frames in clips.items():
        files=[]
        for i,frame in enumerate(frames):
            name=f'{key}-{i:03}.png';frame.save(out/name);files.append(name)
        states.append(dict(id=key,frameFiles=files,frameDurationsMs=[60,90,100,90,60],loop=False,
            facings=[origin,origin,destination,destination,destination] if key.endswith(pair) else [destination,destination,destination,origin,origin],waterKinds=['carry']*5,waterPoses=[False]*5,depthOffsets=[0.0]*5))
    manifest=dict(frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,states=states)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'provenance.json').write_text(json.dumps(dict(sources={n:hashlib.sha256((BASE/'sources'/n).read_bytes()).hexdigest() for n in names},registration=records,derived='Return reverses authored poses. Exact current carry frame-zero endpoints.'),indent=2)+'\n')
    board=Image.new('RGB',(920,208),'#17212a')
    for i,f in enumerate(row):board.paste(f,(184*i,24),f)
    board.save(out/'contact.png');preview=[]
    for key,frames in clips.items():
        for f in frames:
            board=Image.new('RGB',(240,220),'#17212a');ImageDraw.Draw(board).text((8,6),key,fill='white');board.paste(f,(28,28),f);preview.append(board)
    preview[0].save(out/'motion.gif',save_all=True,append_images=preview[1:],duration=[350,90,100,90,350]*2,loop=0)
    if install:
        runtime=ROOT/'character/marsh-v2';relative=f'supplemental/carry-turn-{pair}';folder=runtime/relative;folder.mkdir(parents=True,exist_ok=True)
        for state in states:
            for name in state['frameFiles']:shutil.copyfile(out/name,folder/name)
        for name in ['manifest.json','provenance.json']:shutil.copyfile(out/name,folder/name)
        path=runtime/'catalog.json';catalog=json.loads(path.read_text())
        if relative+'/manifest.json' not in catalog['body']:catalog['body'].append(relative+'/manifest.json')
        path.write_text(json.dumps(catalog,indent=2)+'\n')
    return clips
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--install',action='store_true');p.add_argument('--pair',choices=PAIRS,default='east-north');args=p.parse_args();build(args.install,args.pair)
