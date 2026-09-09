"""Register owner-requested material repaints and tighten reviewed cutout contours.
PNG pixels remain untouched. Earlier registration geometry is preserved in the batch.
"""
import hashlib,json
from pathlib import Path
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
from register_full_wall_props import register,ROOT,APERTURES
from register_alpha_silhouette import polygons,open_holes

DEST=ROOT/'assets/studio-art-fixes-v1'
BACK=DEST/'previous-registrations'
BACK.mkdir(parents=True,exist_ok=True)
REG=ROOT/'rooms/full-wall-v1/registrations'
records=[]
def save(path,data,shape,why):
    if not (BACK/path.name).exists(): (BACK/path.name).write_bytes(path.read_bytes())
    before=json.loads((BACK/path.name).read_text())
    data['pieces']=[[[round(x,3),round(y,3)] for x,y in list(p.exterior.coords)[:-1]] for poly in polygons(shape) for p in open_holes(poly)]
    data['region']=before['region'] # Keep placement scale/pivots stable for owner layouts.
    data['owner_revision']='studio-art-fixes-v1'
    data['method']=why
    path.write_text(json.dumps(data,separators=(',',':'))+'\n')
    records.append({'registration':path.relative_to(ROOT).as_posix(),'source':data['source'],'sha256':data['sha256'],'previous_source':before['source'],'method':why})

for asset,stem in [('drone-service-wall','mining'),('ore-refinery-wall','refinery')]:
    for side in ['', 'west','east']:
        p=REG/(('side-'+asset+'-'+side if side else asset)+'.json')
        previous=json.loads((BACK/p.name).read_text() if (BACK/p.name).exists() else p.read_text())
        src=DEST/(stem+('-sides' if side else '-north')+'.png')
        APERTURES[src.stem]=APERTURES.get(asset,[]) if not side else ([(450,400),(540,410),(1000,400),(1080,410)] if stem=='mining' else previous.get('aperture_seeds',[]))
        fresh=register(src)
        shape=unary_union([Polygon(x) for x in fresh['pieces']])
        if side:
            from PIL import Image
            w,h=Image.open(src).size
            shape=shape.intersection(box(0 if side=='west' else w/2,0,w/2 if side=='west' else w,h))
        previous.update(source=fresh['source'],sha256=fresh['sha256'])
        save(p,previous,shape.buffer(-0.8,join_style=2),'Matte imagegen repaint; independently re-registered silhouette, subpixel edge inset; original region/pivot retained')

for asset in ['mycelium-cultivation-wall','crew-lounge-built-in','maintenance-repair-wall']:
    for p in [REG/(asset+'.json'),*REG.glob('side-'+asset+'-*.json')]:
        if p.name.endswith('-south.json'): continue
        data=json.loads((BACK/p.name).read_text() if (BACK/p.name).exists() else p.read_text())
        # Existing shapes already exclude enclosed holes. Inset only the silhouette,
        # removing the subpixel exterior fringe produced by simplified boundaries.
        shape=unary_union([Polygon(x) for x in data['pieces']])
        shape=shape.buffer(-1.1,join_style=2)
        save(p,data,shape,'Owner cutout correction: 1.1 source-pixel silhouette inset; pale interior art retained; original region/pivot and raster preserved')

(DEST/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
print(f'{len(records)} registrations updated; old geometry, source PNGs and world placement retained')
