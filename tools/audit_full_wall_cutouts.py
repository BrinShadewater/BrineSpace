"""Read-only cutout/color audit. White candidates are review leads, not deletion masks."""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from shapely.geometry import box, Polygon
from shapely.ops import unary_union
from register_alpha_silhouette import polygons

ROOT=Path(__file__).resolve().parents[1]

def audit(path):
    data=json.loads(path.read_text())
    source=ROOT/data['source'].removeprefix('res://')
    image=Image.open(source).convert('RGB')
    rgb=np.asarray(image).astype(np.int16)
    mask=Image.new('L',image.size)
    for p in data['pieces']: ImageDraw.Draw(mask).polygon([tuple(v) for v in p],fill=255)
    inside=np.asarray(mask)>0
    neutral=(rgb.min(2)>=228)&(rgb.max(2)-rgb.min(2)<=22)&inside
    spans=[]
    for y,row in enumerate(neutral):
        changes=np.flatnonzero(np.diff(np.pad(row.astype(np.int8),(1,1))))
        spans.extend(box(int(a),y,int(b),y+1) for a,b in zip(changes[::2],changes[1::2]))
    candidates=[]
    for part in polygons(unary_union(spans)):
        if part.area<24: continue
        point=part.representative_point()
        candidates.append({'area':part.area,'bounds':list(part.bounds),'seed':[int(point.x),int(point.y)]})
    values=rgb[inside].mean(1)
    return {'source':data['source'],'registration':str(path.relative_to(ROOT)),
            'brightness_percentiles':np.percentile(values,[50,90,99]).tolist(),
            'bright_neutral_candidates':sorted(candidates,key=lambda v:-v['area'])}

if __name__=='__main__':
    output=ROOT/'output/room-polish-2026-09-08'
    output.mkdir(parents=True,exist_ok=True)
    records=[]
    for path in sorted((ROOT/'rooms/full-wall-v1/registrations').glob('*.json')):
        record=audit(path); records.append(record)
        print(path.stem,record['brightness_percentiles'],record['bright_neutral_candidates'][:6],flush=True)
    (output/'cutout-audit.json').write_text(json.dumps(records,indent=2)+'\n')
