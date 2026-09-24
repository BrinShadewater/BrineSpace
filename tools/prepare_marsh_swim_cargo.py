"""Prepare a loaded swimming source for review; no runtime installation."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-swim-cargo-v1'
def build(direction='east'):
    assert direction in ['east','west','north','south']
    source=BASE/f'sources/{direction}-loop-{"02" if direction=="north" else "01"}.png';raw=Image.open(source).convert('RGBA');assert raw.size==(2172,724)
    out=BASE/f'review/{direction}-loop-01';out.mkdir(parents=True,exist_ok=True)
    frames=[];records=[]
    centers=[350,892,1435,1978] if direction=='east' else [218,761,1304,1847]
    target_x=120 if direction=='east' else 104
    source_y=391 if direction=='east' else 370
    target_y=136;scale=.32
    if direction=='north':centers=[285,814,1358,1889];target_x=112;source_y=315;target_y=138;scale=.25
    if direction=='south':centers=[264,807,1350,1893];target_x=112;source_y=422;target_y=138;scale=.25
    for i,x in enumerate(centers):
        tile=raw.crop((543*i,0,543*(i+1),724))
        labels,_=label(np.asarray(tile)[:,:,3]>=192);sizes=np.bincount(labels.ravel());sizes[0]=0
        tile.putalpha(Image.fromarray(((labels==sizes.argmax())*255).astype('uint8')))
        dense=tile.resize((round(543*scale),round(724*scale)),Image.Resampling.BOX)
        dense.putalpha(dense.getchannel('A').point(lambda a:255 if a>=128 else 0))
        offset=(round(target_x-(x-543*i)*scale),round(target_y-source_y*scale))
        frame=Image.new('RGBA',(224,208));frame.alpha_composite(dense,offset)
        box=frame.getbbox();assert box and box[0]>0 and box[1]>0 and box[2]<224 and box[3]<208
        assert set(frame.getchannel('A').tobytes())<={0,255}
        frame.save(out/f'{i:03}.png');frames.append(frame);records.append(dict(cell=i,shoulder=[x,source_y],target=[target_x,target_y],scale=scale,offset=offset))
    board=Image.new('RGB',(896,232),'#17212a')
    for i,f in enumerate(frames):board.paste(f,(224*i,24),f)
    board.save(out/'contact.png');preview=[]
    for f in frames:
        board=Image.new('RGB',(280,244),'#17212a');ImageDraw.Draw(board).text((8,6),'Marsh loaded swim - candidate',fill='white');board.paste(f,(28,28),f);preview.append(board)
    preview[0].save(out/'motion.gif',save_all=True,append_images=preview[1:],duration=180,loop=0)
    (out/'provenance.json').write_text(json.dumps(dict(status='review-only; not installed',source=str(source.relative_to(ROOT)),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),registration=records,canvas=[224,208],pivot=[112,172],standingHeight=148),indent=2)+'\n')
    print('Four review frames, binary alpha, no border touches; runtime unchanged')
if __name__=='__main__':build()
