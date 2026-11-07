"""Register separately generated side views from paired sheets; never rotate or edit pixels."""
import argparse
import json
from PIL import Image
from pathlib import Path
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
from register_full_wall_props import register,ROOT
from register_alpha_silhouette import polygons,open_holes

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-dir',default='assets/side-wall-props-v1')
    parser.add_argument('--neutral-min',type=int,default=228)
    parser.add_argument('--output-dir',default='rooms/full-wall-v1/registrations')
    args=parser.parse_args()
    output_dir=ROOT/args.output_dir
    output_dir.mkdir(parents=True,exist_ok=True)
    entries=json.loads((ROOT/'rooms/full-wall-v1/manifest.json').read_text())
    for entry in entries:
        source=ROOT/args.source_dir/(entry['room']+'.png')
        if not source.exists(): continue
        targets=[output_dir/('side-'+entry['asset']+'-'+d+'.json') for d in ['west','east']]
        if all(p.exists() for p in targets):
            print('Preserved reviewed side registrations:',entry['room'],flush=True)
            continue
        data=register(source,args.neutral_min)
        width,height=Image.open(source).size
        half=width/2
        shape=unary_union([Polygon(p) for p in data['pieces']])
        for direction,index in [('west',0),('east',1)]:
            # Inspect backing/seat orientation: the lounge generator reversed the requested order.
            if entry['room']=='crew_lounge': index=1-index
            part=shape.intersection(box(index*half,0,(index+1)*half,height))
            x,y,x2,y2=part.bounds
            assert x>index*half and x2<(index+1)*half, 'View crosses sheet divider'
            assert (y2-y)/(x2-x)>2, 'Not a long side-wall source'
            result=dict(data)
            result['region']=[x,y,x2-x,y2-y]
            result['direction']=direction
            result['pieces']=[[[round(px,3),round(py,3)] for px,py in list(p.exterior.coords)[:-1]] for poly in polygons(part) for p in open_holes(poly)]
            target=output_dir/('side-'+entry['asset']+'-'+direction+'.json')
            if target.exists(): continue
            target.write_text(json.dumps(result,separators=(',',':'))+'\n')
            print(entry['room'],direction,result['region'],flush=True)
