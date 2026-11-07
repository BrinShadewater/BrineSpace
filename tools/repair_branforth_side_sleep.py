"""Build a small breathing deformation from Branforth's own lie-down endpoint."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from extract_crew_seating_study import main as extract

ROOT=Path(__file__).resolve().parents[1]

def main(actor='branforth',direction='east'):
    centers={('branforth','east'):105,('veld','west'):170,('branforth','west'):174}
    chest_center=centers[actor,direction]
    source=extract(actor,direction,'01','sleeping','gutter')['lie-down'][-1]
    pixels=np.asarray(source)
    yy,xx=np.indices(pixels.shape[:2])
    # Lift only the chest by at most one dense pixel; keep skull, pelvis, boots
    # and the mattress-facing lower edge fixed. This is motion, not rescaling.
    weight=np.clip(1-abs(xx-chest_center)/31,0,1)*np.clip((224-yy)/18,0,1)
    out=ROOT/f'character/crew-action-detail-v2/review/{actor}-sleeping-{direction}-local-01'
    out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(6*256,256),'#293b40');draw=ImageDraw.Draw(sheet)
    frames=[]
    amplitudes=[0,.5,1,1,.5,0]
    for i,amplitude in enumerate(amplitudes):
        sy=np.minimum(255,yy+np.rint(weight*amplitude).astype(int))
        frame=Image.fromarray(pixels[sy,xx].copy())
        frame.save(out/f'sleep-{i:03}.png');frames.append(frame)
        sheet.paste(frame,(i*256,0),frame);draw.text((i*256+4,4),str(i),fill='white')
    sheet.save(out/'contact.png')
    (out/'recipe.json').write_text(json.dumps(dict(status='source_rig_requires_runtime_review',actor=actor,direction=direction,sourceRevision='01',donor='lie-down-005',amplitudes=amplitudes,chestCenterX=chest_center,chestHalfWidth=31,maxLift=1,groundY=224),indent=2)+'\n')
    assert np.array_equal(np.asarray(frames[0]),pixels)
    assert np.array_equal(np.asarray(frames[-1]),pixels)
    assert not np.array_equal(np.asarray(frames[2]),pixels)
    print('Six breathing frames; exact endpoint/loop seam; nonzero chest motion')
    return frames

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--actor',default='branforth',choices=['branforth','veld'])
    parser.add_argument('--direction',default='east',choices=['east','west'])
    args=parser.parse_args();main(args.actor,args.direction)
