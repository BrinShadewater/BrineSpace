"""Register Veld north scanner interiors with independent original endpoints."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image
from rebuild_bill_art import binary, chroma

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'

def main(direction="north"):
    assert direction=="north"
    durations=[140]*6
    endpoint=BASE/'sources/veld-north-scanner-body-closing-01.png'
    source=BASE/'sources/veld-north-scanner-strip-01.png'
    raw=binary(chroma(source))
    expected,height,soles=(1774,887),660,[775]*4
    assert raw.size==expected
    scale=148/height
    frames=[Image.open(BASE/f'sources/veld-north-scanner-body-opening-01.png').convert('RGBA')]
    supports=[]
    for i in range(4):
        tile=raw.crop((i*raw.width//4,0,(i+1)*raw.width//4,raw.height))
        sole=soles[i]
        _,x=np.where(np.asarray(tile)[sole-5:sole+1,:,3]>0)
        anchor=float((x.min()+x.max())/2);supports.append([anchor,sole])
        dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
        frame=Image.new('RGBA',(184,184))
        frame.alpha_composite(dense,(round(92-anchor*scale),round(172-sole*scale)))
        frames.append(frame)
    frames.append(Image.open(endpoint).convert('RGBA'))
    out=BASE/f'review/veld-role-interact-{direction}-strip-01';out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1104,184),'#293b40');preview=[]
    for i,frame in enumerate(frames):
        frame.save(out/f'interact-{direction}-{i:03}.png');sheet.paste(frame,(184*i,0),frame)
        matte=Image.new('RGB',frame.size,'#293b40');matte.paste(frame,(0,0),frame);preview.append(matte)
    sheet.save(out/'contact.png')
    preview[0].save(out/'motion.gif',save_all=True,append_images=preview[1:],duration=durations,loop=0)
    report=dict(status='unselected_registered_sequence',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,supports=supports,pivot=[92,172],durationsMs=durations,uniqueFrames=len({f.tobytes() for f in frames}),limits='Native motion and selected-pack verification pending; Fitted helmet variant pending. Endpoints independently preserved.')
    (out/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
