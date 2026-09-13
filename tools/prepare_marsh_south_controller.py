"""Register directional controller interiors with independent original endpoints."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image
from rebuild_bill_art import binary, chroma

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'

def main(direction="south"):
    assert direction in ["south","west","north"]
    pack=ROOT/'character/marsh-v2'
    endpoint=BASE/f'sources/marsh-role-interact-{direction}-end-reference-01.png'
    durations=None
    for relative in json.loads((pack/'catalog.json').read_text())['body']:
        path=pack/relative; manifest=json.loads(path.read_text())
        for state in manifest['states']:
            if state['id']!=f'interact-{direction}':continue
            durations=state['frameDurationsMs']
            if not endpoint.exists():
                original=Image.open(path.parent/state['frameFiles'][-1]).convert('RGBA')
                canvas=Image.new('RGBA',(184,184))
                canvas.alpha_composite(original,(round(92-manifest['pivot'][0]),round(172-manifest['pivot'][1])))
                canvas.save(endpoint)
    assert durations and len(durations)==6
    source=BASE/f'sources/marsh-role-interact-{direction}-strip-01.png'
    raw=binary(chroma(source))
    expected,height,soles={"south":((1934,813),620,[701]*4),"west":((1881,836),588,[717,718,719,717]),"north":((2172,724),554,[642]*4)}[direction]
    assert raw.size==expected
    scale=148/height
    frames=[Image.open(BASE/f'sources/marsh-role-interact-{direction}-reference-01.png').convert('RGBA')]
    supports=[]
    for i in range(4):
        tile=raw.crop((i*raw.width//4,0,(i+1)*raw.width//4,raw.height))
        sole=soles[i]
        _,x=np.where(np.asarray(tile)[sole-5:sole+1,:,3]>0)
        anchor=float(np.median(x)) if direction=="west" else float((x.min()+x.max())/2);supports.append([anchor,sole])
        dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
        frame=Image.new('RGBA',(184,184))
        frame.alpha_composite(dense,(round(92-anchor*scale),round(172-sole*scale)))
        frames.append(frame)
    frames.append(Image.open(endpoint).convert('RGBA'))
    out=BASE/f'review/marsh-role-interact-{direction}-strip-01';out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1104,184),'#293b40');preview=[]
    for i,frame in enumerate(frames):
        frame.save(out/f'interact-{direction}-{i:03}.png');sheet.paste(frame,(184*i,0),frame)
        matte=Image.new('RGB',frame.size,'#293b40');matte.paste(frame,(0,0),frame);preview.append(matte)
    sheet.save(out/'contact.png')
    preview[0].save(out/'motion.gif',save_all=True,append_images=preview[1:],duration=durations,loop=0)
    report=dict(status='unselected_registered_sequence',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,supports=supports,pivot=[92,172],durationsMs=durations,uniqueFrames=len({f.tobytes() for f in frames}),limits='Native motion and selected-pack verification pending; no helmet. Endpoints independently preserved.')
    (out/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
