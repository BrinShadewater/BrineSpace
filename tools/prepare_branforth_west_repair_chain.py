"""Register the west repair source with canonical identity; no runtime writes."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-repair-polish-v1'
OUT=BASE/'review/branforth-west-chain-02'
SOURCE_NAMES=['branforth-west-chain-02.png','branforth-idle-west-bare-endpoint.png','branforth-idle-west-helmet-endpoint.png']

def rgba(p): return Image.open(p).convert('RGBA')

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    source=rgba(BASE/'sources'/SOURCE_NAMES[0])
    records=[];poses=[]
    # Source rows are not equal: the first row's boots extend below y512.
    crops=[(0,0,512,592),(512,0,1024,592),(1024,0,1536,592),
           (0,592,512,1024),(512,592,1024,1024),(1024,592,1536,1024)]
    # Measure the forward boot alone, excluding the grounded rear knee/boot.
    boot_windows=[(301,415),(218,322),(149,256),(182,290),(134,244),(72,182)]
    for i,(crop,window) in enumerate(zip(crops,boot_windows)):
        tile=source.crop(crop);alpha=np.asarray(tile)[:,:,3]>=192
        labels,_=label(alpha);sizes=np.bincount(labels.ravel());sizes[0]=0
        tile.putalpha(Image.fromarray(((labels==sizes.argmax())*255).astype('uint8')))
        a=np.asarray(tile)[:,:,3];left,right=window
        ys,xs=np.where(a[:,left:right]>0);bottom=int(ys.max())+1
        _,xs=np.where(a[bottom-5:bottom,left:right]>0);support=float(np.median(xs))+left
        scale=.30
        dense=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX)
        dense.putalpha(dense.getchannel('A').point(lambda v:255 if v>=128 else 0))
        offset=(round(124-support*scale),round(224-bottom*scale))
        frame=Image.new('RGBA',(256,256));frame.alpha_composite(dense,offset);poses.append(frame)
        records.append(dict(cell=crop,bootWindow=window,support=[support,bottom],scale=scale,offset=offset))
    def idle(variant):
        frame=Image.new('RGBA',(256,256));frame.alpha_composite(rgba(BASE/f'sources/branforth-idle-west-{variant}-endpoint.png'),(36,52));return frame
    # Five distinct descent poses; final pose deliberately settles across two slots.
    # Three authored work poses play forward/back, with an exact closing frame.
    raw={'kneel-west':[None,poses[0],poses[1],poses[2],poses[3],poses[3]],
         'repair-west':[poses[i] for i in [3,4,5,4,3,3]]}
    bare={};worn={};fits=[]
    for state,row in raw.items():
        bare[state]=[];worn[state]=[]
        for i,frame in enumerate(row):
            if frame is None:
                bare[state].append(idle('bare'));worn[state].append(idle('helmet'));continue
            top=frame.getbbox()[1];_,xs=np.where(np.asarray(frame)[top+2:top+12,:,3]>0)
            cx=round(float(np.median(xs)))
            for variant,clips,rect in [('bare',bare,(76,20,109,53)),('helmet',worn,(70,16,114,59))]:
                head=rgba(BASE/f'sources/branforth-idle-west-{variant}-endpoint.png').crop(rect)
                at=(cx+rect[0]-91,top+rect[1]-21)
                out=frame.copy();out.paste((0,0,0,0),(cx-17,top-5,cx+17,top+27));out.alpha_composite(head,at)
                clips[state].append(out)
                fits.append(dict(state=state,frame=i,variant=variant,position=at))
    for variant,clips in [('bare',bare),('helmet',worn)]:
        clips['stand-west']=list(reversed(clips['kneel-west']))
        for state,row in clips.items():
            for i,frame in enumerate(row):frame.save(OUT/f'{variant}-{state}-{i:03}.png')
        assert clips['kneel-west'][-1].tobytes()==clips['repair-west'][0].tobytes()
        assert clips['repair-west'][-1].tobytes()==clips['stand-west'][0].tobytes()
        assert clips['stand-west'][-1].tobytes()==idle(variant).tobytes()
    sequence=[('kneel-west',i) for i in range(6)]+[('repair-west',i) for _ in range(3) for i in range(6)]+[('stand-west',i) for i in range(6)]
    frames=[];times=[]
    for state,i in sequence:
        board=Image.new('RGB',(512,280),'#17212a');d=ImageDraw.Draw(board);d.text((8,6),state+' / bare',fill='white');d.text((270,6),'helmet',fill='white')
        for col,clips in enumerate([bare,worn]):board.paste(clips[state][i],(col*256,24),clips[state][i])
        frames.append(board);times.append(140 if state=='repair-west' else [70,90,100,100,90,70][i])
    frames[0].save(OUT/'chain.gif',save_all=True,append_images=frames[1:],duration=times,loop=0)
    sheet=Image.new('RGB',(1536,560),'#17212a')
    for row,clips in enumerate([bare,worn]):
        for i,f in enumerate(clips['kneel-west']):sheet.paste(f,(i*256,row*280+24),f)
    sheet.save(OUT/'contact.png')
    (OUT/'registration.json').write_text(json.dumps(dict(status='prepared_runtime_chain',selection='tools/branforth_repair_revision.py',sources={name:hashlib.sha256((BASE/'sources'/name).read_bytes()).hexdigest() for name in SOURCE_NAMES},registration=records,headFits=fits,derived='Canonical face and helmet. Final descent hold and ping-pong tool motion; stand reverses kneel.',limits=['Native and station review recorded separately','Not owner accepted']),indent=2)+'\n')
    print('36 west candidate frames; exact joins pass; no runtime writes')
    return bare,worn

if __name__=='__main__':build()
