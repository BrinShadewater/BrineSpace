"""Package grounded death pilots without changing accepted dry crew assets."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parent
for actor in ['bill', 'veld', 'branforth']:
    clip = actor + '-death-ground-east'
    source = ROOT/'generated'/f'{clip}.png'
    data = np.array(Image.open(source).convert('RGBA'))
    rgb = data[:,:,:3].astype(np.int16)
    key = (rgb[:,:,0] > rgb[:,:,1]+35) & (rgb[:,:,2] > rgb[:,:,1]+35)
    data[key] = 0
    edges = np.diff(np.r_[False, (data[:,:,3]>0).sum(axis=0)>3, False].astype(int))
    groups = [(int(a),int(b)) for a,b in zip(np.where(edges==1)[0],np.where(edges==-1)[0]) if b-a>25]
    assert len(groups)==6, (actor,groups)
    poses=[]
    for a,b in groups:
        im=Image.fromarray(data[:,a:b]);box=im.getbbox();poses.append((im.crop(box),box))
    top=min(box[1] for im,box in poses);ground=max(box[3] for im,box in poses)
    scale=74/(ground-top)
    out=ROOT/'pilot'/clip;out.mkdir(parents=True,exist_ok=True)
    frames=[];sheet=Image.new('RGB',(1104,206),'#1d252a');draw=ImageDraw.Draw(sheet)
    durations=[180,160,180,180,220,500]
    for i,(im,box) in enumerate(poses):
        im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.BOX)
        im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0))
        x=(92-im.width)//2;y=86-round((ground-box[1])*scale)
        assert x>=1 and y>=1 and x+im.width<92 and y+im.height<92,(actor,i)
        frame=Image.new('RGBA',(92,92));frame.alpha_composite(im,(x,y));frames.append(frame)
        frame.save(out/f'frame_{i:03}.png')
        big=frame.resize((184,184),Image.Resampling.NEAREST);sheet.paste(big,(i*184,22),big)
        draw.text((i*184+5,4),str(durations[i])+' ms',fill='white')
    sheet.save(out/'contact.png')
    preview=[]
    for frame in frames:
        bg=Image.new('RGB',(184,184),'#1d252a');im=frame.resize((184,184),Image.Resampling.NEAREST);bg.paste(im,(0,0),im);preview.append(bg)
    preview[0].save(out/'preview.gif',save_all=True,append_images=preview[1:],duration=durations)
    manifest={'status':'packaged_pilot_not_integrated','frameWidth':92,'frameHeight':92,'pivot':[46,86],'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':scale,'states':[{'id':'death-ground-east','frameFiles':[f'frame_{i:03}.png' for i in range(6)],'frameDurationsMs':durations,'loop':False,'terminalFrame':5}]}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(actor+': six grounded death frames, fixed scale, binary alpha, no clipping')
