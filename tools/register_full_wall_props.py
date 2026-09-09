"""Read-only source registration for the balanced room installation artwork.

Writes vector geometry only. Source PNGs and their colors are never rewritten.
Neutral exterior is excluded; enclosed apertures may be supplied as source seeds.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from shapely.geometry import box
from shapely.ops import unary_union
from register_alpha_silhouette import polygons, open_holes

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/full-wall-props-balanced-v1'
OUT = ROOT / 'rooms/full-wall-v1/registrations'
APERTURES = {
    'ore-refinery-wall': [(330,345),(965,319),(1180,470)],
    'pressure-manifold-wall': [(160,400),(350,500),(480,590),(700,535),(700,587),(166,463),(163,510),(1190,232)],
    'drone-service-wall': [(650,300),(890,344)],
    'mycelium-cultivation-wall': [(247,335),(246,558)],
    'emergency-isolation-wall': [(472,395),(473,548),(1109,316),(1110,379)],
    'bio-culture-wall': [(343,328)],
}

def register(path, neutral_min=228):
    rgb = np.asarray(Image.open(path).convert('RGB')).astype(np.int16)
    neutral = (rgb.min(2) >= neutral_min) & (rgb.max(2)-rgb.min(2) <= 22)
    flood = Image.fromarray(np.where(neutral, 255, 0).astype('uint8')).copy()
    width, height = flood.size
    for seed in [(0,0), (width-1,0), (0,height-1), (width-1,height-1)]:
        ImageDraw.floodfill(flood, seed, 128)
    for seed in APERTURES.get(path.stem, []):
        if flood.getpixel(seed) == 255:
            ImageDraw.floodfill(flood, seed, 128)
    mask = np.asarray(flood) != 128
    spans = []
    for y, row in enumerate(mask):
        changes = np.flatnonzero(np.diff(np.pad(row.astype(np.int8), (1,1))))
        spans.extend(box(int(a), y, int(b), y+1) for a,b in zip(changes[::2], changes[1::2]))
    components = [p.simplify(1, preserve_topology=True) for p in polygons(unary_union(spans)) if p.area >= 90]
    bounds = unary_union(components).bounds
    pieces = [list(p.exterior.coords)[:-1] for c in components for p in open_holes(c)]
    return {'source': 'res://'+path.relative_to(ROOT).as_posix(),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'method': 'Read-only exterior-neutral vector registration; raster unchanged',
            'neutral_min_channel': neutral_min,
            'neutral_max_channel_spread': 22,
            'region': [bounds[0],bounds[1],bounds[2]-bounds[0],bounds[3]-bounds[1]],
            'pieces': [[[round(x,3),round(y,3)] for x,y in p] for p in pieces]}

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for path in sorted(SOURCE.glob('*.png')):
        if (OUT/(path.stem+'.json')).exists():
            print('Preserved reviewed registration:',path.stem,flush=True)
            continue
        if path.stem == 'maintenance-repair-wall':
            path = ROOT / 'assets/full-wall-props-refined-v2/maintenance-repair-wall.png'
        result = register(path)
        (OUT/(path.stem+'.json')).write_text(json.dumps(result, separators=(',',':'))+'\n')
        print(path.stem, result['region'], len(result['pieces']), flush=True)
