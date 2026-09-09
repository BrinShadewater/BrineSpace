"""Register the unchanged observation sprite as three depth-sorted wall pieces."""
import json
from pathlib import Path
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from register_alpha_silhouette import polygons, open_holes
from register_full_wall_props import register

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'rooms/underwater/observation-room-v1/registration.json'
data = register(ROOT / 'rooms/underwater/observation-room-v1/source-v3.png',neutral_min=110)
shape = unary_union([Polygon(piece) for piece in data['pieces']])
parts = []
for name, clip, footprint in [
    ('observation_north', box(0,0,1254,560), [-180,-176,360,151]),
    ('observation_west', box(0,560,627,1254), [-180,-25,49,195]),
    ('observation_east', box(627,560,1254,1254), [131,-25,49,195]),
]:
    geometry = shape.intersection(clip)
    x,y,r,b = geometry.bounds
    pieces = [list(p.exterior.coords)[:-1] for c in polygons(geometry) for p in open_holes(c)]
    parts.append(dict(id=name,footprint=footprint,bounds=[x,y,r-x,b-y],pieces=pieces))
data['parts'] = parts
data['neutral_min'] = 110
data['visual_acceptance'] = 'pending native review'
path.write_text(json.dumps(data,separators=(',',':'))+'\n')
print('Registered three pieces; source raster unchanged.')
