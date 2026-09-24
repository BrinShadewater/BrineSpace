"""Build Marsh bed-edge contact clips from the preserved source; no generation calls."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]

def build():
    root=ROOT
    out=root/'character/marsh-berth-v1'
    raw=out/'contact-source.png'
    a=np.array(Image.open(raw).convert('RGBA'))
    a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0,:3]=0
    im=Image.fromarray(a)
    runs=[];start=None
    for x,used in enumerate(np.any(a[:,:,3]>0,axis=0).tolist()+[False]):
        if used and start is None:start=x
        if not used and start is not None:
            if x-start>20:runs.append((start,x))
            start=None
    assert len(runs)==6,runs
    boxes=[]
    for left,right in runs:
        b=im.crop((left,0,right,im.height)).getbbox()
        boxes.append((left+b[0],b[1],left+b[2],b[3]))
    scale=148/(boxes[0][3]-boxes[0][1])
    # Hand-reviewed source-space pelvis landmarks, not per-frame bounding-box alignment.
    hips=[(194,414),(503,421),(866,427),(1258,410),(1603,397),(1951,398)]
    canonical=np.array(Image.open(root/'character/marsh-v2/frames/bare/idle-south/000.png').convert('RGBA'))
    palette=Image.fromarray(canonical[canonical[:,:,3]>0,:3].reshape(1,-1,3)).quantize(colors=256)
    target=root/'character/marsh-v2/supplemental/berth-east';target.mkdir(parents=True,exist_ok=True)
    board=Image.new('RGBA',(6*184,184),(26,35,39,255))
    for i,(box,hip) in enumerate(zip(boxes,hips)):
        tile=im.crop(box);tile=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.NEAREST)
        alpha=tile.getchannel('A');tile=tile.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');tile.putalpha(alpha)
        xy=(92-round((hip[0]-box[0])*scale),115-round((hip[1]-box[1])*scale))
        assert min(xy)>=0 and xy[0]+tile.width<=184 and xy[1]+tile.height<=184,(i,xy,tile.size)
        frame=Image.new('RGBA',(184,184));frame.alpha_composite(tile,xy)
        frame.save(target/f'{i:03}.png');board.alpha_composite(frame,(184*i,0))
    board.save(out/'extraction-review.png')
    (target/'recipe.json').write_text(json.dumps(dict(source='character/marsh-berth-v1/contact-source.png',source_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),source_boxes=boxes,source_hips=hips,shared_scale=scale,registered_hip=[92,115],pivot=[92,172],canonical_idle='character/marsh-v2/frames/bare/idle-east/000.png',canonical_idle_sha256=hashlib.sha256((root/'character/marsh-v2/frames/bare/idle-east/000.png').read_bytes()).hexdigest(),rise_derivation='Reverse lie-down frames and durations; endpoints shared'),indent=2)+'\n')
    # Final idle uses the canonical profile below.
    
    shutil.copyfile(root/'character/marsh-v2/frames/bare/idle-east/000.png',target/'000.png')
    durations=[120,300,300,300,300,280]
    states=[]
    for name,indices,times,loop in [('berth-lie-east',list(range(6)),durations,False),('berth-sleep-east',[5],[1000],True),('berth-rise-east',list(reversed(range(6))),list(reversed(durations)),False)]:
        states.append(dict(id=name,frameFiles=[f'{i:03}.png' for i in indices],frameDurationsMs=times,loop=loop,depthOffsets=[32 if i==0 else 64 if i==1 else 96 for i in indices]))
    (target/'manifest.json').write_text(json.dumps(dict(frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,states=states),indent=2)+'\n')
    catalog_path=root/'character/marsh-v2/catalog.json'
    catalog=json.loads(catalog_path.read_text());relative='supplemental/berth-east/manifest.json'
    if relative not in catalog['body']:catalog['body'].append(relative)
    catalog_path.write_text(json.dumps(catalog,indent=2)+'\n')
    return {'states':3,'unique_frames':6,'transition_ms':sum(durations)}

if __name__=="__main__":print(build())
