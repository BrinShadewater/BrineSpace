"""Select authored pose sources; preserve empty carried helmet in overhead phase."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(); parser.add_argument('--actor',choices=['veld','branforth'],default='veld')
actor=parser.parse_args().actor
out=ROOT/'pilot'/f'{actor}-equip-helmet-east'; out.mkdir(exist_ok=True)
sheet=Image.new('RGB',(1104,230),'#1d252a'); draw=ImageDraw.Draw(sheet)
evidence=[]
for i in range(6):
    revision=3 if actor=='veld' else 1
    source=ROOT/'generated'/f'{actor}-equip-helmet-east-candidate-{revision:02}.png'
    im=Image.open(source).convert('RGBA'); a=np.array(im)
    key=(a[:,:,0].astype(int)>a[:,:,1].astype(int)+35)&(a[:,:,2].astype(int)>a[:,:,1].astype(int)+35); a[key]=0
    im=Image.fromarray(a); active=(a[:,:,3]>0).sum(axis=0)>3
    runs=[]; start=None
    for x,on in enumerate(list(active)+[False]):
        if on and start is None: start=x
        if not on and start is not None:
            if x-start>25: runs.append((start,x))
            start=None
    assert len(runs)==6
    left,right=runs[i]; part=im.crop((left,0,right,im.height)); box=part.getbbox(); part=part.crop(box)
    body_height=566-154 if actor=='veld' else 547-211
    scale=74/(body_height/683*im.height)
    boot_x=([195,548,890,1234,1550,1870] if actor=='veld' else [178,520,820,1174,1534,1870])[i]/2048*im.width
    sprite=part.resize((round(part.width*scale),round(part.height*scale)),Image.Resampling.BOX)
    sprite.putalpha(sprite.getchannel('A').point(lambda v:255 if v>=128 else 0))
    position=(46-round((boot_x-left-box[0])*scale),98-sprite.height)
    frame=Image.new('RGBA',(92,104)); frame.alpha_composite(sprite,position); frame.save(out/f'frame_{i:03}.png')
    big=frame.resize((184,208),Image.Resampling.NEAREST); sheet.paste(big,(i*184,22),big)
    evidence.append({'source':str(source.relative_to(ROOT)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourcePose':i,'scale':scale,'placement':position,'sourceBounds':[left+box[0],box[1],left+box[2],box[3]]})
draw.text((5,4),actor+' donning / pose selection pilot / not runtime accepted',fill='white'); sheet.save(out/'contact.png')
(out/'sources.json').write_text(json.dumps(evidence,indent=2)+'\n')
(out/'manifest.json').write_text(json.dumps({'status':'donning_pilot_not_runtime','frameWidth':92,'frameHeight':104,'pivot':[46,98],'states':[{'id':'equip-helmet-east','frameCount':6,'frameFiles':[f'frame_{i:03}.png' for i in range(6)],'frameDurationsMs':[180,180,220,220,260,240],'loop':False}]},indent=2)+'\n')
