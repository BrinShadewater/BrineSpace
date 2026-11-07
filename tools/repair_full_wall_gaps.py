"""Repair explicitly reviewed enclosed gaps without changing raster, outer outline or anchors."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
from shapely.geometry import Polygon,Point,box
from shapely.ops import unary_union
from register_alpha_silhouette import polygons,open_holes

ROOT=Path(__file__).resolve().parents[1]

def repair(registration,seeds):
    data=json.loads(registration.read_text())
    source=ROOT/data['source'].removeprefix('res://')
    if hashlib.sha256(source.read_bytes()).hexdigest()!=data['sha256']:
        raise ValueError('Source hash changed: re-register and review rather than reusing old anchors')
    rgb=np.asarray(Image.open(source).convert('RGB')).astype(np.int16)
    neutral=(rgb.min(2)>=228)&(rgb.max(2)-rgb.min(2)<=22)
    flood=Image.fromarray(np.where(neutral,255,0).astype('uint8')).copy()
    shape=unary_union([Polygon(p) for p in data['pieces']])
    active=[]
    for seed in seeds:
        if not shape.covers(Point(*seed)): continue # Repeat repairs are idempotent.
        if flood.getpixel(tuple(seed)) not in [255,128]: raise ValueError('Seed is artwork, not bright neutral background: '+str(seed))
        ImageDraw.floodfill(flood,tuple(seed),128)
        active.append(seed)
    if not active: return data
    removed=np.asarray(flood)==128
    if removed[0,:].any() or removed[-1,:].any() or removed[:,0].any() or removed[:,-1].any():
        raise ValueError('Seed connects to exterior; this tool is only for enclosed gaps')
    spans=[]
    for y,row in enumerate(removed):
        changes=np.flatnonzero(np.diff(np.pad(row.astype(np.int8),(1,1))))
        spans.extend(box(int(a),y,int(b),y+1) for a,b in zip(changes[::2],changes[1::2]))
    # Pixel-aligned hole boundaries; no global simplification or anchor recomputation.
    fixed=shape.difference(unary_union(spans))
    assert fixed.bounds==shape.bounds
    for seed in seeds: assert not fixed.covers(Point(*seed))
    data['pieces']=[[[round(x,3),round(y,3)] for x,y in list(p.exterior.coords)[:-1]] for poly in polygons(fixed) for p in open_holes(poly)]
    previous=data.get('aperture_seeds',[])
    data['aperture_seeds']=previous+[s for s in seeds if s not in previous]
    return data

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('registration',type=Path)
    parser.add_argument('--seeds',required=True,help='Reviewed source pixels: x,y;x,y')
    args=parser.parse_args()
    seeds=[[int(n) for n in pair.split(',')] for pair in args.seeds.split(';')]
    result=repair(args.registration,seeds)
    args.registration.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print('Verified all requested gaps excluded; source, outer bounds and anchors retained')
