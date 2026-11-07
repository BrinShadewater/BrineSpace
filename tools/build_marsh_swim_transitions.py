"""Prepare independently authored, torso-registered directional start/stop pairs."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-swim-transitions-v1'
OUT=BASE/'review/east-01'
DIRECTIONS=['east','west','north','south']

def build(install=False,direction='east'):
    assert direction in DIRECTIONS
    OUT=BASE/f'review/{direction}-01'
    OUT.mkdir(parents=True,exist_ok=True)
    axial=direction in ['north','south']
    names=['axial-start-01.png' if axial else f'{direction}-start-01.png',f'tread-{direction}-endpoint.png',f'swim-{direction}-endpoint.png']
    raw=Image.open(BASE/'sources'/names[0]).convert('RGBA')
    assert raw.size==((1536,1024) if axial else (2172,724)),'Source changed: remeasure torso landmarks'
    poses=[];records=[]
    anchors=[(344,328),(1080,370),(1856,432)] if direction=='east' else [(366,324),(1028,340),(1750,394)]
    targets=[(86,117),(94,128),(100,136)] if direction=='east' else [(95,116),(89,128),(83,136)]
    if axial:
        anchors=[(260,267),(770,280),(1276,289)] if direction=='north' else [(260,742),(768,766),(1280,790)]
        targets=[(92,119),(92,123),(92,126)] if direction=='north' else [(94,112),(96,122),(98,132)]
    canvas=(184,208) if direction=='west' else (184,184)
    size=512 if axial else 724
    y0=512 if direction=='south' else 0
    for i,(anchor,target) in enumerate(zip(anchors,targets)):
        cell=(i*size,y0,(i+1)*size,y0+size);tile=raw.crop(cell)
        labels,_=label(np.asarray(tile)[:,:,3]>=192);sizes=np.bincount(labels.ravel());sizes[0]=0
        tile.putalpha(Image.fromarray(((labels==sizes.argmax())*255).astype('uint8')))
        scale=.30 if axial else .24;dense=tile.resize((round(size*scale),round(size*scale)),Image.Resampling.BOX)
        dense.putalpha(dense.getchannel('A').point(lambda a:255 if a>=128 else 0))
        offset=(round(target[0]-(anchor[0]-cell[0])*scale),round(target[1]-(anchor[1]-cell[1])*scale))
        frame=Image.new('RGBA',canvas);frame.alpha_composite(dense,offset)
        box=frame.getbbox();assert box and box[0]>0 and box[1]>0 and box[2]<canvas[0] and box[3]<canvas[1],(i,box)
        poses.append(frame);records.append(dict(cell=cell,sourceShoulder=anchor,targetShoulder=target,scale=scale,offset=offset))
    endpoints=[]
    for name in names[1:]:
        endpoint=Image.new('RGBA',canvas);endpoint.alpha_composite(Image.open(BASE/'sources'/name).convert('RGBA'));endpoints.append(endpoint)
    start=[endpoints[0],*poses,endpoints[1]]
    clips={f'swim-start-{direction}':start,f'swim-stop-{direction}':list(reversed(start))}
    states=[]
    for state,row in clips.items():
        files=[]
        for i,frame in enumerate(row):
            name=f'{state}-{i:03}.png';frame.save(OUT/name);files.append(name)
        states.append(dict(id=state,frameFiles=files,frameDurationsMs=[60,90,100,90,60],loop=False,
                           facings=[direction]*5,waterKinds=['transition']*5,waterPoses=[True]*5,depthOffsets=[0.0]*5))
    manifest=dict(frameWidth=canvas[0],frameHeight=canvas[1],pivot=[92,172],standingHeight=148,states=states)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    provenance=dict(sources={n:hashlib.sha256((BASE/'sources'/n).read_bytes()).hexdigest() for n in names},registration=records,derived='Stop reverses authored start poses; unchanged tread/swim zero-frame endpoints, transparent padding only',scope=direction+' start and stop only; no cargo or turns')
    (OUT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    board=Image.new('RGB',(920,canvas[1]+24),'#17212a');d=ImageDraw.Draw(board)
    for i,f in enumerate(start):board.paste(f,(184*i,24),f);d.text((184*i+4,5),f'{direction} start {i}',fill='white')
    board.save(OUT/'contact.png')
    preview=[];durations=[]
    for state in clips:
        for i,f in enumerate(clips[state]):
            board=Image.new('RGB',(240,canvas[1]+36),'#17212a');d=ImageDraw.Draw(board);d.text((8,6),state,fill='white');board.paste(f,(28,28),f)
            preview.append(board);durations.append([350,90,100,90,350][i])
    preview[0].save(OUT/'motion.gif',save_all=True,append_images=preview[1:],duration=durations,loop=0)
    if install:
        import shutil
        runtime=ROOT/'character/marsh-v2';folder=runtime/f'supplemental/swim-{direction}';folder.mkdir(parents=True,exist_ok=True)
        for state in states:
            for name in state['frameFiles']:shutil.copyfile(OUT/name,folder/name)
        for name in ['manifest.json','provenance.json']:shutil.copyfile(OUT/name,folder/name)
        path=runtime/'catalog.json';catalog=json.loads(path.read_text());relative=f'supplemental/swim-{direction}/manifest.json'
        if relative not in catalog['body']:catalog['body'].append(relative)
        path.write_text(json.dumps(catalog,indent=2)+'\n')
    print('10 '+direction+' transition frames;', 'installed' if install else 'review only')
    return clips

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--install',action='store_true');parser.add_argument('--direction',choices=DIRECTIONS,default='east');args=parser.parse_args();build(args.install,args.direction)
