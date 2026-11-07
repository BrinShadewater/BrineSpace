"""Measure authored flame endpoints and convert their registered pixels to world units."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-work-joins-v1'


def build():
    catalog=ROOT/'character/marsh-v2/catalog.json';selected={}
    for relative in json.loads(catalog.read_text())['body']:
        p=(catalog.parent/relative).resolve();m=json.loads(p.read_text())
        for state in m['states']:selected[state['id']]=(p,m,state)
    offsets={};records=[]
    for direction in ['east','west','north','south']:
        p,m,s=selected['weld-'+direction];offsets[direction]=[]
        for slot,f in enumerate(s['frameFiles']):
            path=ROOT/f[6:] if f.startswith('res://') else p.parent/f
            im=Image.open(path).convert('RGBA');points=[]
            for y in range(im.height):
                for x in range(im.width):
                    region=(y>=180 if direction=='south' else x>=120 and y>=40 if direction=='east' else x<=65 and y>=40 if direction=='west' else x>=106 and y>=40)
                    r,g,b,a=im.getpixel((x,y))
                    if region and a>200 and r>180 and 65<g<235 and b<170 and r>g*1.1:points.append((x,y))
            assert points,(direction,slot)
            axis=1 if direction=='south' else 0
            extreme=(min if direction=='west' else max)(point[axis] for point in points)
            tip=[point for point in points if abs(point[axis]-extreme)<=1]
            pixel=[sum(point[i]+.5 for point in tip)/len(tip) for i in range(2)]
            # Character renderer's physical standing ruler is .17 * 384 = 65.28.
            offset=[round((pixel[i]-m['pivot'][i])*65.28/m['standingHeight'],6) for i in range(2)]
            offsets[direction].append(offset)
            records.append(dict(direction=direction,slot=slot,source=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),pixel=pixel,pivot=m['pivot'],standingHeight=m['standingHeight'],offset=offset))
    (OUT/'torch-tip-offsets.json').write_text(json.dumps(offsets,indent=2)+'\n')
    (OUT/'torch-tip-measurements.json').write_text(json.dumps(records,indent=2)+'\n')
    print('Measured24 Marsh welding flame anchors through the65.28/148 standing ruler')


if __name__=='__main__':build()
