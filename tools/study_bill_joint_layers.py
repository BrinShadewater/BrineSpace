"""Isolated knee-coverage study; preserves the selected rig's joint trajectories."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from PIL import Image, ImageDraw
from repair_bill_walk import build, place

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/bill-pixel-layer-2026-09-21'
SOURCES = ROOT / 'output/bill-body-motion-2026-09-20'
ANCHORS = {
    'east': {'far': ((78,119),(63,143),(50,158)), 'near': ((90,114),(102,139),(109,158))},
    'west': {'far': ((83,117),(72,141),(63,159)), 'near': ((99,116),(111,141),(125,158))},
}


def joint_patch(source, center, radius=9):
    mask = Image.new('L', source.size)
    x,y = center
    ImageDraw.Draw(mask).ellipse((x-radius,y-radius,x+radius,y+radius), fill=255)
    pixels = np.array(source)
    pixels[np.array(mask) == 0] = 0
    return Image.fromarray(pixels)


def main():
    OUT.mkdir(exist_ok=True)
    audit = {}
    for direction, anchors in ANCHORS.items():
        source_path = SOURCES / f'{direction}-preserved-0.png'
        source = Image.open(source_path).convert('RGBA')
        baseline,layers,torso,trajectory = build(source,direction)
        frames=[]
        for phase,poses in enumerate(trajectory):
            frame=Image.new('RGBA',source.size)
            bob=-1 if phase in (1,4) else 0
            for leg in ('far','near'):
                hip,knee,ankle=map(np.array,anchors[leg])
                target=poses[leg]
                th,tk,ta=map(np.array,(target['hip'],target['knee'],target['ankle']))
                upper=place(layers[leg]['upper'],hip,knee,th,tk)
                upper.paste((0,0,0,0),(0,0,184,119+bob))
                frame.alpha_composite(upper)
                frame.alpha_composite(place(layers[leg]['lower'],knee,ankle,tk,ta))
                # Put the original continuous kneecap surface over the cutout seam.
                frame.alpha_composite(place(joint_patch(source,knee),knee,ankle,tk,ta))
                step=target['phase']
                angle=([-.25,-.25,-.25,-.1,-.3,-.25] if leg=='far' else [.25,.25,.25,.1,-.05,.1])[step]
                vector=np.array([10*math.cos(angle),10*math.sin(angle)])
                frame.alpha_composite(place(layers[leg]['foot'],ankle,ankle+[10,0],ta,ta+vector))
            frame.alpha_composite(torso,(0,bob))
            frame.paste(source.crop((0,0,184,119)),(0,bob))
            frame.save(OUT/f'{direction}-{phase:02}.png')
            frames.append(frame)
        sheet=Image.new('RGBA',(184*6,184*2),'#26383c')
        for i,(before,after) in enumerate(zip(baseline,frames)):
            sheet.alpha_composite(before,(184*i,0));sheet.alpha_composite(after,(184*i,184))
        sheet.resize((2208,736),Image.Resampling.NEAREST).save(OUT/f'{direction}-comparison.png')
        audit[direction]={'source_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),
                          'trajectory':trajectory,'scope':'Kneecap surface overlap only; no torso/arm repair or runtime selection change.'}
    (OUT/'provenance.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    print('Twelve isolated joint-study frames written; production unchanged.')


if __name__=='__main__': main()
