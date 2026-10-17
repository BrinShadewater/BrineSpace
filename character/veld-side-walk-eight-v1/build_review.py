from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage
R=Path(__file__).resolve().parent
parents={'east':'veld-east-walk-matched-v1','west':'veld-west-walk-master-v3'}
states=[];audit=[];clips=[]
for direction,parent in parents.items():
    old=R.parent/parent;sid='walk-'+direction
    im=Image.open(R/'sources'/f'{direction}-inbetweens.png').convert('RGBA');a=np.array(im)[:,:,3]
    assert (a<8).mean()>.1
    lab,_=ndimage.label(a>=128);sizes=np.bincount(lab.ravel())
    parts=[(i+1,b) for i,b in enumerate(ndimage.find_objects(lab)) if b and sizes[i+1]>1000]
    assert len(parts)==4,len(parts)
    parts.sort(key=lambda p:p[1][0].start)
    parts=sorted(parts[:2],key=lambda p:p[1][1].start)+sorted(parts[2:],key=lambda p:p[1][1].start)
    scale=148/float(np.median([b[0].stop-b[0].start for _,b in parts]))
    folder=R/'frames'/sid;folder.mkdir(parents=True,exist_ok=True)
    paths=[];frames=[];boxes=[]
    for i,(label,(ys,xs)) in enumerate(parts):
        keypath=folder/f'{i*2:03}.png';keypath.write_bytes((old/f'frames/{sid}/{i:03}.png').read_bytes())
        box=(xs.start,ys.start,xs.stop,ys.stop);boxes.append(box);crop=im.crop(box)
        crop.putalpha(Image.fromarray(np.where(lab[ys,xs]==label,255,0).astype('uint8')))
        small=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
        _,xx=np.nonzero(np.array(crop)[:,:,3][int(crop.height*.05):int(crop.height*.14)]>=128)
        left=(100 if direction=='east' else 84)-round(float(np.median(xx))*scale)
        assert left>=2 and left+small.width<=182
        f=Image.new('RGBA',(184,184));f.alpha_composite(small,(left,172-small.height));p=folder/f'{i*2+1:03}.png';f.save(p)
        for path in [keypath,p]:paths.append(path.relative_to(R).as_posix());frames.append(Image.open(path).convert('RGBA'))
    durations=[112,113]*4
    frames[0].save(R/f'{sid}.webp',save_all=True,append_images=frames[1:],duration=durations,loop=0,lossless=True)
    states.append(dict(id=sid,frameFiles=paths,frameCount=8,frameDurationsMs=durations,loop=True,mirrored=False,provenance={'evenFrames':parent,'oddFrames':'generated in-betweens'}))
    clips.append(frames);audit.append(dict(state=sid,newSourceBoxes=boxes,uniformScale=scale,preservedKeys=4))
manifest=dict(name='Veld eight-frame side walk candidate',frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,status='review_candidate_not_installed',states=states)
(R/'manifest.json').write_text(json.dumps(manifest,indent=2));(R/'extraction.json').write_text(json.dumps(audit,indent=2))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20);review=[]
for i in range(8):
    canvas=Image.new('RGB',(736,480),'#263139');d=ImageDraw.Draw(canvas)
    for col,(direction,frames) in enumerate(zip(parents,clips)):
        f=frames[i];big=f.resize((368,368),Image.Resampling.NEAREST);canvas.paste(big,(col*368,30),big)
        d.text((col*368+15,8),f'{direction} / frame {i+1}/8',font=font,fill='white')
        small=f.resize((56,56),Image.Resampling.LANCZOS);canvas.paste(small,(col*368+156,405),small)
    review.append(canvas)
# GIF uses 10ms ticks: alternate110/120ms with exact900ms total.
review[0].save(R/'eight-frame-review.gif',save_all=True,append_images=review[1:],duration=[110,110,110,120]*2,loop=0)
sheet=Image.new('RGB',(1472,410),'#263139');d=ImageDraw.Draw(sheet)
for row,frames in enumerate(clips):
    for i,f in enumerate(frames):
        sheet.paste(f,(i*184,row*205),f);d.text((i*184+10,row*205+185),f'{list(parents)[row]} {i+1}'+(' key' if i%2==0 else ' new'),fill='white')
sheet.save(R/'contact-sheet.png')
print('16 frames: eight original keys preserved byte-for-byte plus eight new in-betweens. Both cycles900ms.')
