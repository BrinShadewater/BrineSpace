"""Register reviewed rear-facing south banks; leave all PNG source pixels intact."""
import json
from shapely.geometry import Polygon
from shapely.ops import unary_union
from register_full_wall_props import register, ROOT
from register_alpha_silhouette import polygons,open_holes
folder=ROOT/'assets/south-wall-facing-v3'
records=[]
for row in json.loads((folder/'generation.json').read_text()):
    data=register(folder/(row['id']+'.png'))
    shape=unary_union([Polygon(p) for p in data['pieces']]).buffer(-0.8,join_style=2)
    data['pieces']=[[[round(x,3),round(y,3)] for x,y in list(p.exterior.coords)[:-1]] for poly in polygons(shape) for p in open_holes(poly)]
    data['wall_contact']={'side':'south','purpose':'Rear edge against south wall; operation faces room interior'}
    data['direction']='south'
    data['method']+='; 0.8 source-pixel inset; authored overhead rear-facing view'
    path=ROOT/('rooms/full-wall-v1/registrations/side-'+row['id']+'-south.json')
    path.write_text(json.dumps(data,separators=(',',':'))+'\n')
    records.append({'id':row['id'],'source':data['source'],'sha256':data['sha256'],'registration':path.relative_to(ROOT).as_posix(),'status':'registered; native review required'})
(folder/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
print(f'Registered {len(records)} rear-facing south banks')
