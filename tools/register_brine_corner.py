"""Register the BRINE corner source without altering raster pixels."""
import json
import sys
from shapely.geometry import Polygon
from shapely.ops import unary_union
from register_full_wall_props import ROOT,register
from register_alpha_silhouette import polygons,open_holes
folder=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'assets/brine-corner-service-v1')
data=register(folder/'source.png')
shape=unary_union([Polygon(p) for p in data['pieces']]).buffer(-0.6,join_style=2)
data['pieces']=[[[round(x,3),round(y,3)] for x,y in list(p.exterior.coords)[:-1]] for poly in polygons(shape) for p in open_holes(poly)]
data.update(label='BRINE corner life-support console · NW',default_rooms=['brine_core'],display_width=128,corner='northwest',wall_contact={'sides':['north','west']},method='Read-only exterior neutral vector registration; 0.6 source-pixel inset; open inner notch retained')
identity='brine-corner-service-nw'
if '--northeast' in sys.argv:
    identity='brine-corner-analysis-ne'
    data.update(label='BRINE corner analysis and oxygenation · NE',corner='northeast',wall_contact={'sides':['north','east']})
(folder/'registration.json').write_text(json.dumps(data,indent=2)+'\n')
(ROOT/('rooms/full-wall-v1/registrations/'+identity+'.json')).write_text(json.dumps(data,separators=(',',':'))+'\n')
print('BRINE corner registered:',data['region'],'world footprint',128,128*data['region'][3]/data['region'][2])
