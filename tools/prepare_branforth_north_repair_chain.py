"""Prepare a north repair audition; does not write runtime frames."""
from pathlib import Path
import json
import hashlib
import numpy as np
from scipy.ndimage import label
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-repair-polish-v1'
OUT=BASE/'review/branforth-north-chain-02'

def rgba(path): return Image.open(path).convert('RGBA')

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    records=[]
    def extract(name,cols,rows):
        raw=rgba(BASE/'sources'/name); result=[]
        for i in range(cols*rows):
            cell=(i%cols*raw.width//cols,i//cols*raw.height//rows,(i%cols+1)*raw.width//cols,(i//cols+1)*raw.height//rows)
            tile=raw.crop(cell);tile.putalpha(tile.getchannel('A').point(lambda a:255 if a>=192 else 0))
            labels,count=label(np.asarray(tile)[:,:,3]>0)
            sizes=np.bincount(labels.ravel());sizes[0]=0
            tile.putalpha(Image.fromarray(((labels==sizes.argmax())*255).astype('uint8')))
            box=tile.getbbox(); a=np.asarray(tile)[:,:,3]
            # Planted left boot is screen-left, not the right knee or body pivot.
            left=a[:,:int((box[0]+box[2])/2)]
            ys,xs=np.where(left>0); bottom=int(ys.max())+1
            _,xs=np.where(left[max(0,bottom-8):bottom]>0); support=float(np.median(xs))
            scale=.25
            dense=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX)
            dense.putalpha(dense.getchannel('A').point(lambda a:255 if a>=128 else 0))
            offset=(round(111-support*scale),round(224-bottom*scale))
            frame=Image.new('RGBA',(256,256));frame.alpha_composite(dense,offset);result.append(frame)
            records.append(dict(source=name,cell=cell,scale=scale,support=[support,bottom],offset=offset))
        return result
    intermediate=extract('branforth-kneel-north-02.png',2,2)
    authored=extract('branforth-repair-north-01.png',3,2)
    work=[authored[i] for i in [0,1,2,3,4,0]]
    def idle(variant):
        frame=Image.new('RGBA',(256,256));frame.alpha_composite(rgba(BASE/f'sources/branforth-idle-north-{variant}-endpoint.png'),(36,52));return frame
    kneel=[idle('bare')]+intermediate+[work[0].copy()]
    bare={'kneel-north':kneel,'repair-north':work,'stand-north':list(reversed(kneel))}
    head=rgba(BASE/'sources/branforth-idle-north-helmet-endpoint.png').crop((73,21,112,61))
    worn={};fits=[]
    for state,row in bare.items():
        worn[state]=[]
        for i,frame in enumerate(row):
            if (state=='kneel-north' and i==0) or (state=='stand-north' and i==5): out=idle('helmet')
            else:
                top=frame.getbbox()[1];_,xs=np.where(np.asarray(frame)[top+3:top+12,:,3]>0)
                cx=round(float(np.median(xs)));at=(cx-19,top-4)
                out=frame.copy();out.paste((0,0,0,0),(cx-19,top-4,cx+20,top+31));out.alpha_composite(head,at)
                fits.append(dict(state=state,frame=i,at=at))
            worn[state].append(out)
    for variant,clips in [('bare',bare),('helmet',worn)]:
        for state,row in clips.items():
            for i,frame in enumerate(row): frame.save(OUT/f'{variant}-{state}-{i:03}.png')
        assert clips['kneel-north'][-1].tobytes()==clips['repair-north'][0].tobytes()
        assert clips['repair-north'][-1].tobytes()==clips['stand-north'][0].tobytes()
        assert clips['stand-north'][-1].tobytes()==idle(variant).tobytes()
    sequence=[('kneel-north',i) for i in range(6)]+[('repair-north',i) for _ in range(3) for i in range(6)]+[('stand-north',i) for i in range(6)]
    preview=[];times=[]
    for state,i in sequence:
        board=Image.new('RGB',(512,280),'#17212a');d=ImageDraw.Draw(board);d.text((8,6),'NORTH STUDY / '+state,fill='white');d.text((270,6),'Helmet',fill='white')
        for col,clips in enumerate([bare,worn]):board.paste(clips[state][i],(col*256,24),clips[state][i])
        preview.append(board);times.append(140 if state=='repair-north' else [70,90,100,100,90,70][i])
    preview[0].save(OUT/'chain.gif',save_all=True,append_images=preview[1:],duration=times,loop=0)
    sheet=Image.new('RGB',(1536,560),'#17212a')
    for row,clips in enumerate([bare,worn]):
        for i,f in enumerate(clips['kneel-north']):sheet.paste(f,(i*256,row*280+24),f)
    sheet.save(OUT/'contact.png')
    sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (BASE/'sources').glob('*north*png')}
    (OUT/'registration.json').write_text(json.dumps(dict(status='prepared_runtime_chain',selection='tools/branforth_repair_revision.py',sources=sources,registration=records,helmetFits=fits,rejected='kneel-north-01: missing early descent and oversized anatomy',limits=['Native player review recorded separately; not autonomous gameplay acceptance','Owner acceptance pending']),indent=2)+'\n')
    print('36 candidate frames; exact joins pass; runtime untouched')
    return bare,worn

if __name__=='__main__': build()
